# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to build a proof tracer that can explain how homotopy
groups of spheres are determined from mathematical input such as:

- EHP exact sequences
- composition relations
- element orders
- Toda relations
- Toda brackets
- Steenrod operations
- Hopf invariants
- stable-range results
- known literature-backed relations

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
4. a generic fixed-point inference engine,
5. the first EHP domain-inference vertical slice,
6. the first element-order domain-rule family integrated with generic relation reasoning.

The current architecture is:

```text
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

Phase 5-65 is treated as the completion point of the generic inference-engine
foundation.

Phase 6 completed the first EHP-domain vertical slice:

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
traceable derived relation
↓
fixed point
```

Phase 7 completed element-order reasoning and integrated it into the same
generic relation and fixed-point machinery:

```text
ord(α) = n
↓
nα = 0
↓
equality closure
↓
equivalent expressions are zero
```

The Phase 7 representative run executes EHP-derived ZERO reasoning and
ORDER-derived ZERO reasoning together in one knowledge state and reaches a
genuine fixed point without introducing domain-specific branches into the
generic engine.

---

# Development status

- Phase 1: finite abelian-group calculations — completed
- Phase 2: structured subgroup calculations — completed
- Phase 3: quotient groups, exact sequences, extensions, and EHP inference — completed
- Phase 4: presentation-based calculations with free components — completed
- Phase 5: generic proof / inference engine foundation — completed
- Phase 6: EHP domain-inference foundation — completed
- Phase 7-1: exact finite ORDER relation semantics — completed
- Phase 7-2: `ord(α)=n → nα=0` — completed
- Phase 7-3: order-derived ZERO → generic equality propagation — completed
- Phase 7-4: order-derived ZERO → equality closure → ZERO — completed
- Phase 7-5: EHP-derived ZERO and order-derived ZERO in one fixed-point run — completed
- Phase 7-6: EHP / ORDER provenance chains end-to-end — completed
- Phase 7-7: representative Phase 7 fixed-point completion scenario — completed
- Phase 7: element-order reasoning integrated with generic relation inference — completed

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

The earlier finite-group enumeration algorithms are retained as an independent
reference implementation.

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

as a subgroup / lattice condition.

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

The project can enumerate finite abelian candidate structures and test whether
they can occur as valid extension middle groups.

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

A relation may contain structured mathematical expressions, strings, maps, or
other values.

The relation object is intentionally more general than only one specific
homotopy-expression type.

## ORDER semantics

A concrete ORDER relation is represented as:

```text
Relation(
  lhs=α,
  rhs=n,
  relation_type=RelationType.ORDER,
)
```

and means:

```text
ord(α) = n
```

where `n` is the exact positive finite additive order of `α`.

The helper:

```text
order_relation(element, order, source=None, note=None)
```

constructs a concrete exact-order fact and requires `order` to be a positive
integer.

`bool`, non-integer values, zero, and negative values are rejected.

Validation is intentionally performed by the concrete `order_relation()`
helper rather than globally inside `Relation`, because rule patterns may use
`PatternVariable` objects in relation fields.

The current ORDER representation does not mean:

```text
the order of α divides n
```

and it does not yet represent infinite order.

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

Dependencies are represented through `ProofStep.premises`.

A separate graph class is not currently required because the dependency chain
is already represented directly by the proof steps.

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
- EHP inference,
- order calculation.

`HomotopyElement` and algebra-layer `GroupElement` are deliberately separate
concepts.

---

# Generic inference engine

Phase 5-65 is the completion point of the generic inference-engine foundation.

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
structured matching
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

This supports both outer structural matching and structured relation /
dataclass-statement matching.

## PatternVariable / VariableBinding

A `PatternVariable` represents a variable inside a rule pattern.

A `VariableBinding` records:

```text
PatternVariable
→
actual value
```

Shared variables across several premises must bind to the same value.

## Exhaustive premise assignment

The canonical search API is:

```text
find_all_matching_premises()
```

It uses deterministic depth-first backtracking and enumerates all valid ordered
assignments while preventing reuse of the same available-step index inside one
assignment.

Compatibility APIs that expose only the first result remain available.

## Conclusion substitution

Bindings can be substituted into structured conclusion patterns.

`substitute_pattern_value()` recursively substitutes through dataclass fields,
which allows conclusions containing nested expressions such as:

```text
Multiple(
  coefficient=?order,
  expression=?element,
)
```

to be concretized without adding a special engine branch for `Multiple`.

## Fixed-point execution

Derived conclusions are added to the available knowledge state and can be
consumed by later rounds.

Execution continues until:

```text
no genuinely new conclusion is produced
```

or until an optional `max_rounds` safety bound is reached.

`InferenceRunResult` records:

- final steps,
- productive round history,
- round count,
- termination reason.

The detailed round trace also records matches, applications, candidate steps,
accepted steps, and duplicate-rejected candidates.

---

# Generic relation rules

## Equality symmetry

```text
x = y
↓
y = x
```

## Equality transitivity

```text
x = y
y = z
↓
x = z
```

Running symmetry and transitivity together under fixed-point inference creates
an equality closure for a connected component.

The closure is not a special graph algorithm. It emerges from ordinary rules,
fixed-point iteration, and duplicate rejection.

## Generic ZERO propagation

Phase 7 adds a generic ZERO propagation rule:

```text
x = 0
y = x
↓
y = 0
```

This rule is intentionally not restricted to `Composition`.

It allows ZERO facts obtained from different mathematical rule families to
enter the same generic relation machinery.

Examples include:

```text
EHP-derived:
Composition(H,E) = 0
```

and:

```text
ORDER-derived:
nα = 0
```

Both can be propagated through equality closure.

The older Phase 6 composition-specific ZERO propagation rules remain
available for backward compatibility and for the Phase 6 regression suite.

---

# Phase 6: EHP domain inference foundation

Phase 6 established the first domain-specific vertical slice while keeping
the generic engine domain-independent.

Representative rules include:

```text
Image + Kernel → Exactness

Exactness + Image → Kernel

Exactness + Kernel → Image

Exactness → EHP zero composition

EHP zero composition → generic ZERO

equality symmetry

equality transitivity

ZERO propagation
```

The Phase 6 completion scenario confirms:

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
genuine fixed point
```

Phase 6 completion does not mean that all EHP or unstable-homotopy theorems
have been encoded.

It means that one representative EHP theorem family has been executed
end-to-end through the generic engine.

---

# Phase 7: element-order reasoning

Phase 7 adds the first non-EHP mathematical rule family that produces facts
consumable by the same relation engine.

## Phase 7-1: exact finite order relation

Concrete facts can represent:

```text
ord(α) = n
```

with exact positive finite order semantics.

## Phase 7-2: order implies zero multiple

The mathematical rule:

```text
ord(α) = n
↓
nα = 0
```

is implemented by:

```text
order_implies_zero_multiple_inference_rule()
```

The derived relation has the form:

```text
Relation(
  lhs=Multiple(
    coefficient=n,
    expression=α,
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

The rule uses the existing binding and nested dataclass substitution
mechanisms.

No generic-engine change is required.

## Phase 7-3: order-derived ZERO enters generic equality reasoning

The generic rule:

```text
x = 0
y = x
↓
y = 0
```

allows an ORDER-derived ZERO to propagate directly to an equal expression.

## Phase 7-4: order-derived ZERO through equality closure

A representative chain can start with:

```text
ord(α) = n
nα = middle
target = middle
```

and reach:

```text
nα = 0
target = nα
target = 0
```

through symmetry, transitivity, and generic ZERO propagation.

## Phase 7-5: EHP and ORDER branches coexist

EHP-derived ZERO and ORDER-derived ZERO can be produced in the same
fixed-point execution:

```text
EHP branch                         ORDER branch

Image + Kernel                    ord(α)=n
      ↓                               ↓
  Exactness                         nα=0
      ↓
EHP zero composition
      ↓
Composition(H,E)=0
```

Both conclusions remain in the same final knowledge state.

## Phase 7-6: provenance / dependency chains

The common knowledge state does not collapse the proof origins.

The EHP branch preserves:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
EHP-derived ZERO
```

while the ORDER branch preserves:

```text
ORDER fact
↓
ORDER-derived ZERO
```

Each derived `ProofStep` retains its own premises and source
`InferenceRule`.

## Phase 7-7: representative completion scenario

The representative Phase 7 rule set runs:

```text
EHP exactness rules
EHP → ZERO bridge
ORDER → ZERO
equality symmetry
equality transitivity
generic ZERO propagation
```

in one fixed-point execution.

Both branches may then propagate ZERO through separate equality chains:

```text
EHP-derived ZERO
↓
equality closure
↓
EHP target = 0
```

and:

```text
ORDER-derived ZERO
↓
equality closure
↓
ORDER target = 0
```

The completion test verifies both final ZERO conclusions and then evaluates
one additional inference round against the final state.

The additional round produces:

```text
new_steps == ()
```

so the representative Phase 7 rule set reaches a genuine fixed point.

---

# Phase 7 completion boundary

Phase 7 is complete because the project can now execute:

```text
exact element-order fact
↓
order-derived ZERO
↓
generic equality reasoning
↓
ZERO propagation
```

and can execute that path together with the Phase 6 EHP branch in the same
knowledge state.

Phase 7 does not implement:

- automatic discovery of an element's order from a group presentation,
- divisibility-order facts such as `ord(α) | n`,
- infinite-order facts,
- arithmetic simplification of nested `Multiple` expressions,
- general expression normalization,
- theorem-aware equality,
- Toda relations,
- Toda brackets,
- Hopf-invariant theorem families,
- stable-range theorem families,
- Steenrod operations,
- double EHP,
- odd-primary-specific inference.

Those remain future domain-rule families or future requirements.

---

# Current limitations

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

Alternative rule applications are preserved in execution traces, but the
accumulated knowledge state stores only the first accepted `ProofStep` for an
equal conclusion.

The knowledge state does not yet maintain a first-class collection of all
proof objects for one conclusion.

## Pattern-language depth

The current pattern system supports structured relation matching and
dataclass-statement field matching.

Substitution can recursively traverse dataclass fields.

The system is still not a fully general recursive unification language over
arbitrary mathematical syntax trees.

## Unbound conclusion variables

Current substitution semantics return `None` for an unbound
`PatternVariable`.

Domain rules must therefore ensure that variables needed in a conclusion are
bound by their premises.

## Search complexity

Exhaustive premise assignment can grow combinatorially.

The engine currently prioritizes deterministic and inspectable semantics over
performance optimization.

It does not yet implement:

- indexing,
- search pruning,
- memoization,
- semi-naive evaluation,
- agenda / worklist optimization,
- rule prioritization.

## Termination

`max_rounds` is a safety bound, not semantic cycle detection.

The engine relies on equal-conclusion duplicate rejection to stop finite
closure processes such as equality symmetry / transitivity.

It does not prove termination for arbitrary rule families that can generate
unboundedly many distinct conclusions.

---

# Tests

Run the full project suite with:

```powershell
python -m pytest -v
```

At Phase 7-7 completion:

```text
706 passed in 60.22s
```

The Phase 7 representative completion test is:

```powershell
python -m pytest tests/test_ehp_rules.py::test_phase7_representative_end_to_end_scenario_reaches_fixed_point -v
```

The combined EHP / relation-rule suite at Phase 7-7 completion is:

```powershell
python -m pytest tests/test_ehp_rules.py tests/test_relation_rules.py -v
```

with:

```text
37 passed
```

---

# Documentation

- `README.md` — current project capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history

Historical phase descriptions should be read as descriptions of the state at
that phase.

When an older historical section says that a feature was not yet implemented,
that statement must not be interpreted as a current limitation if a later
phase implemented it.

---

# Next development boundary

After Phase 7, the next phase should again be driven by an actual mathematical
rule family rather than speculative generic-engine refactoring.

Candidate directions include:

- suspension relations,
- Hopf-invariant relations,
- stable-range theorems,
- Toda composition relations,
- literature-backed theorem rules,
- Toda brackets,
- Steenrod operations,
- double EHP,
- odd-primary-specific rule families.

The governing development rule remains:

```text
new mathematical knowledge
=
new domain InferenceRule
```

and:

```text
change the generic engine
only when an actual mathematical rule
cannot be represented correctly
with the current rule language
```
