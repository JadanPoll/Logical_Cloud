"""Factorial A/B experiments share one application definition."""
from __future__ import annotations
from .model import variants
from .simulation import simulate


def compare(scenario: dict, *, max_cases: int = 1024, trace: bool = False) -> list[dict]:
    results = []
    for name, case, factors in variants(scenario, max_cases=max_cases):
        result = simulate(case, trace=trace)
        results.append({'name': name, 'factors': factors, 'placement': case['placement'].copy(), **result})
    return results
