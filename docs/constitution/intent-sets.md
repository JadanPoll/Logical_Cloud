# Intent sets: a navigable hierarchy of promises

**Constitutional basis:** LC-01, LC-02, LC-03, LC-04, LC-07. This describes how an agent should *understand* a project; it does not prescribe a file format, framework, or fixed implementation.

## Why a “set hierarchy”?

A contemporary agent often spends more effort reconstructing an application's implicit agreement with itself than making the change requested. A developer adds a new locale or adjusts an overlay and must inspect every screen to avoid inconsistent copies of the same design choice. Documentation that mirrors file-by-file implementation does not solve this; it merely creates a second codebase to synchronize.

Instead, let a group of related functions have a **brief certificate of intent**. Superset certificates explain what the family is for; child certificates specialize its promises. The result behaves like a navigational index of reusable obligations, not a prose code listing.

## One practical shape

- **Application:** a responsive interactive environment with durable user work, discoverable navigation, and responsive feedback.
  - **External devices:** present device capabilities consistently; failure of one device does not obstruct unrelated functions.
    - **Camera:** provide authorized, understandable acquisition of image data and its status.
      - **Capture:** deliver frames or explicit acquisition failures; do not silently claim a camera is active when it is not.
    - **Remote input:** convert inconsistent device-specific input into predictable user intentions.
  - **Player:** make playback state and available actions intelligible across surfaces.
    - **Overlay:** expose controls appropriately for the active input and viewing context.
- **Cross-cutting style:** governs semantic visual roles and presentation consistency, not video decoding.
- **Localization:** governs meaning and presentation of language and regional formats, not camera acquisition.
- **Form-factor adapters:** make the same interaction purpose usable on TV, phone, or desktop, with different physical controls where necessary.
- **Execution fabric:** provides compliant scheduling and remote access under constraints, not the user's application semantics.

This illustration is **not** a required ontology. A camera's permissions also intersect security, privacy, device capabilities, and the application lifecycle. Therefore the real structure is a family of overlapping **sets and relationships**, not a rigid single-parent tree.

## The smallest useful intent certificate

Keep it short enough that an agent can actually read it:

**ID and parent sets:** stable name; relevant generalizations and cross-cutting obligations.

**Purpose:** one or two sentences describing *why this group exists* in user-facing or system-observable terms.

**Promise:** a small number of externally observable obligations or permitted variations.

**Boundary:** what is expected from other sets; what the group does not own.

**Known uncertainty:** a material unsolved condition, if any. Omit when nothing relevant is uncertain.

Example:

> **Set:** External Devices / Camera / Capture  
> **Purpose:** Let authorized applications receive image frames and understand whether acquisition is working.  
> **Promise:** A capture request yields frames or an explicit reason that it cannot; missing hardware cannot make unrelated navigation unusable.  
> **Boundary:** Does not own visual styling, translation, permission granting, or where inference runs.  
> **Intersecting sets:** Device capability, authority, application lifecycle.  
> **Evidence:** Intent only; implementation compliance not established here.

No required field should become a novel administrative obligation when a sentence or existing reference suffices. Implementation specifics belong in code, precise API contracts, or selectively linked notes only when they change the externally relevant promise.

## Retrieval is question-conditioned

For “make the TV's playback controls easier to see,” recover:

1. Product purpose and the **Player / Overlay** intent.
2. Applicable **Style**, **TV input/form factor**, and **Accessibility** obligations.
3. Only the implementation entrypoints and contracts needed for this change.
4. Evidence of past relevant failures, if available.

Do **not** automatically read camera setup, cloud worker scheduling, internationalization dictionaries, or the entire repository.

For “change every control's text size,” retrieve the authoritative typography factor first; fan out to local exceptions only when genuine compatibility concerns appear. This is what it means for a change to have low semantic fan-out—not merely fewer files.

## Inheritance, overlap, and change propagation

A child's obligations cannot silently contradict its parent's purpose. An overlapping set adds obligations without magically making its implementation identical. An agent changing a parent should **identify affected descendants or intersections** and verify the relevant externally visible behavior, not manually rewrite every descendant's certificate.

Two independently modified factors compose **only when their joint obligations still hold**. For example, a German translation with longer labels may alter TV overlay spacing. The style and locale files remain separate, but their intersection requires a representative composition check. Independence of representation does not imply physical independence of behavior.

Multiple parents are allowed where a responsibility genuinely belongs to several families. References, IDs, and relationship descriptions must remain retrievable, but avoid making a mandatory global graph database or exhaustive ontology the price of editing a button.

## Certification and refinement discipline

A certificate is an *intent claim*. Verified, observed, simulated, proposed, and unknown implementation status must remain distinct. Do not write “works across all devices” because the intent says it should. A certificate should survive ordinary refactoring; rewrite it when the obligation changes, not because the code was reorganized.

Refine an intent set when a concrete question exposes a consequential ambiguity. Otherwise stop at an intelligible stable interface. Carry forward a short explanation of an unexpected architectural decision when future agents would otherwise repeatedly rediscover it.

The target is **knowledge reuse without repeated memory work**: the next agent should confidently find what matters, distinguish obligations from conjecture, and begin experimenting.

## Research-style annotations and references belong to the set

An **intent certificate** describes a promise; a **decision annotation** records the reason a particular implementation approach was selected. Keep them distinct. For a consequential mechanism, record a compact citation key beside the adopted choice and an **end-of-set References** section (or link to one canonical shared ledger), ideally pointing to source code and tests at a pinned Git revision rather than a moving document. This lets agents inspect relevant precedents as a unit and trace a mistaken local implementation back to the actual source mechanism.

A reference chain should be navigable both ways: **intent → decision → code precedent → local implementation → local evidence**, and back from a failure to the rule or source that motivated it. A cited precedent is not automatically verified locally; state what was actually observed, modeled, or untested. Multiple children may reference one parent's source without copying a growing bibliography. This is [LC-14](../../CONSTITUTION.md), developed in [research-style provenance](provenance.md).

An agent onboarding into this set must read the applicable parent purpose and the relevant source-backed decisions before substituting a training-familiar alternative. If the established reasoning is wrong, preserve its original evidence and challenge it with a concrete test or competing code precedent. For consequential changes, a brief [LC-15 rule certificate](axiom-calculus.md) records which numbered obligations were applied and whether the observed outcome actually met the goal. Avoid formal paperwork on insignificant edits.
