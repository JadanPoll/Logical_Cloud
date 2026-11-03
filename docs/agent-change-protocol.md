# Agent-generated changes, many versions, and A/B evaluation

A modern agent should be able to change one application's behavior without also knowing which particular device stores it, how it is delivered, or how to deploy unrelated modules. Many competing versions should coexist without destructive replacement.

## Four independently identified entities

1. **Logical application contract:** typed graph, supported effects, constraints, and test fixtures. Placement changes must not change this contract.
2. **Implementation version:** immutable artifact/dependency digest; different code with the same interface still gets a distinct implementation identity.
3. **Execution plan:** placement, requested resources, caching and transport options; can change without modifying implementation.
4. **Rollout experiment:** populations, randomization key, allocation ratios, metrics, budget, abort criteria, parent baseline, approval, and replayable evidence.

`ApplicationContract × ImplementationVersion × ExecutionPlan × ExperimentPolicy → DeploymentCandidate`

Do not represent all of these as one mutable `version` string or a copied directory. A/B correctness requires consistent randomization or shadow replay, confidence intervals, and explicit incompatibility detection when versions change semantics. Simulation covers **estimated performance under assumptions**; it is not proof that a changed program behaves correctly.

## Agent request lifecycle (proposed, not yet automated)

A user says "make the TV's pause overlay larger." The system identifies a component and creates a typed proposal such as:

```json
{
  "intent": "larger playback overlay",
  "target": "player.controls.overlay",
  "base_revision": "git-commit-sha",
  "allowed_files": ["apps/player/overlay.*"],
  "constraints": ["do not change playback logic", "retain remote-control navigation"],
  "tests": ["overlay-rendering", "remote-dpad-interaction"],
  "rollout": "proposal-only"
}
```

A future agent uses this to make a small branch/PR rather than touching unrelated components. GitHub Actions checks the allowed diff, lint/static compatibility, unit tests, the simulator's invariants and applicable real-device smoke tests. Store evidence and a provenance digest. Users can request additional A/B variants without overwriting accepted ones. Promotion, staged rollout, and rollback are separate operations with their own permissions.

For a new placement suggestion ("run detector on the edge"), an agent can already change one variable in a scenario and use the simulator:

```bash
python -m logical_cloud simulate examples/split_camera.json --set placement.detect='"edge"' --trace
python -m logical_cloud compare examples/split_camera.json --html experiment.html
```

## GitHub Actions security and stability

- The initial workflow tests pull requests with only **read** repository permission. It does not use a deployment secret, `pull_request_target`, self-hosted device runners, or writable checkout credentials.
- A future agent proposer must not merge itself into production based only on its own tests. Changes that introduce device access or modify a security boundary require explicit review.
- Experimental changes should be cheap to abandon. Add a version and its measured consequences; avoid tearing down old versions to "simplify" the system.
- Keep test costs bounded. Use fast invariant checks and targeted end-to-end smoke cases on PRs; reserve wide experiments and costly hardware suites for meaningful decisions.
- CI for adversarial forks is untrusted code: never expose device access or private network credentials to those jobs.

## Next concrete work

1. Define stage input/output schemas and a no-ambient-authority capability envelope.
2. Implement a real local runner and append-only event stream with resume cursors.
3. Add versioned artifact build metadata and hash checking, then remote execution over a controlled transport.
4. Calibrate simulator from real traces; add regression budgets for CPU, latency, network traffic and privacy.
5. Add canary/shadow traffic and a branch/PR bot that translates natural-language requests into narrowly factored change sets.
