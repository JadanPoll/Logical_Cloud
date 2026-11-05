# Acceptance cases: evaluate the architecture by what changes become easy

These cases are **requirements for future systems**, not statements about current implementation. Use them to reject locally sophisticated architectures that fail the actual agentic-development objective. Adapt their representative workloads as real applications become available.

## A. Voice-to-preview across machines — the north star

**Starting point:** an existing moderately complex application is running on one device; the user has only a phone and a voice interface; an agent's available compute runs elsewhere.

**Request:** “On the TV, make the pause controls stay visible longer and give me two styles.”

**What success looks like:** the agent identifies the right intent sets and variation points, preserves playback semantics, produces useful previews or a precise blocker, and allows the user to revise one proposal without restating the project. Neither source location nor build-host identity must be memorized by the user.

**Failure signatures:** asking which file controls the overlay; copying a full application for each style; touching unrelated camera/network code; hiding a failed build; requiring manual propagation to the TV; forcing a new request because one optional test failed.

## B. Localization as a substitution, not a rewrite

**Starting point:** an application already has menus, settings, overlays, and user-facing errors.

**Request:** “Let me try the application in Spanish, then German; don't change the behavior.”

**What success looks like:** a shared semantic locale factor governs appropriate language and format changes. Real composition boundaries—longer strings, plural forms, layout direction where relevant, missing translations—are exposed and checked selectively. The English baseline remains available.

**Failure signatures:** copied application trees, dozens of unrelated UI edits, silent fallback presented as complete translation, or a global language constant that cannot represent context.

## C. Advanced application, new form factor

**Starting point:** a usable desktop application with domain behavior, persistent work, and a known set of actions.

**Request:** “Give me a television version navigable with the remote; keep the same work and core capabilities.”

**What success looks like:** the agent reuses domain semantics and user-work continuity while adapting navigation, density, input, and display. It identifies genuinely device-specific limitations rather than claiming pixel-perfect equivalence. The variant can coexist with the desktop form.

**Failure signatures:** reimplementing domain logic for TV, forcing pointer-style interaction, copying all UI files, or treating impossibility of one hardware capability as failure of the entire application.

## D. Independent work by five agents

**Starting point:** an existing application, stable intent hierarchy, and five independently assigned improvements: appearance, locale, remote input, domain behavior, and compute placement.

**What success looks like:** each agent recovers bounded context, produces a named candidate, and retains useful results while others work. Combinations are checked at consequential intersections. Shared-contract conflicts are precise and negotiable; unrelated work does not stop.

**Failure signatures:** serializing all work behind a monolithic shared context; merge conflicts in identical copied style strings; erasing alternative candidates; accepting incompatible changes because they touched different files.

## E. Repeated real-time corrections, not one-shot generation

**Starting point:** case A has yielded a usable preview.

**Requests:** “Keep version two.” Then: “Make the text more compact.” Then: “Actually keep the old navigation.”

**What success looks like:** each request applies to a comprehensible named baseline or variant, with localized changes and cheap rollback. A newly connected agent can resume the conversation's *project state* from persistent references and evidence.

**Failure signatures:** full repository restudy for each utterance; nondeterministic loss of the selected variant; changing playback logic to adjust typography; rebuilding unrelated services before every preview.

## F. Remote execution without lying about physics

**Starting point:** a computational stage can run on a nearby or distant worker, while a device-specific input remains on the target.

**Request:** “Use that other computer for the heavy part without changing how I use the application.”

**What success looks like:** unchanged logical purpose where capabilities permit, explicit scoped data access, observable performance/traffic, and a recoverable fallback. A simulator can compare placements, but observed results are distinguished from predictions.

**Failure signatures:** assuming the remote worker owns the camera, hiding privacy costs, presenting synthetic latency as measured, or requiring the application UI to hard-code the worker address.

## G. Resume without historical reconstruction

**Starting point:** the original agent is gone and the project has accumulated variants, accepted changes, and abandoned experiments.

**Request:** “Continue the TV overlay work; why did we choose layout B?”

**What success looks like:** a new agent retrieves the relevant intent sets, the accepted candidate and alternatives, the motivating request, real evidence, and unresolved uncertainty without retrieving unrelated development history.

**Failure signatures:** explanations only available from an enormous chat log, duplicate contradictory documentation, claims of verification without evidence, or no way to identify which version is on the device.

## H. Agents disagree because of differing training-derived conventions

**Starting point:** a working camera/display subsystem has a brief intent hierarchy, a code reference at a pinned commit, a local adaptation, and known checks. A new agent prefers another design.

**Request:** “Improve responsiveness without breaking the existing camera behavior.”

**Success:** The agent recovers the relevant `LC-XX.Y` clauses and existing source-backed design, identifies a specific failing obligation, and compares an actually inspected alternative or a local counterexample. It records which claims were upstream-observed vs locally verified. If the proposal is merely a preference, it preserves the baseline rather than performing an unnecessary rewrite.

**Failure:** an unreferenced new implementation; an invented source; vague “industry standard” justification; past citations treated as infallible; or a complete rewrite solely because it matches the new agent's learned conventions.

## I. A rule-following agent fails: inspect the constitution

**Starting point:** an agent examines a pinned upstream theme implementation, factors a TV overlay's styling, runs applicable checks, and truthfully labels its preview as simulated.

**Observed failure:** On a real Fire TV remote, an unusual key-up event makes focus disappear. The requested UX is still unsatisfactory.

**Success:** Audit the relevant material clauses: `LC-02.02` (factor), `LC-14.01` (precedent), `LC-09.02` (simulation evidence), `LC-04.03` (form-factor input), and `LC-15.04–15.07` (compliance vs outcome, failure, amendment). Mark each **supported/violated/undetermined/not applicable** using independent evidence. Determine if this is an implementation defect, an omitted cross-factor interaction, a mistaken physical model, or an inadequate constitutional requirement. Preserve the baseline and shortest relevant witness; change the rule only if the case genuinely supports it.

**Failure:** the agent asserts “I followed the constitution” without evidence; all failing tests are construed as proof of misconduct; successful citations are construed as proof of working code; or a rule is quietly rewritten to absolve a previous failure.

## J. Fault provenance without whole-project reconstruction

**Starting point:** an older implementation was copied from an upstream project; a regression now appears and its original author/agent is gone.

**Request:** “Why does this work this way, and what actually broke?”

**Success:** A newly onboarded agent follows the owning set's end-of-set References to a pinned upstream GitHub implementation, then finds the local adaptation and its earlier evidence, compares changed assumptions, and identifies the smallest corrective factor. The decision annotation preserves prior rationale and is easy to supersede without erasing history.

**Failure:** unexplained unpinned URLs, no relation between source and the local code, heavy reconstructive context gathering, or defaulting to a new solution before checking the one already used.

## K. Human gives the vision; agents manage interpretation, scale and continuity

**Starting point:** a person has only text or voice access, has a broad ambition
for a multi-device software environment, and does not want to learn the
project's implementation structure to direct work.

**Request:** "I want a Wii-like console for trying apps, developing new ones,
and jumping between the TV and iPad. Use other agents when useful."

**What success looks like:** A high-level agent recovers the likely holistic
goal and offers a small number of genuinely different outcome-level
interpretations only where useful, with an intelligible default. The person
can say "C now, maybe B later" and agents translate that into factored,
reversible work. They handle routine architecture, citations, implementation,
tests, and integration without repeatedly interrupting the user. Each
consequential family of functions has a compact implementation-independent
purpose/promise/boundary and selectively cited version-pinned code
precedents, local changes and evidence, so another agent can join, take
over, or leave without repeated interviews or whole-repository study.
A subsequent "Actually make the TV UI more playful, not the backend"
changes the relevant factor without resetting unrelated progress.

**Failure signatures:** The agent asks the human to pick source files,
transports, frameworks or test commands; offers seven indistinguishable
options or performs a preference survey for a reversible choice; silently
chooses a consequential product direction; a changed preference requires
rewriting the whole application; workers block each other waiting for
implementation details despite stable intent contracts; onboarding requires
a complete chat transcript; cited works are generic homepages or invented
references; the agent claims success before an inspectable preview exists.

**Evidence boundary:** This case is a prospective acceptance criterion.
Intent-set documents and research references permit informed delegation
but do not by themselves prove that an implementation or on-device user
experience works. Escalate genuine preference/authority questions, not
routine technical uncertainty.

## L. Navigate general intent, functional choices, and implementation evidence

**Starting point:** A person describes a broad interactive-computing vision.
Several agents have implemented separate capabilities.

**Request:** "Remind me of the big idea. What is remote-input supposed to
do? Why use shared normalization instead of letting each game handle input?
Could we switch for this one application?"

**Success:** The agent gives a short human-readable purpose first, then the
relevant set/superset promises and a goal-based comparison of two designs.
If asked, it opens the actual code and selective version-pinned references,
distinguishing prior implementations from locally verified behavior. The
person can change one functional choice without rewriting the vision or
resetting independent work. A new agent reconstructs the reason without
asking the person to repeat the conversation.

**Failure:** The explanation starts with unrelated code; "we use A because
the code uses A"; source references are invented; functional intent is
mistaken for proven runtime behavior; a local alternative erases the shared
goal or previous evidence.

**Evidence boundary:** This is a prospective acceptance test. Documentation
alone does not establish that this interaction is implemented.

## M. Full human-to-tool software development, not philosophy alone

**Starting point:** A person has only a TV or iPad and a broad request
for a persistent playable idea. Logical Cloud has source-grounded
intent sets, some coding tools, and a placement simulator, but its
complete agent runtime is not assumed to exist.

**Request:** "Make a fun obstacle game for my sister. Let her play
something quickly, and tomorrow I want to ask for changes."

**What success looks like:** The person receives a coherent, brief
interpretation of the desired experience and any materially different
creative options; the functional promises specify a playable candidate,
consistent controls, named project identity and revision. An agent
actually locates the relevant existing code and inspected implementation
precedents, performs tool calls that create or modify source, runs
proportionate realistic checks, and returns a usable artifact or preview
with its real evidence level. Project identity, selected interpretation,
variant and evidence survive to the next agent/session; "make the jump
longer" changes that project without a full new interview.

**Failure signatures:** We stop at a philosophical decomposition;
the agent produces a plausible plan but no actual tool execution;
the simulator is claimed to be a real game runtime; an APK build is
presented as proof of usability; every adjustment requires the person
to administer CI; prior agent context is lost; the implementation is
rewritten from training conventions without examining its existing
purpose or sources.

**Evidence boundary:** A document describing this workflow specifies
it, not implements it. The current simulator can verify aspects of
placement under its model, not the full human-to-game experience.
Progress should expose the smallest working links rather than invent
missing connections or require all layers to be implemented serially.

## The scoreboard should be holistic

Compare candidate architectures on **time from broad vision to first meaningful interpretation or preview**, **time to accepted update**, **number of independently modified authoritative definitions**, **amount of context reacquired**, **number and severity of cross-factor inconsistencies**, **parallel-agent blocking time**, **real user-flow success**, **cost of necessary verification**, **rollback/resumption reliability**, and **ability to recover why the result exists**, **upstream-to-local implementation traceability**, **preference-driven unnecessary rewrites**, and **ability to classify a failed result as rule violation versus rule inadequacy**.

Do not invent numeric targets before there is a credible baseline. A short honest comparison, observed traces, and known uncertainty are better than a manufactured score. Benchmarks should reflect actual user flows and frequent realistic variation. Expand to rare but consequential failures when the stated risk justifies the cost.

## Stopping tree

- **Small localized change:** stop at useful preview plus relevant bounded checks, unless a consequential risk remains.
- **Cross-factor substitution:** stop after representative composition, with explicit untested intersections.
- **Actual device deployment:** stop only when authorization, observability, and rollback appropriate to the effect are satisfied.
- **Unknown architectural claim:** stop at a clearly labeled hypothesis or simulation; gather external evidence before treating it as fact.
- **Repeated failure of local optimization:** stop polishing and reconsider the governing intent, factor boundary, or whole workflow.

These are decision aids, not unconditional gates. If a gate itself becomes the primary obstacle to ordinary use, it is an architectural failure subject to LC-13.03.
