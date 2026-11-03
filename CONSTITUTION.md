# Logical Cloud — Constitution for Agentic Software Evolution

**Status:** Foundational direction, version 0.1. This governs future development decisions; it is not a claim that the platform already realizes them. Read the [intent-set doctrine](docs/constitution/intent-sets.md), [agentic development loop](docs/constitution/agentic-loop.md), and [acceptance cases](docs/constitution/acceptance.md) when relevant.

## Preamble — the problem we are actually solving

“Build anything” makes producing a first version cheap; maintaining, modifying, porting, comparing, and coordinating many evolving versions can remain disproportionately expensive. Agents repeatedly rediscover what an application does, propagate the same change through unrelated files, rebuild their context after interruptions, and collide with other agents. A user asking for a small alteration can inadvertently initiate a large engineering project.

**Our asymptotic goal is software change at the speed of intention.** A person speaks into a phone; an agent running on an available compute machine interprets the request against a recoverable project intent; independently modifies the relevant factors; explores alternatives; and returns a working, inspectable result for a chosen device or form factor. The user need not manage where the source, build, code artifacts, or expensive computation reside.

The project is about **agentic software architecture and the development process**. Location-independent code and execution are among its applications, not the whole thesis. This constitution samples relevant ideas from REM, RSM, and FKEN without copying their full research machinery into every software project.

The articles below are *operational principles*, not a ceremonial checklist. Invoke a principle when it addresses a real difficulty. Explain departures when they materially affect the goal.

## LC-01 — Preserve the problem, not the accidental solution

**LC-01.01 Purpose before mechanism.** Interpret the user's request in terms of the experience or capability sought. A spoken example may denote a *class* of changes, not a literal implementation prescription. Recover the unstated larger objective before proposing substantial restructuring.

**LC-01.02 Respect existing work.** Before replacing a component, discover why it exists and what obligations it currently fulfills. A strange implementation may embody a constraint absent from current documentation. No agent may treat novelty as sufficient reason to delete working behavior.

**LC-01.03 Optimize the complete path.** The relevant unit of efficiency is: intention → correct scope → experiment → working preview → evaluation → deployment → future modification. Improving only code-generation speed while multiplying integration, comprehension, or regression cost is not an improvement.

## LC-02 — Factor by independently meaningful substitutions

**LC-02.01 Algebraic principle.** Represent choices that vary independently as named substitutable factors. Application semantics, domain logic, UI style, localization, form-factor adaptation, device capabilities, execution placement, persistence, and deployment policy must not be entangled without a reason.

**LC-02.02 The change-surface test.** A factor is well chosen when changing one meaningful concern usually changes one authoritative definition plus only the truly necessary integration boundaries. If “make all buttons larger” requires editing dozens of screens, the abstraction has failed—however nicely the files are arranged.

**LC-02.03 No false universality.** Different form factors and devices may require distinct layouts, interactions, or accessibility strategies. Factor shared **meaning** and variation rules; do not pretend one exact UI implementation fits every surface.

**LC-02.04 Factorization has a price.** Do not split a stable, one-off detail into a forest of indirections. Introduce a factor when it reduces expected future reasoning, modification, or coordination cost. Remove redundant layers as their purpose disappears.

**LC-02.05 Composition must be legible.** An agent should be able to say what factor is being substituted, which other factors are held fixed, and which interactions require evaluation. Local substitutability is a hypothesis, not an exemption from integration checks.

## LC-03 — Documentation sets certify intent

**LC-03.01 Intent hierarchy.** Each consequential group of responsibilities should be reachable through concise, nested **intent sets**: project purpose → capability families → related function groups → leaves where useful. “External devices” can contain “camera,” which can contain “capture”; related concerns may belong to several sets.

**LC-03.02 A certificate says what, not how.** An intent-set certificate briefly states why the group exists, what observable promise it makes, what must remain invariant, what it relies on or exposes, and material exclusions or unknowns. It must **not** duplicate source code, paraphrase every function, or invent correctness evidence.

**LC-03.03 Hierarchies are navigational.** Agents retrieve a small pertinent slice: the parent purpose, the directly implicated set, and consequential dependencies or intersecting policies. A phone-overlay edit should not require re-reading the camera driver, cloud fabric, or every language string.

**LC-03.04 Certificates and tests are different.** An intent certificate records the intended obligation. It does not certify that an implementation fulfills it. Claims of verified behavior require traceable observations, tests, or other evidence.

**LC-03.05 Stop at useful boundaries.** Do not recursively document a leaf whose behavior is already apparent from its stable interface. Refine only when the current abstraction cannot answer an important modification or integration question. See [intent sets](docs/constitution/intent-sets.md).

## LC-04 — Make cross-cutting concerns genuinely independent

**LC-04.01 Style.** Shared design language—semantic tokens, typography roles, spacing, emphasis, accessibility states—should be factored independently from the business behaviors it presents. Local exceptions remain possible and discoverable.

**LC-04.02 Localization.** Text, terminology, formatting rules, directionality, and linguistic variants should be authoritatively substitutable without cloning application behavior. Translation is not merely replacing strings: pluralization, length, meaning, and layout remain real obligations.

**LC-04.03 Form factor and input.** Phone, TV, desktop, embedded screen, touch, remote, keyboard, accessibility input, and future surfaces should be considered **adapters to common capabilities**, not necessarily separate applications. Factor the intent of navigation and actions separately from how the device affords them.

**LC-04.04 Versioned variation.** Store competing visual, linguistic, interaction, and algorithmic ideas as variants with a common referent, not unrelated forks whose differences become impossible to reconstruct.

## LC-05 — Let agents work independently without making people integrators

**LC-05.01 Parallelism is a first-class use case.** Five agents may concurrently change appearance, language, interaction, computation placement, and a domain feature. No agent should need the entire repository in active context just to safely progress its own task.

**LC-05.02 Stable contracts over coordination meetings.** Independence comes from shared intent, explicit boundaries, meaningful interfaces, and localized checks—not from asking agents to synchronize on every small edit.

**LC-05.03 Convergence is conditional.** Disjoint changes that preserve their shared obligations should compose cheaply. When two agents change an overlapping contract or a shared invariant, surface a precise conflict and its consequences; do not automatically declare both versions compatible.

**LC-05.04 Alternatives are assets.** Preserve useful independent proposals, baselines, and results. A/B variants are not mistakes to be prematurely collapsed into one “best” version. Reversibility and comparison are part of the architecture.

**LC-05.05 Protect human intent.** Agents may independently investigate, modify proposals, and generate previews; they may not silently reinterpret a high-level request as authority to delete data, weaken security, publish externally, or deploy a consequential change.

## LC-06 — Self-play is the development engine

**LC-06.01 Tighten the loop.** The essential loop is: question or request → hypothesis → minimally scoped variation → observable result → critique → next variation. The agent and its tools should automate static chores while human attention stays on goals, surprises, and meaningful choices.

**LC-06.02 Human as goal director.** The person may steer the experiment in near real time, without being forced to operate a build system or resolve every intermediate bookkeeping state. Short voice utterances and corrective follow-ups are legitimate primary interfaces.

**LC-06.03 Deliberately create variance.** Investigate meaningfully different candidates, not a dozen cosmetic restatements. Use counterexamples and questions about the abstraction itself to avoid optimizing a misconceived objective.

**LC-06.04 Self-play needs reality checks.** Repeated simulation can refine decisions *under the model*; it cannot establish that the model matches a physical device or human preference. Label conjecture, simulation, observed behavior, and accepted decisions separately.

**LC-06.05 Stop and switch methods.** Continue only while the next experiment's expected useful learning or improvement justifies its cost. If evidence suggests a mistaken question, abstraction, or premise, revise it rather than endlessly polishing the current variant.

## LC-07 — Context recovery is infrastructure, not individual agent heroics

**LC-07.01 Minimum sufficient context.** An agent should receive or retrieve the smallest navigable set of intent certificates, contracts, precedents, and source regions needed for its specific question. Entire repository dumps are not a substitute for architecture.

**LC-07.02 Reconstructability.** Significant experiments and decisions should leave recoverable pointers: originating intent, factor changes, baseline, evidence, limits, and current status. A new agent should resume without oral history.

**LC-07.03 Source of truth.** Prefer one authoritative location for each stable rule and lightweight links from consumers. Avoid maintaining duplicated descriptions that must all be edited to remain consistent.

**LC-07.04 Question-conditioned navigation.** Use the current change request to activate relevant documents and dependencies. Do not materialize every potential relationship, add endless metadata, or require constant context reviews.

## LC-08 — Compute and device location are replaceable constraints

**LC-08.01 Logical rather than fictional transparency.** Applications should express outcomes and required capabilities. The substrate should manage reasonable placement of code, data, and execution where feasible, while acknowledging latency, hardware access, trust, power, persistence, and failure.

**LC-08.02 No ambient authority.** Remote access to a camera, microphone, files, secrets, or a device is not implied by saying a function can run elsewhere. Authority should follow explicit, scoped, revocable permissions.

**LC-08.03 Device independence supports agent independence.** A remote agentic computer should be able to build and propose an update to a phone or TV without requiring its own code editor or LLM runtime to reside on the target device.

**LC-08.04 Placement is not application meaning.** Moving a compatible stage between local and remote workers should not require rewriting its user-facing contract. Where behavior changes under placement, expose it explicitly and test the relevant boundary.

## LC-09 — Prefer visible experiments to opinions about architecture

**LC-09.01 Factorial experiments.** A candidate can vary implementation, style, locale, form factor, placement, network conditions, or demand independently when appropriate. Preserve baseline and factor deltas; do not copy entire applications for every test.

**LC-09.02 Simulate to compare, observe to validate.** Use reproducible models to explore plausible consequences and discover sensitive interactions. Calibrate against real user flows and measurements before asserting performance or user-experience gains.

**LC-09.03 Optimize a landscape, not a single metric.** Perceived latency, correctness, accessibility, bandwidth, battery, privacy, context cost, integration friction, and future modifiability can conflict. Disclose tradeoffs rather than disguising them with a single score.

**LC-09.04 Risk-weighted exploration.** Cheap changes may merit immediate previews; consequential effects deserve stronger evidence. Spend the test budget where a failure would actually undermine the user's purpose.

## LC-10 — The entire experience must stay legible and unblocked

**LC-10.01 Act at the level of intent.** The system absorbs messy lower-level mechanics without hiding meaningful outcomes. Do not make the user become the workflow's engineer.

**LC-10.02 Show what is happening.** A request should produce an intelligible progress path, an early useful preview when possible, and copyable diagnostic evidence when something fails. Invisible waiting and generic “retry” screens are defects in the interaction.

**LC-10.03 No hostage workflows.** A stale test report, failed optional experiment, or unresolved side branch should not ordinarily block a new unrelated request or a fresh start. Distinguish actual safety or correctness dependencies from avoidable procedural gates.

**LC-10.04 Continuous, reversible improvement.** A small correction should not cost a full reorientation. Make current results immediately inspectable; allow cancellation, comparison, correction, and rollback at the level of user intentions.

## LC-11 — GitHub Actions and other automation serve fast feedback

**LC-11.01 Verification follows scope.** An agent should run the cheapest credible checks for the changed obligations, escalating to integration, simulated, hardware, or human review only when warranted.

**LC-11.02 Independent evidence.** A builder's claims are not its own certification. GitHub Actions can produce externally inspectable check results, comparison artifacts, and provenance; green CI is bounded evidence, not universal assurance.

**LC-11.03 Proposal is distinct from promotion.** A voice request may create a proposal and test candidates quickly. Publishing, device updates, permission changes, destructive actions, and production rollout require appropriate authority and clear reversibility.

**LC-11.04 Keep the pipeline out of the way.** CI must not become a ritual that burns resources on vacuous tests while preventing rapid experimentation. Use realistic flows, informative failures, selective validation, and tight feedback loops.

## LC-12 — Measure the right kind of speed

**LC-12.01 Primary signal.** Track *time from understandable request to first meaningful, inspectable candidate*, and to an accepted update—not merely generation tokens or wall-clock build time.

**LC-12.02 Hidden costs count.** Track repeated context reconstruction, number of authoritative locations edited, human coordination, conflicts, regressions, test cost, deployment friction, and ability to resume after interruption.

**LC-12.03 Compositional efficiency.** A system can be locally fast but globally awkward. Judge it on sequences of changes across independent factors and agents, not a polished single demo.

**LC-12.04 Do not manufacture precision.** Qualitative comparison is legitimate where numbers are poorly grounded. Report uncertainty and distinguish the hoped-for asymptote from the current implementation.

## LC-13 — The constitution must itself remain engineerable

**LC-13.01 Stable addresses.** Clause identifiers are references to intentions. Do not silently reuse a clause ID for a different proposition; supersede or qualify it when necessary.

**LC-13.02 Amend through cases.** Add or revise doctrine because a real workflow exposed a failure, missing distinction, or better abstraction. Preserve the motivating case, decision, and remaining uncertainty without requiring excessive ceremony.

**LC-13.03 Anti-bureaucracy clause.** This constitution must reduce the work required to modify software. If applying a rule creates more friction than the failure it prevents, challenge the rule and retain a simpler sufficient path.

**LC-13.04 No completion theater.** A certificate is not an implementation, a simulation is not a measurement, a PR is not a deployed product, and an agent's confidence is not verification. Make the state of each claim explicit.

---

## How to use this constitution

**Human or voice user:** express the desired effect; optionally name the target form factor, constraints, or preferred variant. You need not know implementation files, build machines, or transports.

**Agent beginning a change:** recover the big-picture intent; navigate only relevant intent sets; identify the factorizable change surface; propose the smallest meaningful variation; obtain bounded evidence; return an inspectable result and uncertainties. See [agentic loop](docs/constitution/agentic-loop.md).

**Architect modifying the platform:** demonstrate why the new mechanism earns its complexity against actual workflows. See [acceptance cases](docs/constitution/acceptance.md).

**Provenance:** these principles are a selective, project-specific synthesis of [REM, RSM and FKEN](docs/constitution/sources.md). Their source specifications remain independent and authoritative for their own domains.
