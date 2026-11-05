"""CLI for repeatable experiments; stdout is a compact human summary or JSON."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

from .experiments import compare
from .design_space import load_design, resolve_design, compare_design, human_summary
from .model import ModelError, load, set_factor, validate
from .simulation import simulate


def _dump(obj: object, filename: str | None = None) -> None:
    data = json.dumps(obj, indent=2, sort_keys=True) + '\n'
    if filename:
        Path(filename).write_text(data, encoding='utf-8')
    else:
        print(data, end='')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='logical-cloud', description='Simulate factorized split applications')
    commands = parser.add_subparsers(dest='command', required=True)
    sim = commands.add_parser('simulate', help='simulate one resolved case')
    sim.add_argument('scenario')
    sim.add_argument('--set', dest='settings', action='append', default=[], metavar='FACTOR=JSON')
    sim.add_argument('--trace', action='store_true')
    sim.add_argument('--output')
    comp = commands.add_parser('compare', help='run variants x parameter axes')
    comp.add_argument('scenario')
    comp.add_argument('--max-cases', type=int, default=1024)
    comp.add_argument('--trace', action='store_true')
    comp.add_argument('--output', help='full machine-readable JSON results')
    comp.add_argument('--html', help='standalone comparison dashboard with timeline')
    design = commands.add_parser('design',
        help='inspect a human-facing algebraic design space, without running code')
    design.add_argument('scenario', help='domain-independent factor design JSON')
    design.add_argument('--variant', help='named partial candidate assignment')
    design.add_argument('--set', dest='design_settings', action='append', default=[],
                        metavar='FACTOR=OPTION',
                        help='override one named design factor, not an executable expression')
    design.add_argument('--compare', action='store_true',
                        help='inspect explicitly named candidates (not full Cartesian product)')
    design.add_argument('--json', action='store_true',
                        help='emit evidence-qualified report for other agents')
    design.add_argument('--output', help='write machine-readable report to file')
    opts = parser.parse_args(argv)
    try:
        if opts.command == 'design':
            design_doc = load_design(opts.scenario)
            if opts.compare and (opts.variant or opts.design_settings):
                raise ModelError('--compare cannot combine with --variant or --set')
            if opts.compare:
                reports = compare_design(design_doc)
            else:
                overrides = {}
                for assignment in opts.design_settings:
                    if '=' not in assignment:
                        raise ModelError('--set requires FACTOR=OPTION')
                    factor, option = assignment.split('=', 1)
                    if factor in overrides:
                        raise ModelError(f'duplicate factor override {factor}')
                    overrides[factor] = option
                reports = resolve_design(design_doc, variant_id=opts.variant,
                                         overrides=overrides)
            if opts.output or opts.json:
                _dump(reports, opts.output)
            elif isinstance(reports, list):
                for i, item in enumerate(reports):
                    if i:
                        print('\n' + '-' * 36 + '\n')
                    print(human_summary(item))
            else:
                print(human_summary(reports))
            return 0
        scenario = load(opts.scenario)
        if opts.command == 'simulate':
            for setting in opts.settings:
                if '=' not in setting:
                    raise ModelError('--set requires FACTOR=JSON')
                selector, raw_value = setting.split('=', 1)
                try:
                    value = json.loads(raw_value)
                except json.JSONDecodeError as exc:
                    raise ModelError(f'invalid JSON value for {selector}: {exc}') from exc
                set_factor(scenario, selector, value)
            validate(scenario)
            _dump(simulate(scenario, trace=opts.trace), opts.output)
        else:
            cases = compare(scenario, max_cases=opts.max_cases, trace=opts.trace or bool(opts.html))
            if opts.html:
                from .report import render_html
                Path(opts.html).write_text(render_html(cases), encoding='utf-8')
            if opts.output:
                _dump(cases, opts.output)
            else:
                print('name\trequests\tp50_ms\tp95_ms\tnetwork_bytes\tartifact_fetches')
                for case in cases:
                    print(f"{case['name']}\t{case['requests']}\t{case['p50_ms']}\t{case['p95_ms']}\t"
                          f"{case['network_bytes_total']}\t{case['counters'].get('artifact_fetches', 0)}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'logical-cloud: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
