# The near-real-time agentic development loop

**Constitutional basis:** LC-01, LC-05 through LC-12, LC-16. This is a desired workflow and set of decision rules, not a claim that voice-driven remote deployment is already built.

## North-star demonstration

A user is holding a phone while an application is running on a television, desktop, or another device. They speak:

> “The pause controls disappear too quickly on the TV. Make them easier to use with this remote. Try a couple of layouts.”

The phone transcribes the request and sends it to an available agentic compute machine. The agent retrieves **Player / Overlay**, **Input / Remote**, and **Visual Style** intent sets and the relevant interfaces. It does not scan the whole project, rebuild unrelated services, or require the user to copy source code to the target device.

It preserves the existing playback contract; prepares two genuinely different UI proposals under the same behavior; exercises plausible remote-key flows; and returns an observable preview or accurate failure report. The user can say, “I like the second one, but make it less tall.” Only the affected factors need re-evaluation.

The build host, runtime device, and artifact storage may be different machines. That is the **substrate's responsibility**, subject to authorization and actual capability, not a repeated instruction burden placed on the user.

**Success is the whole experience:** the utterance reaches an agent, relevant context is recovered, useful alternatives appear, a chosen version can be applied or reverted, and a new agent can later understand what happened without another full interview.

## Human vision and high-level interpretation

The user may supply nothing more than an ambitious, informal vision over
text or voice. Their central contribution is to express the **big-picture
and holistic goals**, refine a few consequential preferences, and judge
useful experiences—not specify the Android, network, source-tree, or test
mechanics. The agents take responsibility for implementation and routine
uncertainty (LC-16).

When the vision has materially different plausible meanings, the high-level
agent offers two or three **contrasting interpretations of the outcome**,
briefly naming their tradeoffs and proposing an initial default. The user
can reply "second, but keep the first one's navigation"; the selection
becomes a named, reversible intent/variant constraint and the agents proceed.
Do not turn straightforward requests into multiple-choice homework. A
cheap preview may be more informative than a question.

A representative interaction:

> **Human:** "I want a Wii-like console where I can make and explore apps
> entirely from my TV or iPad."
>
> **High-level agent:** "Do you prefer (A) an app launcher with a separate
> build workspace, (B) a unified create-and-preview console, or (C) a
> lightweight launcher that delegates development to remote agents?
> I can start with C while preserving the path to B."
>
> **Human:** "C for now; make it easy to turn into B."
>
> **Agents:** Preserve that purpose, factor launcher, agent coordination,
> build/preview and deployment interfaces, research relevant established
> implementations, and return an inspectable candidate. A new worker
> retrieves the concise *why/promise/boundary* for its class of functions,
> plus source-pinned implementation rationale and evidence, rather than
> asking the human to repeat this history.

This is an **illustrative desired flow**, not a claim that Logical Cloud
already implements a voice coordinator or all of these capabilities.
Outstanding low-level implementation and compositional uncertainty should
normally remain with the responsible agents. A human decision is requested
only when it meaningfully changes the vision, preference, or authority.
Scale agents up or down while keeping the same named intent and sources of
truth; record variants and decisions, not full conversational transcripts.

## Recursive vision clarification: the high-level agent's main job

Before delegating into file-level tasks, identify (1) the **holistic reason**
the person wants this system and (2) the few **critical sub-big-pictures**
that together make that ambition meaningful. For each sub-goal, separate
the person's expressed intention from the agent's provisional interpretation.
If an important outcome is ambiguous, offer two or three clear, contrasting
*experiences* the person could mean, with an optional recommendation and
"none of these / here's what I meant" as a normal response. The human can
select or mix interpretations in one phrase.

Clarification is **recursive but conditional**: descend into a sub-question
only if a choice there would substantially change the final experience,
priority or authorization. Otherwise agents select reasonable reversible
implementations, present working previews, and iterate. Never recursively
expand an entire hypothetical decision tree just to demonstrate diligence.

Then return a compact **shared understanding**: "Here is the holistic goal
I understood; here are its critical sub-goals; here is what I take each to
mean; here is the sensible path; here is what the first and eventual result
should feel like." Invite a short correction, not formal sign-off. The
initial milestone is that the human **recognizes their vague idea as
faithfully specified**, not that they understand the engineering or that
implementation is already complete. A clearly understood vision and an
actually verified result are distinct kinds of evidence.

Example: the person imagines an open-ended Fire TV console, where they can
play ambitious games, ask for persistent playable prototypes that family
members enjoy, investigate low-level Android behavior, and treat offshore
Compute as an extension of the TV. The high-level agent should recognize
**play**, **imagine/create/iterate**, **inspect/learn**, and **compute
elsewhere** as related but substitutable sub-big-pictures. It might offer
different interpretations of "ambitious games" (play existing games, build
original ones, or both) without asking the person to choose between Gradle,
Godot or Android's input APIs. It should leave unresolved options open,
propose an intelligible first end-to-end experience, and own the technical
work after alignment. This is an example of the intended method, not a
claim of implemented autonomous game creation.

A new agent should recover this concise decomposition, selected/rejected
interpretations and the underlying intent certificates with selective,
version-pinned research references. It should not need a complete transcript
of the conversation or another interview with the person. See LC-16.07–16.10.

## The operational loop

**1. Orient.** Interpret the question; identify larger intent and constraints. A short correction to an existing request should reuse its unresolved scope rather than begin a new project description.

**2. Activate.** Retrieve the smallest applicable intent-set neighborhood, authoritative factors, previous relevant decisions, and source anchors. Admit unknown constraints.

**3. Check precedents.** Read the owning set's implementation annotations and version-pinned source precedents, especially real GitHub implementations and tests; do not overwrite source-backed decisions because a different framework is more familiar from training.

**4. Factor.** State the intended single-variable or limited-variable substitution. Prefer an existing mechanism or solved precedent over inventing a new subsystem.

**5. Vary.** Produce one useful candidate quickly; create competing hypotheses or variants where the decision genuinely benefits from comparison. Let unpromising branches die cheaply without destroying their history.

**6. Observe.** Present incremental visible feedback, bounded checks, targeted simulation, or direct device evidence according to the risk. Show why the result differs, not only whether a job was green.

**7. Critique.** Compare against the actual user goal and current baseline. Reconsider the problem representation when the experiment fails to answer the question. Give the human an easy path to steer, reject, or refine.

**8. Certify, promote or resume.** Include the narrow material numbered constitutional clauses, source references, and a qualified statement of evidence; distinguish whether the method was followed from whether it achieved the intended result. A proposal remains a proposal until authorized promotion. Preserve a concise trace of variant factors, inspected source precedents, applicable numbered clauses, evidence, decision, and unresolved limitations so the next agent can continue.

This is a revisitable **ring**, not a strict eight-step ceremony. A trivial typography adjustment may jump straight from activation to preview; a surprising failure may move back to orientation.

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


## Constitution-aware self-play

Each meaningful iteration can update **two hypotheses** independently: a hypothesis about the software, and a hypothesis about whether the governing `LC-XX.Y` clause is sufficient under the current situation. A failure should therefore be traced in the [axiom calculus](axiom-calculus.md), with enough source-anchored evidence to distinguish a violated rule, a faithfully followed but inadequate rule, an incorrect model, and undetermined claims. Useful outcomes include a fix, a rejected variant, a narrow new exception, or an amendment supported by a concrete counterexample.

This is not a demand for agents to endlessly justify themselves. Small cited decisions and reproducible differences are sufficient in ordinary work; only consequential disputes need deeper audits. Preserve old code/reasons before changing it, and do not require the human to referee preference disagreements between models.
