# Logical Cloud — from engineering philosophy to executable development

> **Status:** architectural target and testable contracts. The current repository
> implements a deterministic placement simulator and report generation; it
> does **not** yet implement the complete human/agent/worker/runtime stack.
> This document identifies the missing pieces, rather than naming them as
> existing services.

## The distinction that defines the project

The **Navigationals** work in Learning_Visualizations_Taxonomy organizes
and develops general philosophies and navigational strategies from REM, RSM,
and FKEN: how to recognize the right problem, move among reasoning operations,
recover knowledge, and preserve the holistic picture.

**Logical Cloud is their software-and-engineering realization.** Its subject
is what the actual experience, interfaces, decision policies, agent
responsibilities, source and tool contracts, execution substrates, evidence,
and revision loop must be for a person to comfortably direct sophisticated
software work through text or voice.

This is not an effort to copy those frameworks into every project or to
replace their original authoritative documents. They supply guidance and
questions; Logical Cloud specifies operational obligations, implementation
boundaries, and reproducible acceptance criteria in the engineering domain.

**North star:** the human supplies the vision; an intelligent system
understands and sharpens it, offers meaningful alternative experiences
when needed, delegates and executes what it can, shows an early useful
result, and makes subsequent changes of mind inexpensive. The system,
rather than the human, bears the cost of ordinary context retrieval,
compilation, placement, integration, instrumentation, and agent onboarding.

## The complete conceptual stack

The numbers are **navigational layers**, not a mandatory waterfall. Agents
may jump between layers as REM's reasoning ring demands. In particular,
unknown implementation details must not automatically hold up independent
work against a sufficiently clear functional promise.

| Level | Owner / contract | What goes in | What should come back |
| --- | --- | --- | --- |
| **1. General intent** | Human vision, interpreted by high-level agent | A vague idea, text/voice corrections, holistic goals | Short README-level shared understanding: what this is for and the intended experience |
| **2. Functional intent** | Intent-set/superset navigator | The general goal, selected/rejected meanings, actual constraints | Critical sub-big-pictures; observable promises, meaningful alternatives, scope and intersections |
| **3. Grounded decisions** | Source-aware research/design agents | Functional questions, relevant existing work, unresolved hypotheses | A-versus-B reasoning and applicable version-pinned code precedents; proposed factors and contracts, not unsupported "best practices" |
| **4. Delegation and coordination** | High-level planner and independent workers | Priorities, stable contracts, candidate variants, permissions and available workers | Bounded independent tasks, versioned proposals, clear exceptions/conflicts, no repeated interviews |
| **5. Development and execution** | Coding agents and tool/device adapters | Scoped decisions and source contracts | Actual code edits, build invocations, tool calls, artifacts, runnable previews, or explicit evidence of why a proposed action cannot run |
| **6. Observation and criticism** | Test harnesses, agent evaluators, human as goal director | Candidate results, realistic user flows, resource and fidelity limits | Source checks, simulation, emulator/physical observations, A/B comparison and concise failure witnesses; evidence type is explicit |
| **7. Revision and continuity** | Project knowledge and state service | Human correction, findings, completed and abandoned variants | Updated intent/factors, recoverable reasons and evidence, checkpoints, rollback, easy agent handoff |

**Three human-facing explanations:** levels 1, 2 and 3–6 respectively
provide (a) the general idea, (b) revisable functional promises, and
(c) implementation details and research-quality evidence. The human
should normally see the smallest relevant level and be able to ask
"Why A rather than B?" and drill down or go back up without starting over.

### What makes this a specification instead of a philosophical checklist?

For each *consequential* boundary, identify only what is needed to build
or inspect it:

- **Trigger/input:** what human intent, agent event or artifact activates it?
- **Promise/output:** what can another component rely on, regardless of
  the chosen implementation or where it runs?
- **Options and uncertainty:** which interpretations or implementations
  remain live? Which are already selected by the human?
- **Authority and effects:** what can be explored autonomously, and what
  requires explicit device/data/rollout permission?
- **Witness:** what small observable trace or user flow distinguishes
  a working outcome from a plan, simulation, or agent claim?
- **Repair route:** which owning factor should change if the witness fails,
  and how does another agent recover the prior reasoning and sources?

No compulsory global schema or universal plugin ABI is implied. A short
README, an intent-set certificate, a source-backed decision, and a concrete
artifact may be enough. Use machine-readable structures where actual
coordination and substitution benefit from them, not as paperwork.

### Factorized architecture before the full stack is known

Before choosing an implementation, an agent can treat the person's
holistic goal as a stable objective and vary **functional design variables**
such as UI presentation, control modality, game rules, scene representation,
asset source, agent workflow, executor and state continuity. Constraints
and interactions are explicit; unknown dimensions remain unknown. This
also applies to Compute's TV interface and future agentic 3D Playroom,
not only portability or distributed execution placement.

A first executable [design-space contract](algebraic-design-spaces.md)
can produce a human-facing summary of relevant choices, unresolved
dependencies and the next informative test, plus an agent-readable JSON
record. The contract does not substitute for real code, evidence, or a
human's value judgments. Avoid a full combinatorial sweep when one
meaningful factor comparison is sufficient.

### The crucial non-dependency rule

A's *implementation* need not finish before B starts if B can advance
against A's relevant sufficiently stable **functional contract**. Agents
may mock A, compare candidate contracts, explore factor alternatives,
or run simulations, with honest labeling. Only the affected
intersection needs integration evidence later.

This relocates low-level uncertainty to the responsible subsystem;
it does not pretend that permissions, physics, or real device fidelity
vanish. Their effects become consequential only where they can change the
user's requested outcome or an authorized real-world action.

## Worked use case: a playable Fire TV idea

**Human:** "Make a silly obstacle game for my sister; I want her to play
immediately, and I should be able to change it tomorrow."

1. **General intent:** accessible, entertaining creation and continuing
   ownership of a playable idea, not an Android project-management task.
2. **Functional intent:** one prompt yields an early playable scene,
   remote-friendly input, named persistent project and versions. If a
   meaningful artistic interpretation is unclear, offer two or three
   brief creative directions; do not ask the human to pick a compiler.
3. **Grounded choice:** an agent inspects existing, relevant engine/game
   implementations, documents why the chosen prototype route fits these
   constraints and what evidence it actually inspected. Other routes
   remain replaceable.
4. **Independent work:** game rules, visual theme, input normalization,
   persistence and preview can progress through clear shared promises,
   even if one contributor's native build is still incomplete.
5. **Actual work:** agents edit source, invoke available tools, produce
   and run a candidate on an appropriate surface. A planned action is
   not reported as executed.
6. **Critique:** test a realistic play → close → reopen → one-sentence
   change loop. Distinguish simulated preview, Android emulator, actual
   Fire TV observation, and the human's accepted experience.
7. **Continue:** store the project, source/artifact revisions, chosen
   meanings, decisions and bounded evidence. Another agent can resume
   tomorrow without rereading the chat.

**Why this is better than simply "more automated builds":** the next
human idea can be understood and explored before an unrelated package
build, emulator startup, or low-level input experiment has completed.

## Smallest honest implementation sequence

1. **Prove interpretation before orchestration:** a human prompt can yield
   a concise holistic statement, critical functional sub-goals, and
   meaningful options, with accepted corrections recorded as revisions
   to the same intent—not a detached new response.
2. **Prove one source-backed factor change:** an agent can navigate only
   the affected intent neighborhood, inspect actual precedents, make
   one editable candidate, and return a real preview plus traceable evidence.
3. **Prove continuation:** a second agent can recover the same project,
   chosen intent, code, rationale, variants and evidence without
   re-interviewing the human.
4. **Prove cross-device substitution:** move a compatible build/preview
   stage between available workers or devices without changing its
   human-facing meaning; measure real cost and trust boundaries.

These are progression examples, not serial gates for unrelated work.
Independent workers can develop against stable contracts in parallel.

## Relationship to existing repository work

- [Constitution](../CONSTITUTION.md): numbered operational obligations
  and falsifiable rule-following evidence.
- [Intent sets](constitution/intent-sets.md): navigable promises,
  overlaps and the three human-facing explanations.
- [Agentic development loop](constitution/agentic-loop.md): the ring
  of orientation, variation, evidence, critique and resumption.
- [Architecture](architecture.md): application/fabric/transport/
  state/placement factor boundaries.
- [Agent change protocol](agent-change-protocol.md): distinguish
  logical contract, implementation version, execution plan and rollout.
- [Acceptance cases](constitution/acceptance.md): real human/agent flows
  that future implementations must pass.
- [Provenance](constitution/provenance.md) and
  [framework sources](constitution/sources.md): actual inspected
  mechanisms and upstream philosophical references, not decorative citations.

The only current executable slice is the simulator, its CLI, reports and
tests. The broader interpretation, agent orchestration, program editing,
live tool execution, multi-device runtime, and unified preview/continuation
remain implementation objectives until supported by working evidence.
