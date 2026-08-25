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

The next development stage is:

```text
Phase 6: EHP domain inference rules
```

Phase 6-1 through Phase 6-3, including the first EHP domain inference rule
integration and its structured statement support, are completed.

The main goal of Phase 6 is not to add speculative generic-engine features.
It is to encode actual EHP / homotopy-theoretic rules using the Phase 5
engine and extend the engine only when a real domain rule demonstrates a
missing capability.

---

# Development status

- Phase 1: finite abelian-group calculations — completed
- Phase 2: structured subgroup calculations — completed
- Phase 3: quotient groups, exact sequences, extensions, and EHP inference — completed
- Phase 4: presentation-based calculations with free components — completed
- Phase 5: generic proof / inference engine foundation — completed
- Phase 6-1: EHP exactness inference rule — completed
- Phase 6-2: structured statement matching foundation — completed
- Phase 6-3: statement conclusions and match guards — completed
- Phase 6: EHP domain inference rules — in progress

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

Phase 6 moves from:

```text
building inference machinery
```

to:

```text
encoding and executing EHP mathematics
```

Candidate rule families include:

- E/H/P relations,
- EHP exactness consequences,
- suspension relations,
- Hopf invariant relations,
- element-order relations,
- composition relations,
- stable-range results,
- known Toda relations,
- literature-backed relations.

The intended pattern is:

```text
mathematical theorem / relation
↓
InferenceRule
↓
Phase 5 generic engine
↓
derived ProofSteps
↓
proof trace
```

The generic engine should not contain EHP-specific branches.

A new generic feature should be added only if an actual domain rule cannot
be represented correctly with the current rule language.

## Phase 6-1: EHP exactness inference rule

Phase 6-1 adds the EHP-specific rule factory:

```python
ehp_exactness_inference_rule(exact_step)
```

The rule uses existing proof steps:

```text
ImageStatement(E)
KernelStatement(H)
```

to infer an `ExactnessStatement` through the Phase 5 generic inference
engine. The existing `ehp_exactness_proof_step()` constructs and validates
the EHP exactness statement.

The derived `ProofStep` uses:

```text
ProofRule.INFERENCE
```

The originating EHP rule remains available through
`ProofStep.inference_rule`.

Phase 6-1 does not introduce:

- changes to `proof.py`,
- new `ProofRule` values,
- automatic selection of arbitrary EHP segments.

## Phase 6-2: structured statement matching foundation

Phase 6-2 extends the generic matching layer with a domain-independent
structured statement pattern:

```python
PremisePattern(
        statement_pattern=ImageStatement(
                group_map=PatternVariable("first_map"),
                structure=PatternVariable("image_structure"),
        ),
)
```

`match_statement_pattern()` compares dataclass fields and delegates each
field to the existing `match_pattern_value()` and
`merge_variable_bindings()` mechanisms. This supports concrete field values,
field bindings, repeated variables, and shared bindings between premises.

The EHP exactness rule now accepts the existing
`ehp_exactness_inference_rule(exact_step)` form and also supports an
argument-free form that derives the exact sequence from the matched image and
kernel maps. The rule remains in `ehp_rules.py`; no EHP-specific branch or
new `ProofRule` was added to the generic engine.

Phase 6-2 deliberately does not implement automatic exact-pair discovery,
EHP sequence construction, or domain index arithmetic.

## Phase 6-3: statement conclusions and match guards

Phase 6-3 extends statement support from premise matching to conclusion
construction. `InferenceRule.conclusion_pattern` can now contain a dataclass
statement, and `substitute_statement_pattern()` replaces its fields using the
existing bindings. The generic substitution path remains domain-independent.

`InferenceRule.match_guard` provides an optional callable receiving the
matched premises and bindings. It can reject a structurally valid assignment
when an additional domain condition is required, without adding a
domain-specific branch to the generic engine.

The argument-free EHP exactness rule uses a statement conclusion pattern and a
guard that accepts only consecutive maps. The existing factory-bound form and
the direct `ehp_exactness_proof_step()` API remain compatible.

Phase 6-3 does not implement automatic EHP segment discovery, full EHP
sequence construction, or general theorem/index inference.
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

For the Phase 5-65 uploaded `proof.py` and
`test_inference_rule_pattern.py`, the inference-rule suite was re-run during
the documentation review:

```text
423 passed
```

This number refers specifically to the inference-rule pattern test file, not
to the complete project test suite.

Phase 6-1 tests:

```text
tests/test_ehp_rules.py: 1 passed
full project test suite: 648 passed
```

Phase 6-2 tests:

```text
focused inference and EHP tests: 428 passed
full project test suite: 652 passed
git diff --check: clean
```

Phase 6-3 tests:

```text
focused inference and EHP tests: 441 passed
full project test suite: 665 passed
pytest exit code: 0
```

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
