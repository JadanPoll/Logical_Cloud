# Agent entrypoint — Logical Cloud

Read [CONSTITUTION.md](CONSTITUTION.md) before substantial design or development work. Its objective is rapid, independent, factorized software evolution under human intent—not merely a remote-computation simulator. This short file is an entrypoint, not an extra approval gate.

For a specific task:

1. Recover what the user wants to experience, including the likely larger goal. Preserve existing work and discover relevant constraints before deleting or replacing it.
2. Navigate the smallest relevant **intent sets** and affected interfaces (see [intent-set doctrine](docs/constitution/intent-sets.md)). Do not reconstruct the whole repository by default. If an intent certificate is missing, infer cautiously from implementation and document only what is consequential.
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
