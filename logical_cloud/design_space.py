"""Domain-independent factor design spaces: questions, choices, intersections.

This is *not* a simulator, a universal optimizer, or objective proof of
product quality. It is a small evidence-qualified way for agents and humans
to expose which variables matter, which are still open, and what needs an
experiment. Partial candidate assignments are first-class.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import ModelError

MATURITY = {"unexamined", "hypothesis", "upstream", "repo_implemented", "observed"}
EVIDENCE = {"unknown", "hypothesis", "source", "simulation", "automated_test", "device", "human"}
EXPERIMENT_STATUS = {"proposed", "source_checked", "simulated", "automated_test", "observed"}


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ModelError(f"{field} must be nonempty text")
    return value


def _ident(value: Any, label: str) -> str:
    _text(value, label)
    if any(c not in "abcdefghijklmnopqrstuvwxyz0123456789._-" for c in value):
        raise ModelError(f"{label} must be a lowercase stable identifier")
    return value


def _list(value: Any, name: str) -> list:
    if not isinstance(value, list):
        raise ModelError(f"{name} must be a list")
    return value


def _assignments(values: Any, choices: dict[str, set[str]], label: str) -> dict:
    if not isinstance(values, dict):
        raise ModelError(f"{label} must be an object of named factor assignments")
    for factor, option in values.items():
        if factor not in choices:
            raise ModelError(f"{label} uses unknown factor {factor}")
        if option not in choices[factor]:
            raise ModelError(f"{label} uses unknown option {factor}={option}")
    return values


def validate_design(doc: dict) -> None:
    if not isinstance(doc, dict) or doc.get("schema_version") != 1:
        raise ModelError("design schema_version must be 1")
    _ident(doc.get("id"), "design id")
    intent = doc.get("intent")
    if not isinstance(intent, dict):
        raise ModelError("design intent must be an object")
    _text(intent.get("goal"), "human goal")
    invariants = _list(intent.get("invariants"), "intent invariants")
    if not invariants:
        raise ModelError("at least one human-facing invariant is required")
    for invariant in invariants:
        _text(invariant, "invariant")

    choices: dict[str, set[str]] = {}
    factors = _list(doc.get("factors"), "factors")
    if not factors:
        raise ModelError("design must contain at least one factor")
    for factor in factors:
        if not isinstance(factor, dict):
            raise ModelError("factor must be an object")
        ident = _ident(factor.get("id"), "factor id")
        if ident in choices:
            raise ModelError(f"duplicate factor {ident}")
        _text(factor.get("question"), f"{ident} question")
        _text(factor.get("relevance"), f"{ident} relevance")
        options = _list(factor.get("options"), f"{ident} options")
        if not options:
            raise ModelError(f"factor {ident} needs options")
        available = set()
        for option in options:
            if not isinstance(option, dict):
                raise ModelError(f"factor {ident} option must be an object")
            name = _ident(option.get("id"), f"{ident} option id")
            if name in available:
                raise ModelError(f"duplicate option {ident}={name}")
            available.add(name)
            _text(option.get("meaning"), f"{ident}={name} meaning")
            if option.get("maturity", "unexamined") not in MATURITY:
                raise ModelError(f"unknown maturity for {ident}={name}")
            evidence = option.get("evidence", {"kind": "unknown"})
            if not isinstance(evidence, dict) or evidence.get("kind") not in EVIDENCE:
                raise ModelError(f"invalid evidence type for {ident}={name}")
            if option.get("maturity") == "observed" and evidence.get("kind") not in {"device", "human"}:
                raise ModelError(f"observed option {ident}={name} requires observed evidence")
            if option.get("maturity") in {"upstream", "repo_implemented", "observed"} and not evidence.get("refs"):
                raise ModelError(f"supported option {ident}={name} must provide evidence refs")
        choices[ident] = available

    used_variants = set()
    for variant in _list(doc.get("variants", []), "variants"):
        if not isinstance(variant, dict):
            raise ModelError("variant must be an object")
        name = _ident(variant.get("id"), "variant id")
        if name in used_variants:
            raise ModelError(f"duplicate variant {name}")
        used_variants.add(name)
        _assignments(variant.get("set", {}), choices, f"variant {name}")
        _text(variant.get("purpose"), f"variant {name} purpose")

    rule_ids = set()
    for rule in _list(doc.get("intersections", []), "intersections"):
        if not isinstance(rule, dict):
            raise ModelError("intersection must be an object")
        name = _ident(rule.get("id"), "intersection id")
        if name in rule_ids:
            raise ModelError(f"duplicate intersection {name}")
        rule_ids.add(name)
        when = _assignments(rule.get("when"), choices, f"intersection {name} when")
        needs = _assignments(rule.get("requires"), choices, f"intersection {name} requires")
        if not when or not needs:
            raise ModelError(f"intersection {name} must have both when and requires")
        if rule.get("strength") not in {"design_contract", "hypothesis"}:
            raise ModelError(f"intersection {name} needs declared strength")
        _text(rule.get("reason"), f"intersection {name} reason")

    experiment_ids = set()
    for experiment in _list(doc.get("experiments", []), "experiments"):
        if not isinstance(experiment, dict):
            raise ModelError("experiment must be an object")
        name = _ident(experiment.get("id"), "experiment id")
        if name in experiment_ids:
            raise ModelError(f"duplicate experiment {name}")
        experiment_ids.add(name)
        _text(experiment.get("question"), f"experiment {name} question")
        _text(experiment.get("witness"), f"experiment {name} witness")
        _assignments(experiment.get("focus", {}), choices, f"experiment {name} focus")
        status = experiment.get("status")
        if status not in EXPERIMENT_STATUS:
            raise ModelError(f"experiment {name} needs valid status")
        if status != "proposed" and not experiment.get("evidence_refs"):
            raise ModelError(f"experiment {name} cannot claim results without references")


def load_design(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        doc = json.load(handle)
    validate_design(doc)
    return doc


def resolve_design(doc: dict, *, variant_id: str | None = None,
                   overrides: dict[str, str] | None = None) -> dict:
    """Evaluate a *partial* factor assignment without inventing missing choices.

    Return a legible, machine-readable gap/intersection report; never assert
    an untested combination is feasible merely because components exist.
    """
    validate_design(doc)
    choices = {f["id"]: {o["id"] for o in f["options"]} for f in doc["factors"]}
    selected: dict[str, str] = {}
    if variant_id is not None:
        variant = next((v for v in doc.get("variants", []) if v["id"] == variant_id), None)
        if variant is None:
            raise ModelError(f"unknown design variant {variant_id}")
        selected.update(variant["set"])
    selected.update(_assignments(overrides or {}, choices, "factor overrides"))
    option_by_id = {
        f["id"]: {o["id"]: o for o in f["options"]} for f in doc["factors"]
    }
    selected_options = {}
    for factor, name in selected.items():
        opt = option_by_id[factor][name]
        selected_options[factor] = {
            "option": name, "meaning": opt["meaning"],
            "maturity": opt.get("maturity", "unexamined"),
            "evidence": opt.get("evidence", {"kind": "unknown"}),
        }
    open_factors = [
        {"id": f["id"], "question": f["question"], "relevance": f["relevance"],
         "options": [o["id"] for o in f["options"]]}
        for f in doc["factors"] if f["id"] not in selected
    ]
    intersections = []
    for rule in doc.get("intersections", []):
        if not all(selected.get(k) == v for k, v in rule["when"].items()):
            continue
        missing = {k: v for k, v in rule["requires"].items() if k not in selected}
        disagreed = {k: {"required": v, "selected": selected[k]}
                     for k, v in rule["requires"].items()
                     if k in selected and selected[k] != v}
        intersections.append({
            "id": rule["id"], "strength": rule["strength"],
            "reason": rule["reason"],
            "status": ("conflict" if disagreed and rule["strength"] == "design_contract"
                       else "question" if disagreed or missing else "satisfied_as_assignment"),
            "missing": missing, "disagreed": disagreed,
        })
    relevant_experiments = [
        {"id": e["id"], "question": e["question"], "witness": e["witness"],
         "status": e["status"], "evidence_refs": e.get("evidence_refs", [])}
        for e in doc.get("experiments", [])
        if all(k not in selected or selected[k] == v
               for k, v in e.get("focus", {}).items())
    ]
    conflicts = [x for x in intersections if x["status"] == "conflict"]
    uncertainties = [x for x in intersections if x["status"] == "question"]
    return {
        "design": doc["id"],
        "human_goal": doc["intent"]["goal"],
        "invariants": doc["intent"]["invariants"],
        "variant": variant_id,
        "selected": selected_options,
        "open_factors": open_factors,
        "intersections": intersections,
        "conflicts": conflicts,
        "uncertainties": uncertainties,
        "experiments": relevant_experiments,
        "verdict": "declared_contract_conflict" if conflicts else
                   "incomplete" if open_factors or uncertainties else
                   "candidate_unverified",
        "epistemic_limit": "A consistent factor assignment is not proof of user experience, implementation feasibility or hardware behavior.",
    }


def compare_design(doc: dict) -> list[dict]:
    """Compare only explicitly named candidate assignments, not all products."""
    validate_design(doc)
    return [resolve_design(doc, variant_id=v["id"]) for v in doc.get("variants", [])]


def human_summary(result: dict) -> str:
    lines = [f"DESIGN: {result['design']}",
             f"GOAL: {result['human_goal']}",
             "PRESERVE: " + "; ".join(result["invariants"]),
             f"VERDICT: {result['verdict']} (not runtime verification)"]
    if result["selected"]:
        lines.append("ASSIGNED FACTORS:")
        for factor, option in result["selected"].items():
            lines.append(f"  {factor} = {option['option']} "
                         f"[{option['maturity']}; {option['evidence']['kind']}]")
    if result["open_factors"]:
        lines.append("OPEN FACTORS:")
        for factor in result["open_factors"]:
            lines.append(f"  {factor['id']}: {factor['question']} "
                         f"(why relevant: {factor['relevance']})")
    if result["intersections"]:
        lines.append("FACTOR INTERSECTIONS:")
        for x in result["intersections"]:
            lines.append(f"  {x['id']}: {x['status']} — {x['reason']}")
    if result["experiments"]:
        lines.append("DISCRIMINATING EXPERIMENTS (not automatically run):")
        for e in result["experiments"]:
            lines.append(f"  {e['id']} [{e['status']}]: {e['question']} "
                         f"— witness: {e['witness']}")
    lines.append("LIMIT: " + result["epistemic_limit"])
    return "\n".join(lines)
