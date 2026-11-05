# Logical Cloud architecture — factor the problem before distributing it

**Scope:** This document specifies the execution/fabric factors of
Logical Cloud, not the whole project. The broader architecture begins
with a person's holistic vision and functional intent, and continues
through research-grounded decisions, agent delegation, real code/tool
work, evidence and revision. See the
[human-to-execution stack](vision-to-execution-stack.md). The placement
simulator is an existing executable *slice* of that stack.

## Desired developer experience

An application says **what** should happen. The substrate decides **where and when**, within declared cost, capability, quality, privacy, and latency constraints. A local widget and a remote widget present the same logical interface. The system exposes observable execution telemetry, not a maze of configuration tasks.

The difficult problem is *not* sending a Python function to a different machine. It is preserving a useful contract while factoring out artifact distribution, execution placement, state, effects, permissions, and upgrades. Treating those dimensions as independent algebraic parameters limits how many details an agent must change to improve a UI or swap a backend.

## Algebraic boundaries

For an idealized pure stage:

`Stage[artifact, interface, version] : Input → Output`

For real applications:

`Stage : (Input, StateRef, CapabilitySet) → (Output, StateDelta, Events)`

Placement and transport should be independent of stage semantics:

`Plan = Place(ApplicationGraph, DeviceFabric, Demand, Constraints)`

`Run = Execute(Plan, ArtifactStore, StateService, EventTransport)`

A stage requiring a camera does not magically obtain remote camera access. It receives a **scoped capability** (for example `camera.frames@device-tv`), and the system chooses whether to move code toward it or stream data to another device. Secrets, stateful side effects, untrusted code, and non-idempotent operations require explicit boundaries. We should optimize for *logical* location-independence, not assert physical transparency where it is impossible.

### Separate substitutable modules

| Term | Stable contract | Replaceable implementations |
|---|---|---|
| Application | typed stage graph, versioned interfaces and effects | UI/native/WASM/runtime-specific adapters |
| Artifact | immutable content digest, dependencies, availability | local disk, peer cache, registry, object store |
| Placement | `stage → executor` with constraints | manual, heuristics, planner, trained policy |
| Executor | isolated stage invocation + lifecycle/events | local process, sandbox, peer, remote worker |
| Transport | ordered streams, backpressure, checkpoints | IPC, WebSocket, QUIC, WebRTC |
| State | snapshots + revision/merge semantics | local durable store, sync engine, CRDT where appropriate |
| Experiment | immutable baseline + named factor overrides | exhaustive sweep, adaptive search, canary rollout |
| Policy | authority, budgets, privacy, trust | developer rules, owner rules, organizational governance |

Avoid universal interfaces that hide radically different costs. Track remote byte counts, cold-start cost, battery and CPU budgets, and why a policy chose a placement. Expose local/remote status without forcing every UI component to care about it.

## Streaming is two related but separate paths

**Code/artifact stream:** immutable named chunks fetched on demand and verified against a digest. Caches can share and deduplicate chunks. Artifact distribution should not be confused with arbitrary remote code execution. The simulator currently uses a *size of code artifact*, not the code bytes or hash verification.

**Execution-result stream:** invocations produce ordered events and occasional state snapshots. A subscriber should be able to resume from sequence number *N*, apply exactly-once effects only where provable, and detect a stale revision. Proposed envelope:

```json
{
  "schema": 1,
  "application": "sha256:...",
  "invocation": "request-uuid",
  "sequence": 17,
  "stage": "detect",
  "kind": "output|progress|checkpoint|error|completed",
  "payload_ref": "sha256:...",
  "state_revision": "revision-or-null"
}
```

This is a **target contract**, not a presently implemented protocol. Keep payload references immutable and ensure event sequencing remains tied to an invocation. Support backpressure, cancellation, idempotency keys, and reconnects before promising video-like reliability.

## Simulator ↔ runtime

The simulator is a replaceable model of this execution structure. Its Python package is intentionally standard-library only, with pure scenario inputs and machine-readable outputs. It currently simulates full-stage data transfers, network serialization, non-preemptive CPU queueing, code-fetch coalescing and LRU caching. The stage graph is validated to be acyclic. Every invocation logs a trace when requested.

Model evolution should preserve comparative usefulness:

- Add measured throughput and latency distributions rather than inventing hardware accuracy.
- Add memory, cold process startup, GPU classes, energy/thermal limits, endpoint trust and device availability.
- Add preemption and backpressure; partial result streaming and pipelining matter to perceived latency.
- Simulate stale replicas, consistency strategies, failures, retries, and cross-region cost.
- Replay traces from *real* executions through the same dashboard, distinguishing `observed` from `simulated` in the data schema.

For multi-criteria optimization use a **Pareto frontier** over p95, throughput, bytes, money, battery, correctness and privacy constraints, rather than blindly minimizing one number. Correctness and authority are hard constraints, not performance dimensions to trade away.

## Stopping rules / completion boundaries

- **Simulation complete enough** when empirical workloads reproduce both good and pathological placement patterns within measured uncertainty, and the model clearly discloses blind spots.
- **Single-machine executor complete enough** when a real stage runs twice against the same immutable artifact, emits independently replayable ordered events, and survives subscriber reconnects without lost events.
- **Remote execution complete enough** when the *same* staged application can switch between local and remote execution without a UI rewrite, with scoped authority, immutable artifact verification, timeouts, cancellation, and trustworthy rollback.
- **Agentic change flow complete enough** when a tiny spoken change maps to a localized code diff, reproducible checks, a comprehensible A/B outcome, and explicit promotion. No implicit production writes from the voice request.

## Precedent worth studying

- **Nix**: derivations and isolated immutable store paths as inspiration for multi-version artifacts; do not copy its complexity into every application.
- **Ray / distributed task systems**: remote scheduling, resource-aware execution, failure handling and object stores.
- **SimPy / discrete-event simulation**: resource queueing and event progression. This minimal simulator uses a handwritten event queue to avoid dependency setup.
- **GitHub Actions**: PR-triggered reusable validation and artifacts. Deployment permissions stay separate.
- **Video streaming systems**: adaptive chunks, startup latency, caching and client buffering; execution streams additionally require state and side-effect semantics.

The factorization itself is the valuable deliverable: application authors see stable names and logical interfaces, while the backend owns the messy substitution mechanism.
