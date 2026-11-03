import copy
import json
import unittest
from pathlib import Path

from logical_cloud import ModelError, compare, load, set_factor, simulate, validate
from logical_cloud.model import digest, variants
from logical_cloud.report import render_html


ROOT = Path(__file__).resolve().parents[1]


def tiny():
    return {
        'schema_version': 1,
        'application': {
            'artifacts': [{'id': 'code', 'bytes': 100, 'home': 'client'}],
            'stages': [{'id': 'work', 'artifact': 'code', 'deps': [], 'work_units': 10,
                        'input_bytes': 100, 'output_bytes': 50}]},
        'fabric': {
            'devices': [
                {'id': 'client', 'speed': 1, 'slots': 1, 'cache_bytes': 0},
                {'id': 'worker', 'speed': 1, 'slots': 1, 'cache_bytes': 100},
            ],
            'links': [{'id': 'wire', 'a': 'client', 'b': 'worker', 'latency_ms': 1,
                       'bandwidth_bytes_per_ms': 10}]},
        'demand': {'requester': 'client', 'arrivals_ms': [0, 100]},
        'placement': {'work': 'worker'},
    }


class SimulationTests(unittest.TestCase):
    def test_first_request_streams_code_then_warm_cache(self):
        result = simulate(tiny(), trace=True)
        self.assertEqual(result['latencies_ms'], [38, 27])
        self.assertEqual(result['network_bytes_total'], 400)
        self.assertEqual(result['counters']['artifact_fetches'], 1)
        self.assertEqual(result['counters']['cache_hits'], 1)
        self.assertEqual(result['tasks_by_device'], {'worker': 2})
        self.assertEqual([e['at_ms'] for e in result['trace']],
                         sorted(e['at_ms'] for e in result['trace']))

    def test_tiny_cache_forces_every_code_fetch(self):
        s = tiny()
        set_factor(s, 'device.worker.cache_bytes', 99)
        result = simulate(s)
        self.assertEqual(result['latencies_ms'], [38, 38])
        self.assertEqual(result['counters']['artifact_fetches'], 2)
        self.assertEqual(result['network_bytes_total'], 500)

    def test_location_independence_of_graph_and_no_network_if_local(self):
        s = tiny()
        semantics_before = digest(s['application'])
        set_factor(s, 'placement.work', 'client')
        result = simulate(s)
        self.assertEqual(result['latencies_ms'], [10, 10])
        self.assertEqual(result['network_bytes_total'], 0)
        self.assertEqual(result['application_sha256'], semantics_before)

    def test_cpu_queue_and_slots(self):
        s = tiny()
        s['placement']['work'] = 'client'
        s['application']['stages'][0]['input_bytes'] = 0
        s['application']['stages'][0]['output_bytes'] = 0
        s['demand']['arrivals_ms'] = [0, 0]
        self.assertEqual(simulate(s)['latencies_ms'], [10, 20])
        s['fabric']['devices'][0]['slots'] = 2
        self.assertEqual(simulate(s)['latencies_ms'], [10, 10])

    def test_inflight_code_fetch_shared(self):
        s = tiny()
        s['demand']['arrivals_ms'] = [0, 0]
        r = simulate(s)
        self.assertEqual(r['counters']['artifact_fetches'], 1)
        self.assertEqual(r['counters']['inflight_joins'], 1)
        self.assertEqual(r['latencies_ms'], [47, 57])  # competing input uploads serialize before code fetch

    def test_two_hops(self):
        s = tiny()
        s['fabric']['devices'].append({'id': 'middle', 'speed': 1, 'slots': 1, 'cache_bytes': 0})
        s['fabric']['links'] = [
            {'id': 'a', 'a': 'client', 'b': 'middle', 'latency_ms': 1, 'bandwidth_bytes_per_ms': 10},
            {'id': 'b', 'a': 'middle', 'b': 'worker', 'latency_ms': 2, 'bandwidth_bytes_per_ms': 10},
        ]
        s['demand']['arrivals_ms'] = [0]
        r = simulate(s)
        self.assertEqual(r['network_bytes_by_link'], {'a': 250, 'b': 250})
        self.assertEqual(r['latencies_ms'], [69])  # 23 input + 23 code + 10 CPU + 13 result

    def test_factorial_experiment_and_semantic_identity(self):
        s = tiny()
        s['variants'] = [
            {'id': 'local', 'set': {'placement.work': 'client'}},
            {'id': 'remote', 'set': {'placement.work': 'worker'}},
        ]
        s['axes'] = {'link.wire.latency_ms': [1, 10], 'device.worker.speed': [1, 2]}
        results = compare(s)
        self.assertEqual(len(results), 8)
        self.assertEqual(len({r['application_sha256'] for r in results}), 1)
        self.assertEqual(len({r['scenario_sha256'] for r in results}), 8)
        with self.assertRaisesRegex(ModelError, 'limit'):
            list(variants(s, max_cases=7))

    def test_invalid_factors_and_cycles_are_explicit(self):
        s = tiny()
        with self.assertRaisesRegex(ModelError, 'unsupported'):
            set_factor(s, 'device.worker.run_shell', 'oops')
        with self.assertRaisesRegex(ModelError, 'unknown device'):
            set_factor(s, 'placement.work', 'moon')
            validate(s)
        s = tiny()
        s['application']['stages'][0]['deps'] = ['work']
        with self.assertRaises(ModelError):
            validate(s)
        s = tiny()
        s['fabric']['links'] = []
        with self.assertRaisesRegex(ModelError, 'no network path'):
            simulate(s)
        s['placement']['work'] = 'client'
        self.assertEqual(simulate(s)['network_bytes_total'], 0)

    def test_determinism_and_html_escapes_names(self):
        s = tiny()
        self.assertEqual(simulate(s, trace=True), simulate(copy.deepcopy(s), trace=True))
        r = simulate(s, trace=True)
        r['name'] = '</script><script>alert(1)</script>'
        html = render_html([r])
        self.assertNotIn('</script><script>alert(1)</script>', html)
        self.assertIn('application', json.dumps(s))

    def test_example_runs_six_controlled_cases(self):
        s = load(ROOT / 'examples/split_camera.json')
        cases = compare(s, trace=True)
        self.assertEqual(len(cases), 6)
        for case in cases:
            self.assertEqual(case['requests'], 5)
            self.assertEqual(len(case['latencies_ms']), 5)
            self.assertTrue(case['trace'])
        self.assertEqual(len({c['application_sha256'] for c in cases}), 1)


if __name__ == '__main__':
    unittest.main()
