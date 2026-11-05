# Algebraic design spaces — an engineering language for unfinished ideas

**Purpose:** Extend Logical Cloud's factor-substitution method beyond
distributed placement into *designing the application itself*. When a human
wonders "what could Compute look like?" or "could agents develop a 3D game?",
an agent should identify the relevant variables, consequences, dependencies,
and next discriminating questions **without first deciding the architecture
or asking the human to administer it**.

This is a refinement of the existing constitution, not a competing
philosophy or a new product area. In particular:

- [LC-02](../CONSTITUTION.md) favors factored, substitutable capabilities.
- [LC-16 and the intent sets](constitution/intent-sets.md) distinguish human
  holistic purpose, functional contracts and actual implementation evidence.
- [LC-08 and execution algebra](architecture.md) already separate application,
  fabric, placement, artifacts, state and transport.
- [LC-09, LC-11 and LC-15](constitution/axiom-calculus.md) keep hypotheses,
  simulations, tests and actual outcomes separate.

## 1. A design is a constrained, partially assigned product space

For a human goal `H`, write:

`Candidate = H × F₁ × F₂ × … × Fₙ | Constraints(F₁, …, Fₙ)`

Here `H` denotes **the human's intended experience and invariant
promises**, not an interchangeable technical module. Each `Fᵢ` is a
consequential **question** with several replaceable answers. An assignment
may remain unknown; this is a first-class, desirable state.

The factor set itself is **open to revision**. One may discover another
variable or learn that two factors should be merged or split. Factorization
is a useful model, not a mathematical proof that real-world interactions
are independent. Constraints represent intersections between factors.

One should not generate the entire Cartesian product by default: candidate
enumeration can grow exponentially and most combinations may be irrelevant.
Prefer a few **named, partial candidates**, a specific human question, and
a small experiment that might distinguish them.

## 2. The minimal, optional machine-readable record

For consequential projects, a small JSON record can contain:

| Field | Meaning |
| --- | --- |
| `intent.goal`, `intent.invariants` | Human purpose and stable promises |
| `factors[].id/question/relevance` | Why this variable matters for the human objective |
| `options[].id/meaning/maturity/evidence` | Choices and qualified state of knowledge |
| `variants[].set` | Named, **partial** assignments worth comparing |
| `intersections[]` | Cross-factor requirements or explicitly labeled hypotheses |
| `experiments[].question/witness/status` | The next empirical discrimination and its actual evidence |

A `design_contract` intersection states an **internally declared design
requirement**; it is not external scientific proof. A `hypothesis`
intersection asks for investigation. Both may be revised when actual
observations refute their premises.

Maturity and evidence are **not synonyms**: an option can be proposed with
no local proof; another can be supported by upstream source but be untested
on Fire OS. The current schema requires references for claims of upstream
support, repository implementation, and direct observation. A named
variant that satisfies every declared contract is still only a
`candidate_unverified`, never automatically a working system.

The schema is **not mandatory for every button, helper or quick idea**.
An agent can use the same reasoning in a compact chat response or a
one-paragraph intent certificate. Use JSON where reuse across agents,
comparison, or future revisions justify it.

## 3. Two concrete questions and a runnable tool

The existing simulator continues to handle *quantified runtime* workload
and placement choices. The new pure-Python design-space analyzer provides
**structural analysis**, not timings, code generation, a physical device
check, or deployment:

```bash
# Which questions about Compute still matter?
python -m logical_cloud design examples/design_compute_tv.json

# Inspect a possible agentic work configuration without claiming it works
python -m logical_cloud design examples/design_compute_tv.json --variant agent_work

# Compare ONLY a few deliberately chosen 3D Playroom routes
python -m logical_cloud design examples/design_playroom_3d.json --compare

# Hold the remote-rendering idea fixed, vary presentation, and expose a conflict
python -m logical_cloud design examples/design_playroom_3d.json \
  --variant remote_fidelity --set presentation=local_frames

# Let another agent inspect the same grounded, incomplete design as JSON
python -m logical_cloud design examples/design_playroom_3d.json \
  --variant browser_prototype --json
```

**3D Playroom:** change renderer between WebGL, Android native and streamed
GPU; independently consider simulation locality, controls, assets, scene
language, game state and agent-generated variants. For example, selecting
remote GPU rendering while explicitly assigning a *local frame* presentation
violates a declared option contract. Selecting remote world simulation
without a state-continuity choice is an **open question**, not automatically
a contradiction. Scene language, state and agent workflow can remain
unassigned while the first minigame prototype is built.

**Compute:** vary a **device gallery** versus a **task board** or
desktop-like GUI, paired with remote-only or iPad input, bundled or
live device discovery, actual executors, job dispatch, recoverability
and telemetry. The goal is **productive work from the TV**; a
capability gallery is one valuable partial capability, not proof the
agentic kernel is finished.

**Portability:** an application request varies the execution route,
presentation, controls and placement while keeping its essential
user-facing experience in view. See the current
[Fire portability factor model](https://github.com/JadanPoll/fire/blob/main/docs/PORTABILITY_FACTOR_SPACE.md).
This is the same conceptual language, not a new special-purpose algebra.

**Android Dojo:** an experiment can present the human with factor
alternatives, why they matter, and the smallest test that reveals
something surprising. The *learning objective*, not a mechanical
"correct configuration", is what matters.

## 4. What agents should show the human

An agent need not present every internal variable. Condense analysis to:

1. **What we are trying to achieve:** a one-sentence purpose, confirmed
   or provisional, including what should remain invariant.
2. **The consequential choices:** only the factors that materially
   influence the current question, with tangible alternative experiences.
3. **What's known and unknown:** source-backed facts, contradictory
   assignments, unverified candidate combinations and binding constraints.
4. **What we could do next:** a small, reversible preview or experiment
   chosen for insight, not a to-do list of every conceivable subsystem.
5. **How the answer changes the design:** the specific factor/intersection
   updated by evidence, with a route to revise or roll back.

A person's preference for something enjoyable, visually appealing, or
intuitive is **not a measurement error**. They own the value function.
The agent can be objective about constraints, options, costs and
observations but cannot silently optimize away the human's purpose
using a fake numerical "architecture quality score."

## 5. Non-dependency and evidence boundaries

Two independently staffed subprojects can proceed before an adjacent
factor is decided if their shared contract is sufficiently stable.
This does not mean the final combination is compatible: the relevant
intersection still needs a meaningful check.

Examples of helpful **early stopping points**:

- A 3D game has a playable 2D or block-world prototype that tests the
  input and world-identity contracts before choosing a final renderer.
- The Compute gallery makes physical/virtual capabilities understandable
  before the remote executor is operational.
- A future agent demonstrates two same-intent candidates under one
  changed variable, with measured differences and honest uncertainty.
- An investigation reveals that a proposed factor does not affect
  the human's current decision; drop it from the visible discussion.

Avoid broad speculative machinery until real experiments make its
value legible. The CLI is a **no-dependency, offline, read-only analyzer**.
It does not claim to select an optimal engine, invoke Codex, establish
remote authorization, run experiments, or prove Fire TV compatibility.

## 6. Source and validation witness

The implementation is [`logical_cloud/design_space.py`](
../logical_cloud/design_space.py) with examples and bounded tests
[`tests/test_design_space.py`](../tests/test_design_space.py).
It reuses the repository's existing `ModelError`, standard-library JSON,
named factor assignments and CLI entrypoint, rather than rebuilding the
performance simulator or mandating a global engineering ontology.

**Constitutional assessment:** LC-02 (factorization), LC-04 (intersection
compatibility), LC-09 (experimental evidence), LC-13 (avoid ceremony),
LC-15 (separate adherence from success), LC-16 (human/agent layers) and
LC-17 (make philosophy an executable tool). Passing unit tests verifies
only this small structural analyzer; future human outcomes and real
Playroom/Compute functionality remain separately unverified.
