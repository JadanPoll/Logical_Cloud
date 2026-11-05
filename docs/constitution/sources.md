# Source projection: REM, RSM, and FKEN → Logical Cloud

This is a **selective synthesis**, not an attempt to import three entire research systems as software requirements. These documents belong to the separate [Learning_Visualizations_Taxonomy / Navigationals](https://github.com/JadanPoll/Learning_Visualizations_Taxonomy/tree/main/Navigationals) project. Their original context, uncertainty, and constraints should be preserved.

## Philosophical map versus executable engineering specification

The Navigationals repo is the upstream **collation, development and
navigation of general principles**. Logical Cloud is the **specific
software-development design**: how the person expresses intent, how a
high-level agent develops options and function sets, how other agents
recover and question research-grounded decisions, how code and tool
calls actually execute, how evidence is obtained and how revisions
persist. The operational map is
[vision-to-execution stack](../vision-to-execution-stack.md) and its
governing obligations are in [LC-17](../../CONSTITUTION.md).

Every such capability must move beyond a philosophical label to a
discoverable input, promise, authority boundary, working artifact or
honestly unimplemented interface, observable witness and repair path.
This does **not** mean creating seven services up front or requiring
them to run in a serial pipeline. Only build a new factor when a real
user flow benefits.

## REM — the Richer Engineering Method

[Source](https://github.com/JadanPoll/Learning_Visualizations_Taxonomy/blob/main/Navigationals/The_Richer_Engineering_Method.md)

**Applied here:** Recover the actual and holistic goal before solving a local problem; choose economical interventions; respect pre-existing constraints; optimize human interaction and transparency rather than creating “hostage situations”; notice that local optimization is not compositional optimization; use real user flows rather than vacuous rhetorical test cases.

**Critical self-play translation:** REM describes a tightening loop between data, response, reasoner, and the human meta-reasoner/goal director. Logical Cloud turns this into LC-06 and the agentic loop: fast iteration, visible results, parallel alternatives, informative experiments, and increasing automation of mechanical work. This is not a guarantee that autonomous loops will self-improve.

**Selective combinatorial exploration:** REM's recursive state/relationship investigation is useful at consequential integration boundaries; applying exhaustive formal state exploration to every button edit would violate REM's own practicality principle.

## RSM — the Richer Scientific Method

[Source](https://github.com/JadanPoll/Learning_Visualizations_Taxonomy/blob/main/Navigationals/The_Richer_Scientific_Method.md)

**Applied here:**
- **RSM-02:** Revisit the question and its higher purpose; stop excessive upward/downward decomposition when stable obligations suffice.
- **RSM-03.02–03.05:** Parameterize, factor, introduce useful intermediary representations, and coarse-grain where distinctions do not affect the current question.
- **RSM-04.04–04.05:** Use self-play to probe meaningful changes and boundaries, but distinguish model-conditional results from evidence about reality.
- **RSM-07:** Preserve method limits and resist architecture born of checklist completion instead of demonstrated need.

Logical Cloud's factorization is a question-dependent engineering representation, not a proof that all aspects of software can be made independent.

## FKEN — Fractal Knowledge and Ecosystem Navigation

[Source](https://github.com/JadanPoll/Learning_Visualizations_Taxonomy/blob/main/Navigationals/Fractal_Knowledge_And_Ecosystem_Navigation.md)

**Applied here:**
- **FKEN-01:** Keep navigation, investigation, and operations distinct even when they cooperate.
- **FKEN-03–06:** Hierarchical orientation with progressively relevant detail; useful inspiration for intent sets, without transplanting the entire knowledge-tower ontology.
- **FKEN-10–12:** Activate relationships conditionally on a question; selectively preserve reusable pathways, not every possible edge.
- **FKEN-17.1–17.4:** Recoverability, epistemic separation, resumption, and context-preserving provenance.
- **FKEN-19.1–19.6 and FKEN-20:** Justify new machinery against actual failures, compare simpler alternatives, and optimize the whole encounter-to-reuse path.
- **FKEN Appendix B:** Small, source-anchored certificates can help clarify decisions; they must not be confused with empirical verification.

## Synthesis boundaries

**Our additions:** software-specific intent-set certificates; factorized UI/locale/form-factor substitutions; parallel agent candidates; near-real-time spoken change requests crossing build/runtime devices; and GitHub Actions as selective independent evidence.

**We do not require:** a universal graph database, exhaustive ontology, globally mandatory checklists, numerically scored agent cognition, a monolithic tool, or a proof of optimality. We will revise the constitution if actual multi-agent development makes any of its machinery unhelpful.

A constitutional citation explains *why a method might guide an action*; it is not independent evidence that a proposed implementation works.

## New constitutional additions: provenance and axiomatic self-correction

**Research-paper-style sources (LC-14)** adapts REM's insistence on studying solved implementations, RSM's source/evidence distinctions, and FKEN's recovery of knowledge by source anchors into a software-specific rule: consequential design choices should cite **actual implementation code** at versioned revisions, plus their local adaptations and verification limits. This requirement is motivated by costly repeated agent reconstruction and incompatible training-derived preferences. See [provenance and inspected GitHub code examples](provenance.md).

**Numbered axiomatic certificates (LC-15)** draws particularly from RSM's stable-address clauses and compact method traces, REM's realistic-failure-led development, and FKEN's selective application certificates. It introduces a decision-relative obligation calculus and distinguishes **did the agent follow the provision?** from **did it achieve the goal?** The latter can falsify the sufficiency of a faithfully applied constitution without implying all behavior is formally decidable. See [axiom calculus and counterexample procedure](axiom-calculus.md).

Do not confuse the RSM/REM/FKEN *principles that motivated these rules* with empirical evidence that the rules improve this project's developer experience; the acceptance workflows are how we assess that claim.
