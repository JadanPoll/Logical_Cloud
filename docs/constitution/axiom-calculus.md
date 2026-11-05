# Axiomatic constitution: obligations, evidence, and falsifiable compliance

This document specifies the **operational reading** of [the Logical Cloud Constitution](../../CONSTITUTION.md), not a general mathematical proof of software correctness. Its purpose is to make agent behavior **accountable to stable numbered rules** and to permit a specific kind of criticism: *the agent followed the governing rule under the recorded conditions, but the result failed, so the rule or its assumptions need revision*.

## 1. The judgment we want to make

Represent a consequential decision by a record `D = (q, c, a, b, e)`: the user's question or intent `q`, observed context `c`, action `a`, applicable baseline `b`, and evidence `e`.

A provision such as `LC-14.01` is **not just advice**. It has an interpretable five-part shape:

| Part | Meaning |
|---|---|
| **When** | Scope/antecedent: under what circumstances the provision applies |
| **Must** | The action, invariant, or decision obligation |
| **Witness** | Smallest independently inspectable evidence that the obligation was met |
| **Unless** | Legitimate exception or alternate route, with its justification |
| **Failure signature** | What observable behavior would contradict the obligation |

For a clause `r`, write `A_r(D)` for its applicability, `O_r(D)` for its required obligation, `X_r(D)` for an allowed exception, and `E_r(D)` for the evidence sufficient to assess that claim.

A useful engineering form is:

`A_r(D) ∧ ¬X_r(D) ⇒ O_r(D)`.

This is **an obligation conditional on known facts**, not a proof that every user goal, software state, or requirement can be decided formally. Missing observations remain **unknown**, not false. Rules about human intent and future utility often require an explicit, challengeable interpretation.

**Rule of evidence:** `Agent says it complied` is never by itself a witness. The witness must point to inspectable facts: file/commit diff, pinned source, invocation trace, user-visible behavior, test output, documented decision, or sufficiently narrow explanation for why the rule did not apply.

## 2. A compact kernel of derived operational axioms

These are deliberately small interpretations of existing addressable clauses. Their complete language and exceptions remain in [CONSTITUTION.md](../../CONSTITUTION.md). Do not silently turn a broad principle into a new mandatory procedure by citing this table.

| Governing provision | When it applies | Required invariant | Minimal way to challenge it |
|---|---|---|---|
| **LC-01.01–01.02** Purpose and preservation | Proposing a nontrivial change | Proposed action addresses the operative user goal and preserves unexplored existing obligations | Show goal mismatch or removed behavior without examined constraint |
| **LC-02.01–02.04** Factorization | A concern varies or repeats across parts of a project | One meaningful factor has a discoverable authority; complexity of indirection must be earned | Demonstrate needless change fan-out or unjustified abstraction |
| **LC-03.01–03.05** Intent sets | A task touches a consequential capability set | Relevant parent purpose, local promise, and intersecting obligations are recoverable; certificates do not imply test success | Missing/contradictory promise or implementation assertion unsupported by evidence |
| **LC-04.01–04.04** Cross-cutting substitutions | Style, locale, form factor, or variant changes | Semantics and shared rules are factored from genuine surface-specific behavior | Same semantic choice copied and manually propagated, or meaningful physical difference hidden |
| **LC-05.01–05.05** Parallel agent work | Multiple candidates or agents act on a common project | Independent work remains recoverable; actual shared-contract conflicts surface rather than disappear | Unrelated work blocked, variant lost, or incompatibility silently combined |
| **LC-06.01–06.05** Self-play | Iterative investigation can answer a consequential question | Each useful experiment relates an explicit question to variation, result, and next decision; model ≠ reality | Repeated trials with no discriminating information or simulations called physical evidence |
| **LC-07.01–07.04** Context recovery | A new agent or interrupted agent resumes | It can locate the relevant intent, decisions, source anchors, and implementation without broad oral-history reconstruction | Repeated full-codebase rediscovery or contradictory authoritative descriptions |
| **LC-08.01–08.04** Location independence | Code/data/execution placement varies | Observable contract and capability/authority boundaries are explicit | Pretending remote hardware or permissions are local and unconditional |
| **LC-09.01–09.04** Experiment evidence | Comparing alternatives or performance | Baseline and changed factors are known; evidence type and uncertainty are stated | Incomparable variants, simulated figures presented as measurements, or unjustified risk |
| **LC-10.01–10.04** User experience | Work involves a human intent or troubleshooting | Feedback and consequential failure are intelligible; unrelated work is not unnecessarily held hostage | Silent failure, uncopyable diagnostic, or optional check blocks a fresh request |
| **LC-11.01–11.04** Selective automation | Verification/integration is needed | Proportionate tests and independent evidence; promotion authority distinct from proposal | Vacuous expensive test gate, hidden failure, or unauthorized deployment |
| **LC-12.01–12.04** Whole-flow efficiency | Evaluating architecture or workflow improvement | Count context rebuilding, integration, and future change cost as well as local speed | A locally faster process causes larger total user/agent overhead |
| **LC-13.01–13.04** Constitutional economy | Adding/revising a rule or ceremony | Rule identity persists and procedure earns its benefit | Versioned obligation silently changes, or compliance work dwarfs avoided failure |
| **LC-14.01–14.09** Source precedent | A consequential mechanism is chosen or disputed | Relevant actual code precedent investigated where available, cited and distinguished from local verification; originality declared when necessary | Vague homepage citation, fabricated inspection, training-preference rewrite, or unmarked invention |
| **LC-15.01–15.10** Certification/amendment | A consequential change is claimed compliant or a failure challenges the rules | Rule applicability, evidence, outcome, and competing explanations are separately recorded with a small audit trail | Self-attested proof, conflated compliance/outcome, or retroactive renumbering to evade criticism |
| **LC-16.01–16.06** Human vision and agent delegation | A person expresses broad intent, changes their mind, or onboards/scales agents | Agents offer concise meaningful outcome-level choices only when needed, own routine technical uncertainty, preserve reversible factors, and provide purpose/contract/precedent/evidence handoffs | Human forced to choose internals, repeat project history, reconcile agents, or accept unsupported claims of completion |

A constitutional clause **can be advisory, conditional, or mandatory**. The word “must” here states obligations *after* the clause is applicable, subject to its explicit exceptions and the anti-bureaucracy rule. It does not turn every trivial edit into a large compliance report.

## 3. Four-valued conformance and independent outcome

A specific clause gets one of four verdicts:

- **Supported** — the clause applied and inspectable evidence supports the required behavior (or a legitimate exception, explicitly identified).
- **Violated** — it applied, and evidence establishes a contradictory action.
- **Undetermined** — applicability or obligation compliance could not be established from available evidence.
- **Not applicable** — the antecedent did not hold, with the relevant reason.

Separately, the **outcome** is `met goal / failed goal / not yet established`. A successful build is not evidence that the requested user experience was achieved; a failed build does not prove an unrelated architectural clause was violated.

There are **two independent axes**: adherence to the method, and success against the actual objective. An honest failure can be more useful than an untraceable success.

**Constitution-following failure:** A case may support `faithful application + goal failure` only when the relevant applicable rules, checked obligations, exception decisions, and observed failure are independently inspectable to the declared scope. This is not a claim of absolute proof of all possible hidden constraints; call the result *supported under examined evidence*, and preserve unknowns.

**Constitution violation:** A failure attributable to the agent ignoring an applicable rule should first be corrected as an application error; do not rewrite the rule merely to excuse the agent.

**Constitution inadequacy:** If the agent plausibly satisfied the applicable rules but actual user behavior still failed, question the premise, completeness, abstraction, or interactions of the rule itself. Reproduce a discriminating failure and propose an amendment rather than endlessly adding ritual verification.

## 4. The minimal rule certificate

For consequential changes, retain the smallest sufficient **certificate**, next to the intent set or change history. An ordinary one-factor edit may need only a couple of lines and links.

```yaml
change: "TV pause overlay stays visible longer"
baseline: "<commit/variant>"
goal: "Remote-control playback remains legible and predictable"
rules:
  - id: LC-02.02
    applies: yes
    witness: "theme token or single authoritative override + diff link"
    verdict: supported
  - id: LC-14.01
    applies: yes
    witness: "[STYLE-1] inspected code precedent + applicability note"
    verdict: supported
  - id: LC-09.02
    applies: yes
    witness: "simulated timing only; TV observation not yet available"
    verdict: undetermined
outcome: "preview generated; on-device behavior not yet established"
unknowns: ["Fire TV remote long-press event variance"]
```

This illustrative YAML is a **human-readable example**, not a required exact schema, existing tested workflow, or newly introduced bureaucracy. Cite only the rules that materially governed a decision and any consequential unresolved obligation. Other clearly applicable obligations remain real even if not listed: a certificate is not a magic exemption from the constitution.

For independent agents, the baseline and certificate travel together. A newcomer should not convert a previously `undetermined` claim into `supported` merely because it expects the code to work.

## 5. Counterexample and amendment procedure

When a result contradicts expectations, retain a small *failure case*, not just a generic “CI failed” message:

1. **Target and evidence:** What user-visible or system-observable promise failed? Record a reproducible witness if possible.
2. **Applicability:** Which numbered rules should have governed this action, given the information actually available to the agent at decision time?
3. **Compliance audit:** For those rules, which actions are supported, violated, undetermined, or inapplicable? Identify the exact source/diff/test for each material claim.
4. **Rival explanations:** Did the agent disobey? Was the rule ambiguous, incomplete, mutually conflicting, or based on false assumptions? Did an upstream reference fail to transfer to our context? Is the test or abstract model wrong?
5. **Discriminating action:** Choose the smallest realistic observation, comparison, or counterexample that could distinguish the explanations.
6. **Disposition:** Correct application, reinterpret a clause, record a provisional exception, or propose a versioned amendment. Preserve the old statement and reason so future agents can see the change.

A rule amendment should contain: `old clause/version → failure witness → proposed new antecedent/obligation/exception → how it would change this case → expected side effects on other cases`. Do not silently alter the definition of an existing ID. Add a new subclause or mark a rule superseded with an explicit mapping.

**Counterexample is not automatically repeal.** A failure may arise from an uninspected device constraint, an irrelevant test, a bad simulator, or a bug in the adaptation. The point of the calculus is to make those different explanations inspectable.

## 6. Worked constitutional counterexample

**User intent:** “Make the TV overlay readable with a remote; keep the player working.” An agent consults a theme implementation, changes the centralized style factor, produces two previews, and checks its unit tests.

**Observed failure:** On the actual television, remote focus disappears after a key-up event, making the enlarged overlay unusable.

**Audit:** `LC-02.02` may be **supported** (one source of style truth); `LC-14.01` may be **supported** (an actual theme precedent was examined); `LC-09.02` is **violated** only if a simulated preview was presented as measured device success. If the agent correctly labeled the preview as synthetic and no actual TV validation was feasible at that stage, the experimental evidence may be compliant but insufficient to claim successful delivery. `LC-04.03` remains relevant because remote input needs its own adaptation.

**Discrimination:** Replay a representative TV key-up/held/OK sequence, compare the focus state with the baseline, and determine whether the physical event model or the style change causes the failure. One can then amend a concrete rule about input composition, improve the implementation, or preserve an unresolved device limitation. Do **not** conclude “the constitution worked” merely from the agent's own narrative.

## 7. Foundational precedents and stopping rules

This operational calculus inherits RSM's numbered method traces, separation of models/evidence, and question-conditioned stopping; REM's practical failure-led refinement and realistic flows; and FKEN's small, recoverable source-anchored certificates. See [source projection](sources.md) and [code precedent ledger](provenance.md).

**Stop auditing when it is no longer decision-relevant.** The purpose is to make a repeated failure diagnosable and a legitimate amendment justified—not to prove, in mathematical logic, that every side effect of an arbitrary program is correct.