# Research-paper-style provenance for software decisions

**Constitutional basis:** [LC-14](../../CONSTITUTION.md). This document defines a lightweight, inspectable evidence trail: **intent set → annotated choice → specific upstream implementation → local adaptation → local evidence**. It should help new agents onboard without importing incompatible preferences from their training distribution.

## The rule: source-grounded development

Before choosing or replacing a consequential implementation, examine the relevant *existing code implementation* and its tests, preferably a pinned GitHub source revision. Find existing work in **this** repository first. Do not cite a library's homepage or an API description as proof that its usage pattern is appropriate. Documentation helps interpret code; code inspection helps establish which mechanism actually exists; our own observations determine whether it works *here*.

Record one short citation marker near the consequential decision (for example, `[STYLE-1]`), with a **References** section at the end of the owning intent set or a pointer to one canonical shared list. That makes a set independently auditable and allows failed assumptions to be traced without reading all of the project.

**A reference is not a proof.** The source may contain bugs, rely on unusual environment details, or fail when adapted. Preserve the difference between *observed upstream*, *adopted locally*, *tested here*, *simulated*, and *hypothesized*. Check licensing before copying code.

## The smallest useful annotation

```md
Intent set: Player / Overlay
Decision [STYLE-1]: use semantic theme roles for shared visual properties.
Why: one change should not require editing every screen.
Precedent: [STYLE-1] actual theme implementation and its constraints.
Local realization: apps/player/theme.ts [or “not implemented yet”].
Evidence: no hardware verification yet; TV input remains separate.
References:
[STYLE-1] pinned GitHub file; relevant class/function/test; what was examined.
```

These are illustrative field names, **not a compulsory template**. Cite each significant algorithm/interaction choice once in the most local authoritative set. Derived sets link back to it. Do not force annotations for syntax, trivial glue, or every line of code.

When an agent questions a prior design, it should produce a **competing reference or testable counterexample** rather than an ungrounded aesthetic preference. “My model usually does it this way” is not evidence; nor is an old source automatically correct. If a prior mechanism is genuinely inadequate, keep the original reason and reference in the history of the superseded decision.

## Verified GitHub implementation examples

These examples were inspected as **actual source files** on 2026-11-03. They illustrate the practice; they do not claim that Logical Cloud already implemented the patterns or that their code works in our environment.

### [STYLE-1] Centralized component theme with explicit local variations

Source: [Flutter Material `theme_data.dart` at commit `319ffb414d2edaf9cd83861117e937e3af3be961`](https://github.com/flutter/flutter/blob/319ffb414d2edaf9cd83861117e937e3af3be961/packages/flutter/lib/src/material/theme_data.dart). Git blob observed: `03402d3341f223ed0789c256115ae7657b80bff5`.

**What was observed:** a shared Material theme implementation importing and composing many component-specific theme classes. This is precedent for centralized semantic styling plus explicit component-specific adaptation, **not** a guarantee that all styling can live in one universal file.

**Potential local use:** factor semantic visual choices apart from playback logic or device input. **Local result:** not implemented or benchmarked by this reference.

### [L10N-1] Concrete localization configuration entrypoint

Source: [Mozilla Bedrock `l10n/l10n-pontoon.toml` at `b8aaef5ef32485a86d19dfbd01e76287290492f0`](https://github.com/mozilla/bedrock/blob/b8aaef5ef32485a86d19dfbd01e76287290492f0/l10n/l10n-pontoon.toml). Git blob observed: `b8524c9e26385bd7d8a34615a7f7c3cdfcff12c1`.

**What was observed:** the localization entrypoint includes `configs/pontoon.toml` while explicitly excluding vendor and special-template configuration. This illustrates authoritative scoping of localization configuration; **it is not a demonstrated runtime translation algorithm**.

**Potential local use:** keep locale policy and text authority separate from domain behavior; test layout/locale intersections. **Local result:** not implemented or benchmarked by this reference.

### [CI-1] Scoped workflow based on affected paths

Source: [GitHub Docs `.github/workflows/all-documents.yml` at `396218f23a6e3fa24d173ebfa74b3499adde67a3`](https://github.com/github/docs/blob/396218f23a6e3fa24d173ebfa74b3499adde67a3/.github/workflows/all-documents.yml). Git blob observed: `0a9d3c0b4ed02f377cd26d5e5ac2795c0c5cc3ad`.

**What was observed:** `pull_request.paths` limits triggering to a script subtree, package manifests, or the workflow file. The workflow requests read-only repository permission and tests a particular script. Its internal-repository guard matters; a public fork should **not** assume identical execution.

**Potential local use:** scope cheap checks to truly implicated sets while retaining important cross-set checks. **Local result:** Logical Cloud currently runs a separate `.github/workflows/ci.yml`; this pattern has not been adopted as a change.

### [SIM-1] Our existing simulator and local checks

Source: [Logical Cloud simulation engine](https://github.com/JadanPoll/Logical_Cloud/blob/f9fcdf69e190880a1209ba69695efa9ded1033c5/logical_cloud/simulation.py) and [simulator tests](https://github.com/JadanPoll/Logical_Cloud/blob/f9fcdf69e190880a1209ba69695efa9ded1033c5/tests/test_simulator.py).

**What was observed:** a deterministic model of work placement and related invariants. The previous simulator workflow succeeded; it is an existing implementation to inspect before rewriting placement policy.

**Limit:** this does not verify execution on remote workers or empirical latency on a physical device.

## Source-selection preference

Use the cheapest credible progression: *existing working project implementation → specific external implementation and tests → concrete reproduction/issue/PR discussion → authoritative documentation or research paper → explicitly labeled novel hypothesis*. A source can be authoritative for an interface yet inadequate for an implementation pattern; match the kind of claim to the kind of evidence.

If no suitable example is available, state what was searched, why it did not transfer, what is original, and what bounded test might refute it. **Novelty is allowed by exception, never laundered into an apparently verified design.** A sourced approach still needs local checks proportional to the risk.

## An onboarding and disagreement trace

For an unfamiliar set, retrieve its parent purpose, intent certificate, decision annotations, end-of-set References, local adaptation, and the most relevant tests. A newcomer can then challenge a specific premise or provide another pinned code precedent and discriminating evidence.

**When an agent disagrees**, record: disputed rule/decision ID, exact claim, old source and local evidence, alternative source or counterexample, scoped experiment, and disposition (retain/try alongside/supersede). Preserve previous rationale instead of erasing it. This is the point of both the research-paper analogy and the formal [rule certificate](axiom-calculus.md): to make correctness and errors *inspectable across independent agents*.

## Maintenance and stopping

Reference IDs should be stable; superseding an interpretation should not silently alter the meaning of the old reference. Prefer source permalinks to immutable commits/tags. Citation checking should not require duplicating an entire bibliography into each overlapping set; use one canonical ledger and link it.

Do not mistake scholarship for progress. A one-line correction may require no new source, while replacing an architecture without having inspected a single real implementation merits a strong warning. Every additional trace should earn its retrieval and diagnostic value.