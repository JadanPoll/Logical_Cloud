"""Schema validation and factor substitution. Pure inputs; no runtime side effects."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from typing import Any, Iterator


class ModelError(ValueError):
    """Invalid scenario or factor."""


def digest(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def load(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        scenario = json.load(handle)
    validate(scenario)
    return scenario


def _number(value: Any, label: str, *, positive: bool = False) -> None:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ModelError(f"{label} must be numeric")
    if not (float('-inf') < value < float('inf')) or (value <= 0 if positive else value < 0):
        raise ModelError(f"{label} must be {'positive' if positive else 'nonnegative'} and finite")


def _unique(entries: list[dict], label: str, *, allow_empty: bool = False) -> dict[str, dict]:
    if not isinstance(entries, list) or (not entries and not allow_empty):
        raise ModelError(f"{label} must be a nonempty list")
    out: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get('id'), str) or not entry['id']:
            raise ModelError(f"{label} entries require nonempty string id")
        if entry['id'] in out:
            raise ModelError(f"duplicate {label} id: {entry['id']}")
        out[entry['id']] = entry
    return out


def validate(scenario: dict) -> None:
    """Validate every factor before simulation; fail explicitly rather than infer."""
    if not isinstance(scenario, dict) or scenario.get('schema_version') != 1:
        raise ModelError('schema_version must be 1')
    try:
        app, fabric, demand, placement = (scenario[k] for k in ('application', 'fabric', 'demand', 'placement'))
        artifacts = _unique(app['artifacts'], 'artifacts')
        stages = _unique(app['stages'], 'stages')
        devices = _unique(fabric['devices'], 'devices')
        links = _unique(fabric['links'], 'links', allow_empty=True)
        arrivals = demand['arrivals_ms']
        requester = demand['requester']
    except (KeyError, TypeError) as exc:
        raise ModelError(f'missing or malformed scenario field: {exc}') from exc
    if not isinstance(placement, dict) or set(placement) != set(stages):
        raise ModelError('placement must assign every stage exactly once')
    if requester not in devices:
        raise ModelError(f'unknown requester device {requester}')
    if not isinstance(arrivals, list) or not arrivals:
        raise ModelError('demand.arrivals_ms must be a nonempty list')
    for i, at in enumerate(arrivals):
        _number(at, f'arrivals_ms[{i}]')
    if arrivals != sorted(arrivals):
        raise ModelError('arrival times must be ascending')
    for dev in devices.values():
        _number(dev.get('speed'), f"device {dev['id']} speed", positive=True)
        if type(dev.get('slots')) is not int or dev['slots'] < 1:
            raise ModelError(f"device {dev['id']} slots must be positive integer")
        if type(dev.get('cache_bytes')) is not int or dev['cache_bytes'] < 0:
            raise ModelError(f"device {dev['id']} cache_bytes must be nonnegative integer")
    for link in links.values():
        if link.get('a') not in devices or link.get('b') not in devices or link['a'] == link['b']:
            raise ModelError(f"link {link['id']} must connect distinct existing devices")
        _number(link.get('latency_ms'), f"link {link['id']} latency_ms")
        _number(link.get('bandwidth_bytes_per_ms'), f"link {link['id']} bandwidth_bytes_per_ms", positive=True)
    for artifact in artifacts.values():
        if type(artifact.get('bytes')) is not int or artifact['bytes'] < 0:
            raise ModelError(f"artifact {artifact['id']} bytes must be nonnegative integer")
        if artifact.get('home') not in devices:
            raise ModelError(f"artifact {artifact['id']} has unknown home")
    for stage in stages.values():
        if stage.get('artifact') not in artifacts:
            raise ModelError(f"stage {stage['id']} has unknown artifact")
        if not isinstance(stage.get('deps'), list) or any(not isinstance(x, str) for x in stage['deps']) or len(set(stage['deps'])) != len(stage['deps']):
            raise ModelError(f"stage {stage['id']} deps must be a unique list")
        if stage['id'] in stage['deps'] or any(dep not in stages for dep in stage['deps']):
            raise ModelError(f"stage {stage['id']} has invalid dependency")
        _number(stage.get('work_units'), f"stage {stage['id']} work_units")
        for field in ('input_bytes', 'output_bytes'):
            if type(stage.get(field)) is not int or stage[field] < 0:
                raise ModelError(f"stage {stage['id']} {field} must be nonnegative integer")
        if placement[stage['id']] not in devices:
            raise ModelError(f"stage {stage['id']} placed on unknown device {placement[stage['id']]}")
    visiting: set[str] = set()
    done: set[str] = set()
    def walk(node: str) -> None:
        if node in visiting:
            raise ModelError(f'cyclic application graph near {node}')
        if node in done:
            return
        visiting.add(node)
        for dep in stages[node]['deps']:
            walk(dep)
        visiting.remove(node)
        done.add(node)
    for stage_id in stages:
        walk(stage_id)
    if not any(not stage['deps'] for stage in stages.values()):
        raise ModelError('application must contain a root stage')


def set_factor(scenario: dict, selector: str, value: Any) -> None:
    """Edit a *named* factor, never arbitrary JSON paths or executable code."""
    parts = selector.split('.')
    if len(parts) == 2 and parts[0] == 'placement':
        if parts[1] not in scenario['placement']:
            raise ModelError(f'unknown stage for {selector}')
        scenario['placement'][parts[1]] = value
    elif len(parts) == 3 and parts[0] in ('device', 'link', 'stage', 'artifact'):
        kind, name, prop = parts
        definitions = {'device': ('fabric','devices', {'speed','slots','cache_bytes'}),
                       'link': ('fabric','links', {'latency_ms','bandwidth_bytes_per_ms'}),
                       'stage': ('application','stages', {'work_units','input_bytes','output_bytes'}),
                       'artifact': ('application','artifacts', {'bytes'})}
        section, collection, allowed = definitions[kind]
        if prop not in allowed:
            raise ModelError(f'unsupported factor selector {selector}')
        entry = next((x for x in scenario[section][collection] if x['id'] == name), None)
        if entry is None:
            raise ModelError(f'unknown factor {selector}')
        entry[prop] = value
    else:
        raise ModelError(f'unsupported factor selector {selector}')


def variants(scenario: dict, *, max_cases: int = 1024) -> Iterator[tuple[str, dict, dict]]:
    """Cartesian product of named alternatives and independent axes."""
    alternatives = scenario.get('variants', [{'id': 'baseline', 'set': {}}])
    axes = scenario.get('axes', {})
    if not isinstance(alternatives, list) or not alternatives:
        raise ModelError('variants must be a nonempty list')
    if not isinstance(axes, dict):
        raise ModelError('axes must be an object')
    labels = list(axes)
    for selector, values in axes.items():
        if not isinstance(values, list) or not values:
            raise ModelError(f'axis {selector} must contain values')
    count = len(alternatives)
    for values in axes.values():
        count *= len(values)
    if count > max_cases:
        raise ModelError(f'experiment has {count} cases; limit is {max_cases}')
    ids: set[str] = set()
    for alternative in alternatives:
        if not isinstance(alternative, dict) or not isinstance(alternative.get('id'), str) or not alternative['id']:
            raise ModelError('each variant must have a nonempty id')
        name = alternative['id']
        if name in ids:
            raise ModelError(f'duplicate variant id {name}')
        ids.add(name)
        changes = alternative.get('set', {})
        if not isinstance(changes, dict):
            raise ModelError(f'variant {name} set must be an object')
        for values in product(*(axes[label] for label in labels)):
            case = deepcopy(scenario)
            # Experiment metadata is not part of the system being simulated.
            case.pop('axes', None)
            case.pop('variants', None)
            factors = dict(changes)
            factors.update(zip(labels, values))
            for selector, value in factors.items():
                set_factor(case, selector, value)
            validate(case)
            case_name = name + ''.join(f'|{key}={json.dumps(value, separators=(",", ":"))}' for key, value in zip(labels, values))
            yield case_name, case, factors
