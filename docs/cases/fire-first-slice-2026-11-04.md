# Fire Console first implementation case — 2026-11-04

This is an **observed and source-integrated agent/tool workflow**, not a claim that the full
Logical Cloud runtime has been built. It challenges the constitution against a
real user-directed task, rather than writing another architectural diagram.

## Parent intent and constraints (human-accepted)

- Fire TV is an open-ended, Wii-like home for games, creating, and tacit Android understanding.
- **Portability intelligence:** an agent should consult a growing evidence-qualified
  database to explain whether a requested app/game can run or be adapted, and whether
  the remote or a future iPad companion makes it usable.
- **Android Dojo:** interesting problem statements organized by topic, glossary and
  tacit checks, with ungraded, revisitable partial progress.
- **Creative Playroom:** intentionally tiny 2D games first, to expose real device
  limitations without overbuilding a general game system.
- **Assets/projects:** longer term, allow game engines on TV to consume independently
  versioned and cached assets developed off-device.
- **Compute product vision deferred:** existing Fire Compute retained, not expanded.
- Preserve existing six-channel UI, GBA route, pinned browser games and saved user data.

## Source first: the actual prior implementation

At Fire commit
[1b3e7e6f83bb15f24bd466eb5bc8202f34a95ef1](https://github.com/JadanPoll/fire/commit/1b3e7e6f83bb15f24bd466eb5bc8202f34a95ef1),
the agent examined:
[GameShelfActivity](https://github.com/JadanPoll/fire/blob/1b3e7e6f83bb15f24bd466eb5bc8202f34a95ef1/app/src/main/java/dev/jadan/fire/GameShelfActivity.java),
[ConsoleActivity](https://github.com/JadanPoll/fire/blob/1b3e7e6f83bb15f24bd466eb5bc8202f34a95ef1/app/src/main/java/dev/jadan/fire/ConsoleActivity.java),
[TvUi](https://github.com/JadanPoll/fire/blob/1b3e7e6f83bb15f24bd466eb5bc8202f34a95ef1/app/src/main/java/dev/jadan/fire/TvUi.java),
[Remote Adapter](https://github.com/JadanPoll/fire/blob/1b3e7e6f83bb15f24bd466eb5bc8202f34a95ef1/AppOS/Remote/README.md),
[Playroom GBA](https://github.com/JadanPoll/fire/blob/1b3e7e6f83bb15f24bd466eb5bc8202f34a95ef1/docs/PLAYROOM_GBA.md),
and [change-scoped CI](https://github.com/JadanPoll/fire/blob/1b3e7e6f83bb15f24bd466eb5bc8202f34a95ef1/.github/workflows/fast-validation.yml).

The candidate uses the already-existing native Playroom Activity and focused
Android View patterns; it does not create a mandatory SDK, input broker or
engine framework. It preserves the existing GBA and pinned web game routes.

## Actual agent/tool links

[Merged Fire PR #15](https://github.com/JadanPoll/fire/pull/15) ([integrated commit `3605b6dd`](https://github.com/JadanPoll/fire/commit/3605b6dd9af554204dd958407e2d071fccf91b13)) contains:
1. **Intent to code:** two minimal native game probes (Collect and Dodge)
   reachable from Playroom, with pure Java model tests.
2. **Agent-readable knowledge:** a machine-readable portability seed and
   `tools/portability_matrix.py` for deterministic query/validation. A missing
   entry produces an explicit *unassessed* research stub, not an impossible claim.
   Interaction quality is independent of execution feasibility.
3. **Knowledge to partial progress:** four Dojo challenges with glossaries
   and tacit checks; `tools/android_dojo.py` persists notes and revisiting
   state locally, without grades.
4. **Proportionate feedback:** Python unit tests and native JVM tests; the
   existing change-scoped CI can exercise the Android source.

Useful independent invocations (from the Fire checkout):

```bash
python3 tools/portability_matrix.py lookup "VS Code"
python3 tools/portability_matrix.py lookup "An unknown title"
python3 tools/android_dojo.py show remote-double-action
python3 tools/android_dojo.py note remote-double-action "Saw unexpected repeated DOWN"
python3 -m unittest discover -s tools -p 'test_*.py'
```

## Evidence ledger

| Claim | Evidence type | Current judgment |
| --- | --- | --- |
| The user-selected Layer 2 can be expressed as independent, navigable factors | Human-accepted intent, Fire vision revision | Supported as intent only |
| Agents made actual Fire source/tool changes | Inspectable PR diff and commit history | Supported |
| Unknown software is not silently called incompatible | Source logic and unit test | **Supported:** targeted CI passed |
| Dojo partial notes survive a program restart | Source logic and unit test | **Supported:** targeted CI passed |
| Native minigames compile | GitHub Actions `:app:testReleaseUnitTest` and `:app:assembleRelease` | **Supported:** [CI run 41978298874](https://github.com/JadanPoll/fire/actions/runs/41978298874) passed |
| Fire remote successfully plays the games | Physical Fire TV observation | **Undetermined** |
| Game assets can be independently refreshed from GitHub | No implementation yet | **Not established** |
| Full human→agent→device→revision loop is operational | No complete run | **Not established** |

## A real failed test and its classification

The first [CI run 41978080951](https://github.com/JadanPoll/fire/actions/runs/41978080951)
failed *before* Android compilation. The portability index validator treated
the canonical ID `vscode` and an alias `vscode` **within the same record** as
conflicting identities. This was a local *implementation/schema error*, not
a counterexample to the user's portability goal or evidence that Android is
incompatible. The scoped correction permits synonyms within an entry while
still rejecting ambiguous names across distinct entries. The following
[run 41978298874](https://github.com/JadanPoll/fire/actions/runs/41978298874)
passed static contracts, Python unit tests, the app's JVM unit tests and
Android release assembly. No device test was performed.

**LC-15 classification:** a narrow implementation-rule bug was found and
repaired, with prior failed evidence preserved. **No LC constitutional
amendment is justified**: the governing precedent/evidence/intent obligations
did not require misinterpreting aliases. A much more consequential remaining
unknown is how an agent translates a route candidate into a *usable* real TV
experience. That remains an acceptance experiment, not a solved feature.

## Constitution pressure test

- **LC-16.03, LC-16.10:** accepted intent is acted upon with code and separate
  contracts rather than additional surveys. Inspect PR and acceptance files.
- **LC-02 and LC-04:** isolate game semantics, TV presentation, portability
  knowledge and Dojo records; verify physical intersections later.
- **LC-14.01:** scoped inspection of actual existing source paths occurred.
  Pinned original source links appear above; new mechanisms are still
  experimental, not proven by citations.
- **LC-11.01 and LC-09.02:** use narrow Python/JVM and changed-module CI; keep
  physical Fire OS verification distinct.
- **LC-15.03–15.05:** incomplete runtime evidence is *undetermined*, not
  automatically supported. No constitution amendment is warranted from
  missing physical evidence alone.

## What this case teaches Logical Cloud

The first practical interface is not necessarily a remote worker or novel
orchestrator: it can be a small, deterministic capability lookup that an agent
can query before choosing a tool, then update with observed evidence. Another
agent can retrieve this case and the Fire datasets without reconstructing
the entire conversation. But **lookup ≠ adaptation**, **a note ledger ≠ TV Dojo
experience**, and **a build ≠ on-device playable proof**.

The next falsifying experiment is to run a real minigame on the physical TV,
observe D-pad/focus/cadence, and revise one narrow factor. Do not build a
general Compute service to make that experiment possible.
