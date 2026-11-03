"""Deterministic discrete-event model of split applications and code streaming.

Assumptions: CPU FIFO slots; full-duplex FIFO links, store-and-forward hops;
immutable artifacts with bounded per-device LRU cache; no failures, congestion
control, OS scheduling, encryption overhead, or live executors in this model.
"""
from __future__ import annotations

from collections import OrderedDict, defaultdict, deque
import heapq
from itertools import count
from typing import Any, Callable

from .model import ModelError, digest, validate


class Simulator:
    def __init__(self, scenario: dict, trace: bool = False):
        validate(scenario)
        self.scenario = scenario
        self.devices = {x['id']: x for x in scenario['fabric']['devices']}
        self.links = {x['id']: x for x in scenario['fabric']['links']}
        self.stages = {x['id']: x for x in scenario['application']['stages']}
        self.artifacts = {x['id']: x for x in scenario['application']['artifacts']}
        self.placement = scenario['placement']
        self.requester = scenario['demand']['requester']
        self.arrivals = scenario['demand']['arrivals_ms']
        self.dependents: dict[str, list[str]] = defaultdict(list)
        for stage in self.stages.values():
            for dep in stage['deps']:
                self.dependents[dep].append(stage['id'])
        self.terminals = [sid for sid in self.stages if not self.dependents[sid]]
        self.queue: list[tuple[float, int, Callable, tuple]] = []
        self.sequence = count()
        self.now = 0.0
        self.want_trace = trace
        self.trace: list[dict] = []
        self.device_queues = {dev: deque() for dev in self.devices}
        self.running = defaultdict(int)
        self.link_free: dict[tuple[str, str, str], float] = defaultdict(float)
        self.cache: dict[str, OrderedDict[str, int]] = {dev: OrderedDict() for dev in self.devices}
        self.cache_used = defaultdict(int)
        self.inflight: dict[tuple[str, str], list[Callable]] = {}
        self.pending: dict[tuple[int, str], int] = {}
        self.request_done_pending = {i: len(self.terminals) for i in range(len(self.arrivals))}
        self.request_finish: dict[int, float] = {}
        self.busy_ms = defaultdict(float)
        self.link_bytes = defaultdict(int)
        self.stats = defaultdict(int)
        self.stage_exec = defaultdict(int)
        self.transfer_id = count()

    def emit(self, event: str, **details: Any) -> None:
        if self.want_trace:
            self.trace.append({'at_ms': round(self.now, 6), 'event': event, **details})

    def schedule(self, at_ms: float, fn: Callable, *args: Any) -> None:
        if at_ms < self.now - 1e-8:
            raise AssertionError('attempted to schedule an event in the past')
        heapq.heappush(self.queue, (at_ms, next(self.sequence), fn, args))

    def route(self, source: str, destination: str, size: int) -> list[tuple[str, str, dict]]:
        """Shortest uncongested serialization+propagation path for this payload size."""
        if source == destination or size == 0:
            return []
        q: list[tuple[float, str]] = [(0.0, source)]
        distance = {source: 0.0}
        previous: dict[str, tuple[str, dict]] = {}
        while q:
            cost, node = heapq.heappop(q)
            if cost > distance[node] + 1e-10:
                continue
            if node == destination:
                break
            for link in self.links.values():
                peer = link['b'] if link['a'] == node else link['a'] if link['b'] == node else None
                if peer is None:
                    continue
                new = cost + link['latency_ms'] + size / link['bandwidth_bytes_per_ms']
                if new < distance.get(peer, float('inf')) - 1e-10:
                    distance[peer] = new
                    previous[peer] = (node, link)
                    heapq.heappush(q, (new, peer))
        if destination not in previous:
            raise ModelError(f'no network path for {source} -> {destination} ({size} bytes)')
        path = []
        current = destination
        while current != source:
            prior, link = previous[current]
            path.append((prior, current, link))
            current = prior
        return path[::-1]

    def send(self, source: str, destination: str, size: int, kind: str, callback: Callable, **meta: Any) -> None:
        if source == destination or size == 0:
            self.schedule(self.now, callback)
            return
        path = self.route(source, destination, size)
        transfer = next(self.transfer_id)
        self.stats['transfers'] += 1
        self.emit('transfer_requested', transfer=transfer, source=source, destination=destination,
                  bytes=size, kind=kind, **meta)
        self.schedule(self.now, self._hop, transfer, path, 0, size, kind, callback, meta)

    def _hop(self, tid: int, path: list, index: int, size: int, kind: str,
             callback: Callable, meta: dict) -> None:
        if index == len(path):
            self.emit('transfer_arrived', transfer=tid, kind=kind, **meta)
            callback()
            return
        source, dest, link = path[index]
        lane = (link['id'], source, dest)  # full-duplex; each direction has an independent sender
        tx_start = max(self.now, self.link_free[lane])
        serial_ms = size / link['bandwidth_bytes_per_ms']
        self.link_free[lane] = tx_start + serial_ms
        self.link_bytes[link['id']] += size
        self.stats['link_hops'] += 1
        self.emit('hop_queued', transfer=tid, link=link['id'], source=source, destination=dest,
                  bytes=size, transmit_at_ms=round(tx_start, 6), kind=kind, **meta)
        self.schedule(tx_start + serial_ms + link['latency_ms'], self._hop, tid,
                      path, index + 1, size, kind, callback, meta)

    def ensure_artifact(self, device: str, artifact_id: str, callback: Callable) -> None:
        artifact = self.artifacts[artifact_id]
        if artifact['home'] == device or artifact['bytes'] == 0:
            self.stats['artifact_home_hits'] += 1
            self.schedule(self.now, callback)
            return
        cache = self.cache[device]
        if artifact_id in cache:
            self.stats['cache_hits'] += 1
            cache.move_to_end(artifact_id)
            self.emit('cache_hit', device=device, artifact=artifact_id)
            self.schedule(self.now, callback)
            return
        key = (device, artifact_id)
        if key in self.inflight:
            self.stats['inflight_joins'] += 1
            self.inflight[key].append(callback)
            return
        self.stats['cache_misses'] += 1
        self.stats['artifact_fetches'] += 1
        self.inflight[key] = [callback]
        self.send(artifact['home'], device, artifact['bytes'], 'code',
                  lambda: self._artifact_arrived(device, artifact_id), artifact=artifact_id)

    def _artifact_arrived(self, device: str, artifact_id: str) -> None:
        artifact = self.artifacts[artifact_id]
        amount = artifact['bytes']
        cap = self.devices[device]['cache_bytes']
        cache = self.cache[device]
        if amount <= cap:
            while self.cache_used[device] + amount > cap:
                _, evicted_size = cache.popitem(last=False)
                self.cache_used[device] -= evicted_size
                self.stats['cache_evictions'] += 1
            cache[artifact_id] = amount
            self.cache_used[device] += amount
        waiters = self.inflight.pop((device, artifact_id))
        self.emit('code_available', device=device, artifact=artifact_id, waiters=len(waiters))
        for callback in waiters:
            self.schedule(self.now, callback)

    def start_request(self, number: int) -> None:
        self.emit('request', invocation=number, requester=self.requester)
        for sid, stage in self.stages.items():
            if stage['deps']:
                self.pending[(number, sid)] = len(stage['deps'])
            else:
                self.pending[(number, sid)] = 1 if stage['input_bytes'] else 0
        for sid, stage in self.stages.items():
            if stage['deps']:
                continue
            if not stage['input_bytes']:
                self.schedule(self.now, self.ready, number, sid)
            else:
                self.send(self.requester, self.placement[sid], stage['input_bytes'], 'input',
                          lambda n=number, s=sid: self.data_arrived(n, s), invocation=number, stage=sid)

    def data_arrived(self, number: int, sid: str) -> None:
        key = (number, sid)
        self.pending[key] -= 1
        if self.pending[key] < 0:
            raise AssertionError(f'duplicate input for {key}')
        if self.pending[key] == 0:
            self.schedule(self.now, self.ready, number, sid)

    def ready(self, number: int, sid: str) -> None:
        stage = self.stages[sid]
        device = self.placement[sid]
        self.ensure_artifact(device, stage['artifact'],
                             lambda n=number, s=sid, d=device: self.enqueue(n, s, d))

    def enqueue(self, number: int, sid: str, device: str) -> None:
        self.device_queues[device].append((number, sid))
        self.emit('stage_queued', invocation=number, stage=sid, device=device)
        self.pump(device)

    def pump(self, device: str) -> None:
        queue = self.device_queues[device]
        slots = self.devices[device]['slots']
        while queue and self.running[device] < slots:
            number, sid = queue.popleft()
            work = self.stages[sid]['work_units'] / self.devices[device]['speed']
            self.running[device] += 1
            self.busy_ms[device] += work
            self.stage_exec[device] += 1
            self.emit('stage_started', invocation=number, stage=sid, device=device,
                      estimated_compute_ms=round(work, 6))
            self.schedule(self.now + work, self.complete_stage, number, sid, device)

    def complete_stage(self, number: int, sid: str, device: str) -> None:
        self.running[device] -= 1
        self.emit('stage_completed', invocation=number, stage=sid, device=device)
        output = self.stages[sid]['output_bytes']
        for consumer in self.dependents[sid]:
            self.send(device, self.placement[consumer], output, 'data',
                      lambda n=number, s=consumer: self.data_arrived(n, s),
                      invocation=number, producer=sid, consumer=consumer)
        if sid in self.terminals:
            self.send(device, self.requester, output, 'result',
                      lambda n=number: self.result_arrived(n), invocation=number, stage=sid)
        self.pump(device)

    def result_arrived(self, number: int) -> None:
        self.request_done_pending[number] -= 1
        if self.request_done_pending[number] == 0:
            self.request_finish[number] = self.now
            self.emit('request_completed', invocation=number)

    def run(self) -> dict:
        for i, at in enumerate(self.arrivals):
            self.schedule(at, self.start_request, i)
        while self.queue:
            self.now, _, fn, args = heapq.heappop(self.queue)
            fn(*args)
        if len(self.request_finish) != len(self.arrivals):
            raise AssertionError('some invocations did not complete')
        latencies = [self.request_finish[i] - at for i, at in enumerate(self.arrivals)]
        latency_sorted = sorted(latencies)
        def pct(p: float) -> float:
            index = (len(latency_sorted) - 1) * p
            lo, hi = int(index), min(int(index) + 1, len(latency_sorted) - 1)
            return latency_sorted[lo] + (latency_sorted[hi] - latency_sorted[lo]) * (index - lo)
        horizon = self.now - self.arrivals[0]
        return {
            'scenario_sha256': digest(self.scenario),
            'application_sha256': digest(self.scenario['application']),
            'requests': len(self.arrivals),
            'latencies_ms': [round(x, 6) for x in latencies],
            'p50_ms': round(pct(0.5), 6),
            'p95_ms': round(pct(0.95), 6),
            'mean_ms': round(sum(latencies) / len(latencies), 6),
            'makespan_ms': round(horizon, 6),
            'network_bytes_by_link': dict(sorted(self.link_bytes.items())),
            'network_bytes_total': sum(self.link_bytes.values()),
            'cpu_busy_ms_by_device': {k: round(self.busy_ms[k], 6) for k in sorted(self.devices)},
            'cpu_utilization_by_device': {k: round(self.busy_ms[k] / (horizon * d['slots']), 6) if horizon else 0
                                          for k, d in sorted(self.devices.items())},
            'tasks_by_device': dict(sorted(self.stage_exec.items())),
            'counters': dict(sorted(self.stats.items())),
            'trace': self.trace if self.want_trace else [],
        }


def simulate(scenario: dict, *, trace: bool = False) -> dict:
    return Simulator(scenario, trace=trace).run()
