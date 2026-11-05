# Logical Cloud

**Logical Cloud is the executable software-and-engineering realization of the
general ideas explored in REM, RSM and FKEN.** The Navigationals material
develops philosophies about identifying holistic goals, routing among
reasoning operations, recovering knowledge, and avoiding locally brilliant
but globally unhelpful work. Logical Cloud asks the next question:
**what should the actual human/agent interface, functional contracts,
agent-to-agent coordination, coding process, tools, runtime, evidence and
revision machinery look like so those ideas work in real software projects?**

The end-to-end aspiration is **software development at the speed of human
intention**: a person communicates a big-picture idea in text or voice;
a high-level agent turns it into intelligible sub-goals and meaningful
choices; specialist agents use modular contracts and inspected precedents;
actual code and tools produce early inspectable candidates; and the person
can revise one preference, keep the project, or recruit another agent
without reconstructing the engineering.

**Three human-facing levels:** (1) general/holistic idea; (2) revisable
functional intent organized as sets and supersets; (3) actual
implementation decisions, code, source-grounded references and evidence.
A human can ask "why A instead of B?" at any level without needing
to administer the technical workflow.

Start with the [full vision-to-execution stack](docs/vision-to-execution-stack.md),
[Constitution](CONSTITUTION.md), [intent-set doctrine](docs/constitution/intent-sets.md),
and [agent entrypoint](AGENTS.md). The constitution's
[numbered axiom calculus](docs/constitution/axiom-calculus.md) distinguishes
rule compliance from outcome success, and its
[research-style provenance](docs/constitution/provenance.md) links
decisions to actual inspected implementations.

**Current implementation status:** This repository implements a
deterministic distributed-execution simulator, CLI, tests and offline
comparison reports. The full voice/text-to-agent-to-code/tool/runtime
development loop is a *specified objective*, not an existing feature.
The simulator is one component of this ambition, not the project itself.

---

## Existing implementation — placement simulator

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

**Current cross-project execution case:** [Fire Console's first Playroom,
portability lookup, and ungraded Android Dojo slice](docs/cases/fire-first-slice-2026-11-04.md).
It records actual GitHub source/tool actions and bounded checks while separating
an agent-queryable route from a real physical-TV result. This is an early
exercise of the constitution, not a finished orchestration runtime.

## Next milestones

Prioritize **one end-to-end user-directed development slice** before adding
new general-purpose orchestration machinery. Each milestone is an observable
acceptance flow, not merely a document:

1. **Human vision → interpreted and revisable intent:** a text/voice
   request yields a concise holistic goal, critical sub-goals, a small
   set of meaningful alternative experiences when warranted, and an
   editable selected interpretation that persists into the next request.
2. **Intent → real agent/tool action → useful preview:** an agent
   navigates the relevant factor and inspected source precedents, makes
   a scoped code change with an existing tool, checks the cheapest
   realistic user flow, and returns an inspectable artifact with honest
   evidence and a clear revision path.
3. **Continuation and independent agents:** another agent can recover
   accepted intent, variants, code, reasons and evidence without
   re-interviewing the human; independent work need not wait for
   unrelated implementation details.
4. **Placement and distributed runtime:** calibrate the existing simulator
   against real traces, implement a trusted local executor with resumable
   events, then selectively test moving a compatible worker to another
   device while preserving the functional contract.

See the [vision-to-execution stack](docs/vision-to-execution-stack.md)
for the full contract and [acceptance cases](docs/constitution/acceptance.md)
for the success/failure criteria. Do not confuse specifying a capability
with having implemented it.
