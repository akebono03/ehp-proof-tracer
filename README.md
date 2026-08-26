# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to build a proof tracer that can explain how homotopy
groups of spheres are determined from mathematical input such as:

- EHP exact sequences
- composition relations
- Toda brackets
- Steenrod operations
- Hopf invariants
- stable-range results
- known element orders and relations
- literature references

The project deliberately separates:

```text
mathematical rule / theorem
```

from:

```text
generic inference mechanism
```

and from:

```text
abelian-group calculation
```

so that each layer can evolve independently.

---

# Current status

The project has completed the foundations of:

1. finitely generated abelian-group calculation,
2. EHP exact-sequence calculation,
3. proof / relation representation,
4. a generic fixed-point inference engine.

The current architecture is:

```text
EHP domain inference rules
        ↓
generic proof / inference engine
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

At the completion of Phase 5-65, the generic inference engine is treated as
a completed foundation.

Phase 6, the first EHP domain-inference vertical slice, is completed.

The completed Phase 6 path connects domain-specific EHP facts to generic
relation reasoning:

```text
Image / Kernel facts
↓
EHP exactness
↓
EHP zero composition
↓
generic ZERO relation
↓
equality symmetry / transitivity / closure
↓
ZERO propagation
↓
derived relation
```

Phase 6 completion does not mean that all EHP or unstable-homotopy theorems
have been encoded. It means that the first representative domain rule family
can be executed end-to-end by the Phase 5 generic fixed-point engine without
adding EHP-specific branches to that engine.

---

# Development status

- Phase 1: finite abelian-group calculations — completed
- Phase 2: structured subgroup calculations — completed
- Phase 3: quotient groups, exact sequences, extensions, and EHP inference — completed
- Phase 4: presentation-based calculations with free components — completed
- Phase 5: generic proof / inference engine foundation — completed
- Phase 6-1: Image + Kernel → Exactness — completed
- Phase 6-4/5: Exactness ↔ Image / Kernel structure propagation — completed
- Phase 6-7: Exactness → EHP zero composition — completed
- Phase 6-9: EHP zero composition → generic ZERO relation — completed
- Phase 6-11/13: ZERO propagation through equality — completed
- Phase 6-14: equality symmetry — completed
- Phase 6-16: equality transitivity — completed
- Phase 6-18: equality equivalence closure — completed
- Phase 6-19: equality closure → ZERO propagation — completed
- Phase 6-20: EHP → equality closure → ZERO propagation integration — completed
- Phase 6-21: representative Phase 6 end-to-end completion test — completed
- Phase 6: EHP domain-inference foundation — completed

---

# Algebra layer

## Finitely generated abelian groups

The algebra layer is designed for groups of the form:

```text
Z^r ⊕ finite torsion
```

including examples such as:

```text
0
Z
Z^2
Z/2
Z/4
Z/2 ⊕ Z/4
Z ⊕ Z/2
Z ⊕ Z/4
```

The general calculation path is presentation based:

```text
group presentation
↓
relation matrix
↓
integer lattice
↓
Hermite normal form
↓
Smith normal form
↓
kernel / image / cokernel
```

This avoids finite-element enumeration when free components are present.

## Finite-group reference implementation

The earlier finite-group enumeration algorithms are retained as an
independent reference implementation.

For small finite groups they can explicitly calculate:

- group elements
- subgroups
- generators
- kernels
- images
- quotient cosets
- quotient structures

Finite enumeration and presentation-based calculations can therefore be
cross-checked independently.

## Homomorphisms

Homomorphisms are represented by integer matrices.

The algebra layer supports cases including:

```text
finite → finite
finite → free
free → finite
free → free
mixed → mixed
```

and handles non-diagonal maps, zero groups, and zero maps.

For:

```text
f : G → H
```

the presentation-based path can calculate abstract structures for:

```text
Ker(f)
Im(f)
Coker(f)
```

## Exact sequences

For:

```text
A --f--> B --g--> C
```

the algebra layer can calculate:

```text
Im(f)
Ker(g)
B / Im(f)
Im(g)
```

and determine exactness through:

```text
Im(f) = Ker(g)
```

as a subgroup/lattice condition.

The abstract-group relationship:

```text
B / Im(f) ≅ Im(g)
```

is treated separately from exactness itself.

This distinction is important:

```text
subgroups are equal
```

is not the same statement as:

```text
abstract group structures are isomorphic
```

## Extensions

For finite short exact sequences:

```text
0 → A → B → C → 0
```

the middle group need not be unique.

The project can enumerate finite abelian candidate structures and test
whether they can occur as valid extension middle groups.

The extension-candidate enumeration remains primarily finite-group
functionality.

---

# EHP layer

For an EHP segment:

```text
π_{n+k-1}(S^{n-1})
        --E-->
π_{n+k}(S^n)
        --H-->
π_{n+k}(S^{2n-1})
        --P-->
π_{n+k-2}(S^{n-1})
```

the project can:

- construct E, H, and P homomorphisms from data,
- calculate images and kernels,
- test exactness,
- calculate general finitely generated abelian-group structures,
- construct exact-sequence objects,
- compare quotient and image structures,
- infer finite middle-group candidates from extension data.

The EHP layer delegates general group-theoretic calculation to the algebra
layer.

The algebra layer does not know the homotopy-theoretic meaning of E, H, or P.

---

# Proof / relation model

## Relation

`Relation` represents a known mathematical relation or fact.

Its current structure includes:

```text
lhs
rhs
relation_type
source
note
```

`RelationType` currently contains:

```text
EQUALITY
ZERO
ORDER
```

A relation may contain structured mathematical expressions, strings, or
other values.

The relation object is intentionally more general than only one specific
homotopy-expression type.

## LiteratureReference

Structured literature metadata can be represented through:

```text
label
author
title
year
locator
```

This keeps mathematical-source information attached to known relations
without making it part of the algebra layer.

## ProofStep

A `ProofStep` represents one derivation or calculation:

```text
premises
↓
rule
↓
conclusion
```

A step can preserve:

- its conclusion,
- explicit premise `ProofStep` objects,
- a `ProofRule`,
- a note,
- the `InferenceRule` that generated it.

## Proof

A `Proof` stores a conclusion and an ordered collection of `ProofStep`
objects.

Dependencies are represented through step premises.

A separate graph class is not currently required for the generic inference
engine because `ProofStep.premises` already preserves derivation
dependencies.

---

# Expression model

The expression layer provides structured mathematical expressions such as:

```text
Zero
HomotopyElement
Multiple
Composition
```

and generator helpers such as:

```text
eta(n)
nu(n)
sigma(n)
```

The expression layer represents mathematical structure.

It does not itself perform:

- algebra calculation,
- expression normalization,
- dimension validation,
- theorem application,
- EHP inference.

`HomotopyElement` and algebra-layer `GroupElement` are deliberately separate
concepts.

---

# Generic inference engine

Phase 5-65 is the completion point of the generic inference-engine
foundation.

The current pipeline is:

```text
known ProofSteps
+
InferenceRules
↓
premise-pattern search
↓
all valid premise assignments
↓
relation-pattern matching
↓
PatternVariable bindings
↓
shared-binding consistency
↓
InferenceMatch
↓
conclusion construction / substitution
↓
candidate ProofSteps
↓
application classification
↓
new ProofSteps
↓
next round
↓
fixed point
```

## InferenceRule

An `InferenceRule` can contain:

```text
name
description
premise_patterns
conclusion_builder
conclusion_pattern
match_guard
```

The conclusion may be produced either by:

```text
conclusion_builder
```

or by:

```text
conclusion_pattern + bindings
```

If both are present, the builder currently takes precedence.

## PremisePattern

A premise pattern can constrain:

```text
proof_rule
statement_type
statement_pattern
relation_type
relation_pattern
```

This supports both outer structural matching and structured `Relation`
matching.

## PatternVariable

`PatternVariable` represents a variable inside a rule pattern.

For example:

```text
Relation(
  lhs=?x,
  rhs=?y,
)
```

can match:

```text
Relation(
  lhs=alpha,
  rhs=beta,
)
```

to produce:

```text
?x = alpha
?y = beta
```

## VariableBinding

A `VariableBinding` explicitly records:

```text
pattern variable
→
actual value
```

Bindings may contain arbitrary values.

## Binding consistency

Bindings are merged only when repeated variables have the same value.

For example:

```text
?x = alpha
?x = alpha
```

is consistent, while:

```text
?x = alpha
?x = beta
```

is rejected.

This consistency applies:

- inside one relation pattern,
- across multiple premise patterns,
- across three or more premises,
- with multiple shared variables.

## Exhaustive premise assignment search

The canonical assignment search is:

```python
find_all_matching_premises()
```

It uses deterministic depth-first backtracking.

It enumerates all valid ordered assignments while preventing reuse of the
same available-step index inside one assignment.

Compatibility APIs remain available:

```text
find_matching_premises()
find_inference_match()
```

and return only the first result.

Per-rule all-match search is available through:

```text
find_inference_matches_for_rule()
```

while collection-level:

```text
find_inference_matches()
```

collects all matches from all rules.

## Shared bindings across premises

Multi-premise matching enforces shared-variable consistency.

Conceptually:

```text
premise 1:
x → y

premise 2:
y → z
```

only matches assignments in which the value bound to `y` is the same in
both premises.

Backtracking continues past inconsistent candidates and can find later
consistent assignments.

## InferenceMatch

An `InferenceMatch` stores:

```text
inference_rule
premises
bindings
```

Thus the execution trace can answer both:

```text
which premises matched?
```

and:

```text
which values were bound to the rule variables?
```

## Conclusion substitution

Bindings can be substituted into structured conclusion patterns,
including Relation objects and dataclass-based statements such as
ExactnessStatement.

Conceptually:

```text
bindings:
x = alpha
z = gamma

conclusion pattern:
x → z

derived conclusion:
alpha → gamma
```

The current substitution helpers include:

```text
lookup_variable_binding()
substitute_pattern_value()
substitute_relation_pattern()
substitute_inference_conclusion()
```

## Rule application

`apply_inference_match()` produces a `ProofStep` whose premises are the
matched steps.

The generated step uses:

```text
ProofRule.INFERENCE
```

and stores the originating `InferenceRule`.

## Multiple assignments and multiple conclusions

One rule may match multiple binding assignments.

Different assignments may therefore produce different conclusions.

The engine supports:

- one premise with multiple bindings,
- multiple premises with multiple shared-binding assignments,
- multiple variables,
- partially shared variables,
- variables propagated through three premises,
- several shared variables propagated through three premises.

---

# One-round execution trace

A detailed round result is represented by:

```text
InferenceRoundResult
├── matches
├── application_results
├── candidate_steps
├── new_steps
└── duplicate_rejected_steps
```

Each application result stores:

```text
InferenceApplicationResult
├── match
├── candidate_step
├── accepted
└── rejection_reason
```

The current rejection reasons are:

```text
ALREADY_KNOWN
SAME_ROUND_DUPLICATE
```

Their meanings are:

```text
ALREADY_KNOWN
=
the candidate conclusion existed before the round

SAME_ROUND_DUPLICATE
=
an equal conclusion was accepted earlier in the same round
```

The accumulated knowledge state stores only the first accepted step for an
equal conclusion.

Alternative applications remain visible in the execution trace.

---

# Fixed-point inference

The engine supports automatic repeated inference through:

```python
run_inference_until_stable()
```

and detailed execution through:

```python
run_inference_until_stable_with_history()
```

The structured run result is:

```text
InferenceRunResult
├── steps
├── round_results
├── round_history
├── round_count
└── termination_reason
```

`round_results` stores productive rounds only.

`round_history` is a compatibility view exposing only each round's
`new_steps`.

`round_count` is the number of productive rounds.

The final non-productive fixed-point check is not stored as a round result.

## Termination reasons

The engine distinguishes:

```text
FIXED_POINT
MAX_ROUNDS
```

A fixed point is reported only after an inference check actually produces no
new step.

`MAX_ROUNDS` means the configured productive-round limit was reached; it does
not assert mathematical saturation.

`max_rounds=0` is valid and performs no productive round.

---

# Branching and merging

The Phase 5 engine has been verified beyond simple linear chains.

It supports inference graphs involving:

```text
branch
↓
multiple intermediate conclusions
↓
later propagation
↓
merge
↓
further derivation
↓
fixed point
```

The final Phase 5 integration tests cover:

- a shared-binding graph that branches and merges,
- branch/merge graphs producing multiple final bindings,
- multiple rules chained through derived conclusions,
- multiple rules propagating multiple binding branches,
- multiple branches merged by a later multi-premise rule.

The last case is the Phase 5-65 completion test.

Conceptually:

```text
initial facts
├── branch A
└── branch B

round 1
├── intermediate A
└── intermediate B

round 2
└── later rule consumes both intermediate facts

termination
└── fixed point
```

Dependencies are preserved because the final `ProofStep` directly stores the
intermediate steps as premises.

---

# Current limitations

The following are current limitations after Phase 6-3.

## Conclusion equality

Duplicate detection currently uses ordinary Python equality:

```python
step.conclusion == known_conclusion
```

It does not yet use:

- mathematical equivalence,
- canonical forms,
- normalization,
- theorem-aware equivalence.

## Alternative proofs

Alternative rule applications are preserved in round/application traces, but
the accumulated knowledge state stores only the first accepted `ProofStep`
for an equal conclusion.

The engine does not yet maintain a first-class collection of multiple proof
objects for one conclusion.

## Pattern language depth

The generic pattern system currently has direct structured support for
`Relation` patterns and dataclass statement fields.

Phase 6-2 also provides structured matching for dataclass-based statements.
`PremisePattern.statement_pattern` can match statement fields using
`PatternVariable` and literal values. The current EHP statement patterns can
therefore bind `ImageStatement.group_map` and `KernelStatement.group_map`
while preserving shared binding consistency across premises.

It is not yet a general recursive unification engine over every possible
expression / statement class.

## Unbound variables in conclusion patterns

Current substitution semantics return `None` for an unbound
`PatternVariable`.

Domain rules should therefore ensure that variables needed in a conclusion
are bound by their premises.

A stricter validation policy may be added later if real EHP rules require it.

## Search complexity

Exhaustive premise assignment can grow combinatorially.

The current engine prioritizes correct deterministic semantics over
performance optimization.

It does not yet implement:

- indexing,
- search pruning,
- memoization,
- agenda-based semi-naive evaluation,
- rule prioritization.

These should be considered after real Phase 6 rule sets expose actual
performance requirements.

## Termination

`max_rounds` is a safety bound, not semantic cycle detection.

The engine does not yet detect:

- symbolic cycles,
- repeated abstract states beyond conclusion deduplication,
- unbounded families of distinct conclusions.

---

# Phase 5 completion boundary

Phase 5 is considered complete because the engine now has the mechanisms
needed to test real mathematical rules:

```text
multiple premises
all assignments
pattern variables
bindings
shared-binding consistency
structured conclusion substitution
multiple conclusions
multiple rules
multi-round propagation
branching
merging
fixed-point execution
execution tracing
```

Further generic-engine work should be driven by Phase 6 domain needs rather
than by speculative generalization.

---

# Phase 6: EHP domain inference rules

Phase 6 moves from building generic inference machinery to encoding and
executing actual EHP-domain mathematics.

The governing rule remains:

```text
new mathematical knowledge
=
new InferenceRule
```

The generic engine is changed only when an actual mathematical rule cannot be
represented correctly with the current rule language.

## Phase 6-1 to 6-3: exactness rule and structured statement support

The first EHP-specific rule derives exactness from image and kernel facts:

```text
Image(first_map)
+
Kernel(second_map)
↓
Exactness(first_map, second_map)
```

Structured dataclass statement matching, statement conclusion substitution,
and `match_guard` allow the argument-free EHP rule to bind maps while keeping
EHP-specific validity checks outside the generic engine.

The original factory-bound form and direct EHP proof-step APIs remain
compatible.

## Phase 6-4/5: exactness and Image / Kernel structure propagation

Exactness can propagate subgroup structure in both directions:

```text
Exactness(first_map, second_map)
+
Image(first_map, structure)
↓
Kernel(second_map, structure)
```

and:

```text
Exactness(first_map, second_map)
+
Kernel(second_map, structure)
↓
Image(first_map, structure)
```

These rules reuse the same statement-pattern and shared-binding mechanism.
No new generic-engine branch is required.

## Phase 6-7: exactness implies EHP zero composition

A true EHP exactness statement implies that the consecutive maps compose to
zero. The domain-specific intermediate statement is:

```text
EHPZeroCompositionStatement(
  first_map,
  second_map,
)
```

The fixed-point tests verify that Image + Kernel can derive exactness in one
productive round and the EHP zero-composition statement in the next.

## Phase 6-9: EHP zero composition becomes a generic ZERO relation

The EHP-specific zero-composition statement is translated into the generic
relation layer:

```text
Relation(
  lhs=Composition(second_map, first_map),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

This is the bridge from EHP-specific reasoning to reusable relation-level
reasoning.

## Phase 6-11/13: ZERO propagation through equality

If a composition is known to be zero and another expression is equal to that
composition, the ZERO fact can be transferred to the equivalent expression.
Both equality orientations are supported:

```text
x = composition
composition = 0
↓
x = 0
```

and:

```text
composition = x
composition = 0
↓
x = 0
```

The ZERO rules deliberately require the known-zero expression to be a
`Composition`.

## Phase 6-14: equality symmetry

Generic equality symmetry is represented as an inference rule:

```text
x = y
↓
y = x
```

Fixed-point execution rejects already-known reverse conclusions and therefore
terminates under ordinary conclusion equality.

## Phase 6-16: equality transitivity

Generic equality transitivity is represented as:

```text
x = y
+
y = z
↓
x = z
```

Multi-round tests verify closure across longer equality chains.

## Phase 6-18: equality equivalence closure

Symmetry and transitivity are run together under fixed-point inference.
For a connected component of equality facts, the engine derives all directed
pairwise equalities, including reflexive equalities that arise through the
combination of symmetry and transitivity.

The closure is not implemented as a special graph algorithm. It emerges from
the generic rule engine plus duplicate rejection.

## Phase 6-19: equality closure propagates ZERO

ZERO propagation can consume equalities derived in earlier rounds. Therefore
a ZERO fact attached to one expression can travel through a multi-link
equality component and eventually derive ZERO for another expression.

## Phase 6-20: EHP → equality closure → ZERO propagation integration

The EHP rule chain and the generic relation rules are executed together:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
generic composition = 0

external equality facts
↓
symmetry + transitivity
↓
target = composition

composition = 0
+
target = composition
↓
target = 0
```

This verifies that an EHP-domain fact can cross into generic equality
reasoning and produce a new generic mathematical relation.

## Phase 6-21: representative end-to-end completion scenario

The Phase 6 completion test runs the representative rule set together:

```text
Image + Kernel → Exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
ZERO + equality → propagated ZERO
equality symmetry
equality transitivity
```

The test verifies that the final target ZERO relation is derived, that
premise dependencies and source `InferenceRule` references are preserved,
and that an additional inference round produces no new steps.

Thus the whole representative Phase 6 rule set reaches a genuine fixed point.

## Phase 6 completion boundary

Phase 6 is complete because the project can now execute this vertical slice:

```text
EHP structural facts
↓
EHP-specific inference
↓
generic Relation
↓
generic equality reasoning
↓
ZERO propagation
↓
traceable derived relation
↓
fixed point
```

Phase 6 completion does not include every future homotopy-theoretic rule.
In particular, the following remain future domain-rule families rather than
Phase 6 completion requirements:

- element-order reasoning,
- broader suspension relations,
- Hopf-invariant theorems,
- stable-range theorems,
- Toda relations,
- Toda brackets,
- Steenrod operations,
- double EHP,
- odd-primary-specific theorem families.

The next phase should therefore start from a new mathematical rule family,
not from speculative generic-engine refactoring.

---

# Tests

Run all project tests with:

```powershell
python -m pytest -v
```

Run the generic inference-rule tests with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

Run the Phase 6 domain-rule tests with:

```powershell
python -m pytest tests/test_ehp_rules.py tests/test_relation_rules.py -v
```

The Phase 6-21 representative completion test is:

```powershell
python -m pytest tests/test_ehp_rules.py::test_phase6_representative_end_to_end_scenario_reaches_fixed_point -v
```

Latest verified full project result after Phase 6-21:

```text
691 passed in 22.77s
```

The run collected 691 tests and completed with no failures.

---

# Documentation

- `README.md` — current project capabilities and status
- `docs/design.md` — current design principles and architectural boundaries
- `docs/development_log.md` — chronological implementation history

Historical phase descriptions should be read as descriptions of the state at
that phase.

When an older section says that a feature was "not yet implemented", that
statement is historical and must not be interpreted as a current limitation
if a later phase implemented it.
