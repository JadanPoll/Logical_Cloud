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

## The scoreboard should be holistic

Compare candidate architectures on **time to first meaningful preview**, **time to accepted update**, **number of independently modified authoritative definitions**, **amount of context reacquired**, **number and severity of cross-factor inconsistencies**, **parallel-agent blocking time**, **real user-flow success**, **cost of necessary verification**, **rollback/resumption reliability**, and **ability to recover why the result exists**.

Do not invent numeric targets before there is a credible baseline. A short honest comparison, observed traces, and known uncertainty are better than a manufactured score. Benchmarks should reflect actual user flows and frequent realistic variation. Expand to rare but consequential failures when the stated risk justifies the cost.

## Stopping tree

- **Small localized change:** stop at useful preview plus relevant bounded checks, unless a consequential risk remains.
- **Cross-factor substitution:** stop after representative composition, with explicit untested intersections.
- **Actual device deployment:** stop only when authorization, observability, and rollback appropriate to the effect are satisfied.
- **Unknown architectural claim:** stop at a clearly labeled hypothesis or simulation; gather external evidence before treating it as fact.
- **Repeated failure of local optimization:** stop polishing and reconsider the governing intent, factor boundary, or whole workflow.

These are decision aids, not unconditional gates. If a gate itself becomes the primary obstacle to ordinary use, it is an architectural failure subject to LC-13.03.
