# Agent entrypoint — Logical Cloud

Read [CONSTITUTION.md](CONSTITUTION.md) before substantial design or development work. Its objective is rapid, independent, factorized software evolution under human intent—not merely a remote-computation simulator. This short file is an entrypoint, not an extra approval gate.

For a specific task:

1. Recover the user's big-picture and holistic vision (LC-16); the human is the goal director, not the project's technical integrator. When materially different interpretations remain, present a few useful contrasting choices with a sensible default, or proceed to a reversible preview when asking would add friction. Preserve existing work and discover relevant constraints before deleting or replacing it.
2. Distinguish three navigable levels: **general intent** (README-like vision), **functional intent** (revisable function sets/supersets and why A versus B), and **implementation/evidence** (actual code, inspected version-pinned research precedents, local tests). Navigate the smallest relevant **intent sets** and affected interfaces (see [intent-set doctrine](docs/constitution/intent-sets.md)). Recover each pertinent function-family's general idea, promise and boundary independently of implementation, plus selectively pinned code precedents and local evidence for consequential choices; this is the handoff to a new agent, not another request for the human to repeat history. Do not reconstruct the whole repository by default. If an intent certificate is missing, infer cautiously from implementation and document only what is consequential.
3. Prefer substituting one authoritative factor over copying or editing many dependent parts. Style, locale, form factor, behavior, and placement should usually remain separately variable.
4. Keep independent experiments and other agents' changes intact. If two edits overlap, report the actual violated contract instead of claiming false compatibility.
5. Run realistic, scope-proportionate checks; distinguish simulations from hardware evidence. Prefer quick, useful previews and copyable failure details.
6. Describe the changed intent, relevant factors, practical evidence, limitations, and next useful action. Do not promote or deploy consequential changes without proper authorization.

Never turn these steps into a compulsory report or long checklist for a trivial edit. If they obstruct the user's purpose, apply [LC-13.03](CONSTITUTION.md).

Companion references: [agentic loop](docs/constitution/agentic-loop.md), [acceptance flows](docs/constitution/acceptance.md), and [REM/RSM/FKEN source projection](docs/constitution/sources.md).

## Autonomous development and integration

The owner has explicitly requested **forward momentum rather than approval-gated repository housekeeping**. Treat normal, reversible project edits as authorized work: investigate, implement, run proportionate checks, and **commit directly to the existing main branch** when appropriate. Do not stop after proposing a PR or ask the owner to merge routine work.

Use a feature branch/PR when it adds practical value (parallel agents, conflicting edits, high-risk integration, or independent validation). If you create a PR, **own its lifecycle**: inspect CI, repair failures, and merge it yourself when the checks are satisfactory and the action is authorized. Do not leave completed, routine changes waiting for the owner to press Merge. Distinguish unrelated failing experiments from genuinely blocking dependencies; do not hold ongoing work hostage.

Autonomy is not unlimited authority. Do not silently deploy to production devices, expose secrets, broaden privileges, publish private information, or perform destructive/irreversible actions. Preserve existing user work and disclose consequential uncertainty. For materially risky operations, obtain the approval actually required; avoid seeking it for ordinary, reversible repository maintenance.

The objective is an **autonomous intent → implementation → evidence → integrated result** flow, not a growing backlog of proposed changes. Prefer an accurate summary of work actually landed over reports about work that merely awaits integration.

## Source-first implementation and constitutional certification

Before changing a consequential mechanism, inspect the owning intent set's cited decisions and **real existing source implementations**, preferably version-pinned GitHub code and associated tests, not only a README/API reference. Prefer locally proven practice to an architecture that merely seems familiar from training. Annotate the adopted mechanism near its consequential decision with a stable reference key and maintain an **end-of-set References** section or link to the set's canonical ledger: [provenance](docs/constitution/provenance.md) / [LC-14](CONSTITUTION.md). Existing cited choices are challengeable, but disagreements must identify a precise obligation and concrete evidence, counterexample, or better implementation precedent. If no suitable precedent exists, label the change **experimental/unverified** rather than invent a citation.

For nontrivial edits, include a **minimal constitutional certificate**: the narrow `LC-XX.Y` clauses actually governing the decision, their applicability, a link to the action/source/test supporting compliance, and material unknowns. Do not equate “green CI,” an inspected upstream example, or an agent's own statement with verified real-device behavior. Separate **rule conformance** from **outcome success**. On failure, classify violation vs inadequacy of a faithfully applied rule vs mistaken model or missing evidence; preserve a small counterexample before amending. See [axiom calculus](docs/constitution/axiom-calculus.md) / [LC-15](CONSTITUTION.md).

Maintain the autonomy rule above: **commit ordinary reversible changes directly, and own PRs through merging when one is useful.** The source/certificate system must make development faster by preventing rediscovery and unsupported architectural drift, not turn every trivial fix into a research paper or approval queue.
