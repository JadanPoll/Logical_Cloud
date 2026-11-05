# Fire Console, second executed slice — Snake, Android Dojo and virtual devices

A test of the Logical Cloud vision-to-code contract using three independent,
user-directed refinements in a working project. This case is **not** evidence
that Logical Cloud already operates a complete distributed agent runtime.

## Human intent (Layers 1 and 2)

1. **Playroom:** extend the very small native game catalog with Snake; learn
   from game/input/renderer behavior rather than construct a universal engine.
2. **Android Dojo:** make the ungraded, topic-based challenges and skills
   navigable *on the TV*; allow persistent partial notes, and give the lab
   its own dark, Japanese-arcade-inspired visual taste without forcing it
   upon the rest of the light Console.
3. **Compute:** distinguish a device's identity from its standardized
   capabilities. A device may be physical (TV, PC, Pi), or virtual (GitHub,
   Python worker, agentic environment). GitHub's repositories provide
   versioned storage/assets; Actions provide static compilation/workflows
   that other agents may eventually discover and reuse.
4. **Registration:** opt for a cheap GET announcement prototype with no
   authentication *for public discovery metadata only*. No authority to
   invoke arbitrary commands follows from advertising a capability.

A developer-provided GUI theme belongs to the specific experience; the
platform should standardize semantic navigation and focus, not flatten
independent creative identity.

## Inspected source and minimal implementation

Source starting points were the existing Fire
[MiniGameLabActivity](https://github.com/JadanPoll/fire/blob/main/app/src/main/java/dev/jadan/fire/MiniGameLabActivity.java),
[ProbeGameModel](https://github.com/JadanPoll/fire/blob/main/app/src/main/java/dev/jadan/fire/ProbeGameModel.java),
[TvUi](https://github.com/JadanPoll/fire/blob/main/app/src/main/java/dev/jadan/fire/TvUi.java),
[InputLabActivity](https://github.com/JadanPoll/fire/blob/main/app/src/main/java/dev/jadan/fire/InputLabActivity.java),
[Compute Codex desk](https://github.com/JadanPoll/fire/blob/main/app/src/main/java/dev/jadan/fire/CodexDeskActivity.java)
and the canonical Dojo JSON catalog. New work:
[Fire PR #16](https://github.com/JadanPoll/fire/pull/16).

- Independent pure-Java Snake rules and focused tests plus a foreground
  Activity; existing Playroom catalog retained.
- Native Dojo browses the **same authoritative challenge JSON** as the host
  CLI, mounted as an Android asset. The new palette is localized to the Dojo,
  and local notes have no cloud synchronization claim.
- Compute has an icon-based gallery of physical and virtual devices.
  GitHub is one virtual platform with distinct capabilities for Git/versioned
  resources, Actions workflows/compilation, and published artifacts.
- The Python standard-library HTTP registry accepts a bounded unauthenticated
  GET announcement and returns a metadata-only device list. Transient claims
  are labeled *unverified*, expire after five minutes and are not remotely
  executable. The TV gallery is currently a bundled offline snapshot:
  **the server and the Fire UI are not yet a connected live discovery flow**.

## New constitutional questions surfaced

- Does a common application layer prescribe the appearance of every developer
  app? **No**: the reusable contract is mainly TV focus/control semantics,
  while visuals are substitutable (LC-02, LC-16.04).
- Is GitHub inherently less of a "device" because it is not a physical box?
  **No**: its capability offerings can be modeled as an execution/storage
  provider while its projects, workflows and artifacts remain distinct
  versioned resources. This is a proposed generalization, not proof of a
  working heterogeneous runtime.
- Does the explicit decision to omit authentication authorize all device
  actions? **No**: it applies only to low-risk public metadata discovery.
  A GET label cannot become an implicit permission grant (LC-11.03).
- Can a user inspect challenges and save notes without a working remote agent?
  The TV-native UI implements that bounded contract; full distributed
  development and skill-certification are separate, unmet goals (LC-15.04).

## Follow-up: How high and low can Android Dojo go?

The user refined Dojo's most interesting **research boundary**: it should
invite extremely high-level, script-like solutions as well as native code,
Android service observation, and lower-level investigation. The difficulty
or intellectual depth of a challenge is **not** determined by how much
low-level code it uses.

[Fire PR #17](https://github.com/JadanPoll/fire/pull/17) provides a
second, optional axis over the canonical Dojo problems: scripted/web,
application framework, native/JNI, authorized ADB/system diagnostics, and
kernel/firmware research only. A small JavaScript experiment may expose the
same scheduling boundary as a C++ routine, and the learner should be able
to travel between representations without mandatory coursework or grades.

**Concrete falsifying comparisons:** (1) scripted sprite motion versus
Android Canvas, measured by real frame intervals; (2) a batched versus
per-call JNI operation; (3) app-visible state versus authorized shell
diagnostics. Each is a meaningful question with relevant glossary terms,
partial-progress journal entries, and explicit permissions/capability
limits. Do not infer that ordinary native code can install drivers or
change privileged services. This is an experiment taxonomy, not evidence
that the experiments have been performed or devices are rooted.

**Constitutional relevance:** LC-16.04 (preserve option to change the
abstraction), LC-02 (separate what is being studied from representation),
LC-11.01 (proportionate real measurements), LC-15.04 (method versus
observed learning outcome). No constitutional amendment is presently
warranted; real device observations may change the chosen next mechanism.

## Evidence that should be measured

| Claim | Needed witness |
| --- | --- |
| Snake rules behave deterministically | App JVM tests |
| TV Snake playable with real remote | Physical Fire OS directional/OK/focus trace |
| Dojo opens, is navigable and preserves notes | Android build plus actual reopen on physical TV |
| Dojo data has one authoritative catalog | Gradle asset source link and host CLI reading the same JSON |
| GitHub is discoverable as a virtual capability provider | JSON catalog / gallery |
| Any device can announce metadata through GET | Local HTTP test with actual request and returned JSON |
| Announcement triggers a GitHub Action or a device command | **Not implemented or claimed** |
| TV loads remote dynamic announcements | **Not implemented or claimed** |
| Entire agentic cloud works end to end | **Not implemented or claimed** |

An agent should update this case with real CI outcomes and independent device
observations rather than promoting planned behavior to verified status.
