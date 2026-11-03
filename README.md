# Logical Cloud

**Build an application once; factor out where code, data, and computation happen.**

Logical Cloud explores a world in which the distinction between *local*, *remote device*, and *cloud* stops being an application-level burden. Code should be delivered lazily, execution can happen on a different device, and an interface should subscribe to its results as naturally as it plays a video stream.

The project is **simulation-first**. This repository currently includes a functioning deterministic simulator and an offline experiment explorer. **It does not yet execute code remotely, synchronize real files, provide sandboxing, or offer live migration.** Those are future runtime milestones; see [architecture](docs/architecture.md) and [agent change protocol](docs/agent-change-protocol.md).

## The algebra

An application is a graph of typed work stages and immutable artifact references. Its *placement* is a separate variable:

`Outcome = Simulate(Application, Fabric, Placement, Demand, ArtifactCache)`

`Experiment = Variant × Axis₁ × Axis₂ × …`

Substituting `placement.detect = cloud` does **not** require rewriting `detect` or cloning an app. The graph and its application digest remain identical. Variants carry **explicit, small factor changes**, making agent-generated changes easy to inspect, combine, evaluate, and revert. This is the starting point for algebraic software design, not a claim that arbitrary side-effecting code is automatically location-transparent.

## Run it

Requires Python 3.10+, standard library only:

```bash
python -m unittest discover -s tests -v
python -m logical_cloud compare examples/split_camera.json
python -m logical_cloud compare examples/split_camera.json --html experiment.html --output experiment.json
python -m logical_cloud simulate examples/split_camera.json --set placement.detect='"cloud"' --trace
```

Open `experiment.html` in a browser to compare outcomes and see **where each invocation's code and computation moves among devices**. No server, credentials, pip install, or cloud account is necessary.

## Example: change one factor, not the application

The [camera workload](examples/split_camera.json) defines capture → detect → overlay. The same graph is tested with detection on a television, edge computer, or cloud host. A network-latency axis doubles the experiment set to six cases:

```json
"variants": [
  {"id": "all-local", "set": {"placement.detect": "tv"}},
  {"id": "edge-inference", "set": {"placement.detect": "edge"}},
  {"id": "cloud-inference", "set": {"placement.detect": "cloud"}}
],
"axes": {"link.lan.latency_ms": [3, 15]}
```

This is **not** a claim that these machines actually take those times. Their work and bandwidth coefficients are synthetic, chosen to exercise the model. A real placement controller will need to calibrate them from measurements on actual devices and networks.

## Simulator contract (v0.1)

- **Application:** a DAG of stages with dependencies, normalized `work_units`, entry/exit payload sizes, and referenced code artifacts.
- **Devices:** compute throughput (`speed` in work units/ms), FIFO CPU slots, and a bounded LRU artifact cache.
- **Links:** directed traffic over bidirectional, independently serialized lanes; latency in ms and bandwidth in bytes/ms. Multi-hop paths use store-and-forward forwarding and shortest uncongested estimated transfer time.
- **Demand:** a requesting device and an ordered list of invocation start times.
- **Placement:** each stage maps to a device. An artifact is fetched from its `home` when needed and cached if space permits; duplicate in-flight fetches are coalesced.
- **Outcomes:** per-request latency, p50/p95, per-link transferred bytes, CPU busy time/utilization, cache statistics, hashes of model and application, and an optional timestamped event trace.

**Known limitations:** no actual network I/O, retries, failures, bandwidth fairness, streaming of partial stage outputs, state consistency, variable runtime distributions, memory pressure, GPU modeling, device energy pricing, or authentication. The simulator models each stage as a whole task. It does not currently validate semantic equivalence of *different code implementations*—only keep the same workload definition when evaluating placement changes.

## Agent and GitHub Actions workflow

The [CI workflow](.github/workflows/ci.yml) validates simulator invariants and publishes a standalone experiment report with every PR. It has `contents: read`, and does **not** deploy or run arbitrary user-supplied code on private devices. The intended future assistant/voice path is:

**Intent → typed change set → isolated branch → targeted tests + simulation → comparison report → explicit promotion → rollout/rollback.**

See [agent change protocol](docs/agent-change-protocol.md) for why code variants, execution policies, deployments, and rollout approvals need distinct identities. The original unrelated README is preserved at [docs/legacy-original-readme.md](docs/legacy-original-readme.md).

## Next milestones

1. **Calibrate simulation** against measured device throughput, artifact loading, cache hit rates, network links, and startup costs; model real request distributions and failure modes.
2. **Minimal real executor:** a trusted local runner using a typed stage interface plus an ordered, resumable execution-result stream. Add a remote runner only after authority/capability boundaries and content-address verification are in place.
3. **Agent experiments:** reproducible A/B report artifacts, correctness contracts, version identities, canary/shadow traffic, and promotion/rollback policies. Later: a natural-language/voice frontend, not coupled to the core runtime.

Do not conflate simulating remote execution with having implemented it.
