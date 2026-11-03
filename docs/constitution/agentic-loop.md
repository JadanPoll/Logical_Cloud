# The near-real-time agentic development loop

**Constitutional basis:** LC-01, LC-05 through LC-12. This is a desired workflow and set of decision rules, not a claim that voice-driven remote deployment is already built.

## North-star demonstration

A user is holding a phone while an application is running on a television, desktop, or another device. They speak:

> “The pause controls disappear too quickly on the TV. Make them easier to use with this remote. Try a couple of layouts.”

The phone transcribes the request and sends it to an available agentic compute machine. The agent retrieves **Player / Overlay**, **Input / Remote**, and **Visual Style** intent sets and the relevant interfaces. It does not scan the whole project, rebuild unrelated services, or require the user to copy source code to the target device.

It preserves the existing playback contract; prepares two genuinely different UI proposals under the same behavior; exercises plausible remote-key flows; and returns an observable preview or accurate failure report. The user can say, “I like the second one, but make it less tall.” Only the affected factors need re-evaluation.

The build host, runtime device, and artifact storage may be different machines. That is the **substrate's responsibility**, subject to authorization and actual capability, not a repeated instruction burden placed on the user.

**Success is the whole experience:** the utterance reaches an agent, relevant context is recovered, useful alternatives appear, a chosen version can be applied or reverted, and a new agent can later understand what happened without another full interview.

## The operational loop

**1. Orient.** Interpret the question; identify larger intent and constraints. A short correction to an existing request should reuse its unresolved scope rather than begin a new project description.

**2. Activate.** Retrieve the smallest applicable intent-set neighborhood, authoritative factors, previous relevant decisions, and source anchors. Admit unknown constraints.

**3. Factor.** State the intended single-variable or limited-variable substitution. Prefer an existing mechanism or solved precedent over inventing a new subsystem.

**4. Vary.** Produce one useful candidate quickly; create competing hypotheses or variants where the decision genuinely benefits from comparison. Let unpromising branches die cheaply without destroying their history.

**5. Observe.** Present incremental visible feedback, bounded checks, targeted simulation, or direct device evidence according to the risk. Show why the result differs, not only whether a job was green.

**6. Critique.** Compare against the actual user goal and current baseline. Reconsider the problem representation when the experiment fails to answer the question. Give the human an easy path to steer, reject, or refine.

**7. Promote or resume.** A proposal remains a proposal until authorized promotion. Preserve a concise trace of variant factors, evidence, decision, and unresolved limitations so the next agent can continue.

This is a revisitable **ring**, not a strict seven-step ceremony. A trivial typography adjustment may jump straight from activation to preview; a surprising failure may move back to orientation.

## Five concurrent agents are normal, not exceptional

Suppose one agent changes a domain behavior, a second changes the shared visual theme, a third prepares localization, a fourth adapts TV remote interaction, and a fifth explores execution placement. They should share a **common application intent and versioned contracts**, while each modifies its own factor and produces observable evidence.

The orchestration question is not “how can all five edit the same checkout without conflict?” but “how can each change exist as a named candidate and how cheaply can valid combinations be formed?”

- **Independent obligations:** preserve each agent's candidate; compose or test combinations at meaningful intersections.
- **Shared contract changed:** route the issue to its owner or make the conflict explicit; do not silently rebalance semantics across all workers.
- **Failed or delayed worker:** keep unrelated previews and experiments usable.
- **Competing proposals:** retain alternatives for comparison; decide what to promote independently.
- **New agent arrives:** give it relevant certificates and recoverable evidence, not a giant reconstructed transcript.

A central coordinator should manage *dependencies and meaningful decisions*, not require every independent agent to wait for periodic global consensus.

## Self-play: where the intelligence is spent

REM's self-play insight is not “make agents generate more code.” It is a tight feedback loop between data, response, a reasoner, and the human as meta-reasoner and goal director. The valuable work is forming and revising questions, creating informative variations, finding shortcomings, and noticing when the model or goal is wrong.

Static jobs—building, propagating stable factor definitions, enumerating admissible combinations, retrieving context, producing comparisons, and recording provenance—should increasingly run without requiring fresh semantic reasoning. Agent reasoning can then focus on high-value decisions. Do not mistake a higher number of trials for higher information gain.

Self-play can include automated adversarial or boundary exploration, but its simulation outputs must retain their assumptions. A real mobile-device input or human usability observation has a different epistemic status from a synthetic model.

## GitHub Actions as evidence and repeatability

For a change proposal, CI can independently examine the proposed scope, exercise informative invariants and representative flows, and publish comparison artifacts. The best routine is **cheap checks first**, with expensive environments activated when the changed behavior actually needs them.

GitHub Actions is not the application runtime, not a universal evaluator, and not automatic authorization to deploy. Build output should be easy for another agent or a human to inspect. No branch naming convention or boilerplate report should be allowed to become the core product.

Where feasible, expose a user-friendly **what is happening** timeline with optional copyable details. Do not trap the user behind irrelevant validation steps or silent retries.

## Failure interpretation and stopping decisions

When an attempt fails, distinguish:

- **The experiment failed:** the proposed implementation does not meet the intended obligation; correct or try another candidate.
- **The model failed:** the simulated or assumed conditions are unlike actual device behavior; calibrate or observe.
- **The question failed:** the modification does not advance the larger user goal; revisit the intent.
- **The orchestration failed:** files, dependencies, authority, or timing made a reasonable request cumbersome; fix the substrate rather than making the user repeat work.

Stop an experiment when its expected value falls below its cost, a better path is evident, or an authoritative constraint prevents safe advancement. Retain the user-visible next useful action. Never convert internal bookkeeping into a hostage state.
