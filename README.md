# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined
from mathematical input such as:

- EHP exact sequences
- element orders
- additive relations
- Suspension
- Freudenthal stable-range theorems
- composition relations
- generalized Hopf invariants
- Toda relations and Toda brackets
- Steenrod operations
- literature-backed facts

The project separates:

```text
mathematical rule / theorem
generic inference mechanism
abelian-group calculation
```

The default development principle is:

```text
actual mathematical need
↓
minimal representation
↓
domain InferenceRule
↓
existing generic engine
```

The generic inference engine is changed only when an actual mathematical rule
cannot be represented correctly with the existing infrastructure.

---

# Current status

Completed foundations and theorem families:

1. finitely generated abelian-group calculation,
2. EHP exact-sequence calculation,
3. proof / relation representation,
4. generic fixed-point inference,
5. EHP-domain inference,
6. ORDER reasoning,
7. Suspension reasoning,
8. Freudenthal stable-range reasoning,
9. composition reasoning,
10. Suspension-composition functoriality,
11. generalized Hopf-invariant reasoning,
12. additive expression / additive-law reasoning,
13. provenance and explicit inference-scope / termination boundaries.

Current architecture:

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

Phase 5-65 is the completion point of the generic inference-engine foundation.
Phases 6 onward add mathematical rule families without adding domain-specific
branches to the engine unless an actual theorem demonstrates a missing generic
capability.

---

# Development status

- Phase 1: finite abelian-group calculations — completed
- Phase 2: structured subgroup calculations — completed
- Phase 3: quotient groups, exact sequences, extensions, EHP inference — completed
- Phase 4: presentation-based calculations with free components — completed
- Phase 5: generic proof / inference engine foundation — completed
- Phase 6: EHP domain-inference foundation — completed
- Phase 7: element-order reasoning — completed
- Phase 8: Suspension reasoning foundation — completed
- Phase 9: Freudenthal / stable-range reasoning — completed
- Phase 10: composition reasoning / Suspension-composition functoriality — completed
- Phase 11: generalized Hopf-invariant reasoning — completed
- Phase 12: additive expression / additive reasoning — completed

---

# Algebra layer

The algebra layer handles finitely generated abelian groups of the form:

```text
Z^r ⊕ finite torsion
```

The presentation-based path uses relation matrices, integer lattices, Hermite
normal form, and Smith normal form to calculate kernel, image, and cokernel.

Finite-group enumeration remains available as an independent reference path.

For:

```text
A --f--> B --g--> C
```

exactness is represented by:

```text
Im(f)=Ker(g)
```

and is kept distinct from:

```text
B / Im(f) ≅ Im(g)
```

The algebra layer does not encode Toda-, EHP-, Hopf-, or theorem-specific
meaning.

---

# Proof / relation model

`Relation` stores:

```text
lhs
rhs
relation_type
source
note
```

Current principal relation types:

```text
EQUALITY
ZERO
ORDER
```

A `ProofStep` preserves:

```text
conclusion
premises
rule
note
inference_rule
```

This is the basis for end-to-end provenance.

`LiteratureReference` stores structured literature metadata.

---

# Expression model

Current structured expressions include:

```text
Zero
HomotopyElement
Multiple
Sum
Composition
Suspension
```

Generator helpers include:

```text
eta(n)
nu(n)
sigma(n)
```

The expression layer is structural syntax only.

It does not itself perform:

- theorem application,
- normalization,
- stable-range checks,
- dimension validation,
- equality proof,
- zero proof,
- commutative reordering,
- associative reassociation.

For example, the following remain structurally distinct:

```text
α+β
β+α
```

```text
(α+β)+γ
α+(β+γ)
```

```text
2α
α+α
```

Mathematical equality between such expressions is represented explicitly by
`RelationType.EQUALITY`.

---

# Generic inference engine

The generic pipeline is:

```text
known ProofSteps
+
InferenceRules
↓
premise search
↓
structured matching
↓
bindings / shared-binding consistency
↓
match guard
↓
conclusion construction
↓
duplicate classification
↓
new ProofSteps
↓
next round
```

Termination reasons:

```text
FIXED_POINT
MAX_ROUNDS
```

`max_rounds` is a safety bound, not semantic cycle detection.

One round does not recursively consume conclusions created earlier in that
same round as fresh premises for later rules.

---

# Generic relation rules

Equality symmetry:

```text
x=y
→ y=x
```

Equality transitivity:

```text
x=y
y=z
→ x=z
```

Generic ZERO propagation:

```text
x=0
y=x
→ y=0
```

EHP-, ORDER-, Suspension-, Freudenthal-, composition-, Hopf-, and additive
facts reconnect through this shared generic relation machinery where their
semantics permit it.

---

# Phase 6: EHP reasoning

Representative chain:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
generic ZERO
↓
equality closure / ZERO propagation
↓
FIXED_POINT
```

---

# Phase 7: ORDER reasoning

```text
ord(α)=n
↓
nα=0
↓
generic equality / ZERO reasoning
```

The ORDER conclusion uses `Multiple(n, α)`.

---

# Phase 8: Suspension reasoning

```text
x=y  → E(x)=E(y)
x=0  → E(x)=0
nα=0 → nE(α)=0
```

Repeated Suspension can generate:

```text
E(x), E²(x), E³(x), ...
```

so unrestricted fixed-point termination is not assumed.

---

# Phase 9: Freudenthal reasoning

Stable range:

```text
stem <= sphere_dimension - 2
→ suspension isomorphism
→ injectivity
→ equality / ZERO reflection
```

Boundary:

```text
stem == sphere_dimension - 1
→ epimorphism only
```

Outside the implemented range:

```text
stem >= sphere_dimension
→ no Freudenthal-derived conclusion
```

---

# Phase 10: Composition reasoning

Known composition facts are ordinary structured equality relations:

```text
α∘β = γ
```

Known zero composition can be bridged to generic ZERO.

Suspension preservation gives:

```text
α∘β=γ
→ E(α∘β)=Eγ
```

Suspension-composition functoriality gives:

```text
α∘β=γ
→ E(α∘β)=Eα∘Eβ
```

Generic equality reasoning can then derive:

```text
Eα∘Eβ=Eγ
```

Functors and symmetry can increase structural depth, so staged / bounded
execution is used where required.

---

# Phase 11: Generalized Hopf-invariant reasoning

Generalized Hopf facts are represented by:

```text
H(expression)=value
```

where `value` is an `Expression`, not an integer-only field.

Implemented vertical slices include:

```text
H(α)=β
↓
HopfCompositionLawStatement
↓
H(α∘Eγ)=β∘Eγ
```

and:

```text
H(x)=y
y=0
↓
H(x)=0
```

with the important theorem boundary:

```text
H(x)=0
↛
x=0
```

The EHP bridge includes:

```text
Exactness(E,H)
↓
EHPZeroCompositionStatement(E,H)
↓
H(Eα)=0
```

Recursive Hopf structural growth is not treated as unrestricted
fixed-point-safe.

---

# Phase 12: Additive expression / reasoning

Phase 12 introduces the first proof-layer representation of additive structure.

## Sum

Binary sum:

```text
α+β
```

is represented by:

```python
Sum(
  left=alpha,
  right=beta,
)
```

`Sum` preserves binary tree structure exactly.

No flattening or canonical reordering is performed.

## Additive inverse representation

Phase 12 does not add a dedicated `Inverse` node.

The canonical current representation is:

```text
-α
=
Multiple(-1, α)
```

This is representation only; mathematical consequences are explicit rules.

## Multiple / Sum boundary

The following are intentionally structurally distinct:

```text
Multiple(2, α)
Sum(α, α)
```

Likewise:

```text
Zero()
Multiple(0, α)
```

are structurally distinct.

No automatic `Multiple → Sum` normalization is performed.

## Zero-addition structural boundary

The expressions:

```text
α+0
0+α
```

are representable and remain structurally distinct from `α`.

Phase 12 does not add constructor simplification:

```text
α+0 → α
0+α → α
```

and does not yet add a separate zero-identity theorem family.

## Additive inverse rule

Phase 12 adds:

```text
α+(-α)=0
```

as an explicit domain inference rule.

The conclusion is a generic `RelationType.ZERO`.

The expression itself remains a `Sum`; it is not normalized into `Zero()`.

## Commutativity

Phase 12 adds:

```text
α+β = β+α
```

as an explicit `RelationType.EQUALITY`.

The two `Sum` objects remain structurally distinct.

Reverse equality is handled by existing generic equality symmetry.

## Associativity

Phase 12 adds:

```text
(α+β)+γ = α+(β+γ)
```

as an explicit `RelationType.EQUALITY`.

The left-associated and right-associated trees remain structurally distinct.

Reverse reassociation is handled by existing generic equality symmetry.

## ORDER bridge

Phase 12 retains the Phase 7 ORDER semantics:

```text
ord(α)=n
→ nα=0
```

using `Multiple(n, α)`.

For the first additive bridge, Phase 12 adds only:

```text
α+α = 2α
```

as an explicit equality relation.

This supports:

```text
ord(α)=2
↓
2α=0
```

together with:

```text
α+α=2α
```

and generic ZERO propagation:

```text
α+α=0
```

General `nα ↔ repeated Sum` expansion is not implemented.

## Representative scenario

The Phase 12 representative scenario verifies coexistence of:

```text
additive inverse
commutativity
associativity
ORDER
Multiple / repeated-Sum bridge
generic equality symmetry
generic equality transitivity
generic ZERO propagation
```

in one inference environment.

Representative branches include:

```text
ord(α)=2
↓
2α=0
α+α=2α
↓
α+α=0
```

```text
α+(-α)=0
α+(-α)=(-α)+α
↓
(-α)+α=0
```

and reassociation / commutation chains using generic equality closure.

The finite representative scenario reaches:

```text
FIXED_POINT
```

## Provenance

Representative Phase 12 conclusions preserve:

```text
ProofRule.INFERENCE
inference_rule
premises
```

so that ORDER-derived, additive-inverse-derived, commutativity-derived,
associativity-derived, and generic-relation-derived facts remain traceable.

## Normalization boundary

Phase 12 formally preserves:

```text
α+β                    !=structural β+α
(α+β)+γ                !=structural α+(β+γ)
2α                     !=structural α+α
α+0                    !=structural α
0+α                    !=structural α
```

Mathematical equivalence is represented by explicit theorem relations.

No theorem-aware canonical expression equality is added.

## Inference-scope / termination boundary

Current additive rules are concrete rule factories, for example:

```text
additive_inverse_inference_rule(alpha)
sum_commutativity_inference_rule(alpha, beta)
sum_associativity_inference_rule(alpha, beta, gamma)
double_equals_repeated_sum_inference_rule(alpha)
```

For a finite concrete expression set, additive equality / ZERO closure can
reach a genuine fixed point through ordinary duplicate rejection.

Active rule scope controls what is derivable.

For example:

```text
bridge only
→ α+α=2α
```

does not derive:

```text
2α=0
```

without the ORDER rule, and does not derive:

```text
α+α=0
```

without ZERO propagation.

Phase 12 does not introduce arbitrary expression enumeration, recursive sum
normalization, or general repeated-sum expansion.

---

# Phase 12 completion boundary

Phase 12 is complete because the project can now represent and reason about a
minimal additive structure while preserving the syntax / theorem separation.

Completion means:

1. `Sum` is a first-class structured expression.
2. nested sums are representable.
3. operand order remains structural.
4. association remains structural.
5. `Multiple` remains distinct from repeated `Sum`.
6. additive inverse uses `Multiple(-1, α)`.
7. zero-addition forms remain lossless structural expressions.
8. `α+(-α)=0` is an explicit rule.
9. commutativity is an explicit equality rule.
10. associativity is an explicit equality rule.
11. `α+α=2α` bridges additive syntax to existing ORDER reasoning.
12. `ord(α)=2 → 2α=0 → α+α=0` works through generic ZERO propagation.
13. additive rules coexist in one representative fixed-point scenario.
14. provenance is preserved end-to-end.
15. normalization boundaries are regression-fixed.
16. active rule scope controls additive derivation.
17. no additive-specific branch is added to the generic inference engine.
18. the full regression suite passes.

Phase 12 completion full suite:

```text
809 passed in 62.32s
```

---

# Current limitations

- Duplicate identity uses ordinary Python equality.
- There is no theorem-aware canonical normalization.
- The knowledge state keeps the first accepted `ProofStep` for an equal
  conclusion; alternative applications remain in execution traces.
- Pattern matching is structured but not fully general recursive unification.
- Exhaustive premise assignment can grow combinatorially.
- Arbitrary symbolic rule families are not guaranteed to terminate.
- `max_rounds` is a safety bound, not semantic cycle detection.
- Repeated Suspension, composition functoriality, and recursive Hopf formula
  application can generate unbounded structural depth.
- Automatic rule scheduling / theorem-depth planning is not implemented.
- Canonical `E^n` and composition normalization are not implemented.
- Composition associativity, identity, and bilinearity are not implemented.
- Additive zero identity is not yet an explicit theorem family.
- General `nα ↔ repeated Sum` expansion is not implemented.
- Additivity / homomorphism preservation for E, H, P, or arbitrary maps is not
  yet implemented at the proof-expression level.
- There is no first-class `NONZERO` relation type.
- General inverse-map construction / unrestricted desuspension are not
  implemented.
- Element-level set / subgroup / image / kernel membership is not first-class.
- `H(x)=0` cannot yet produce an explicit `x ∈ Ker(H)=Im(E)` fact or witness.
- Hopf additivity is not implemented.
- `±α` is not yet a first-class indeterminacy representation.
- Toda brackets, Steenrod operations, double EHP, and odd-primary-specific
  theorem families remain future work.

---

# Tests

Run the full project suite with:

```powershell
python -m pytest -v
```

Phase 12 completion:

```text
809 passed in 62.32s
```

Useful focused suites include:

```powershell
python -m pytest tests/test_expression.py -v
```

```powershell
python -m pytest tests/test_relation_rules.py -v
```

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time.
Current behavior is defined by the latest README and design documents.

---

# Next development boundary

The roadmap places:

```text
Abelian group expression
↓
Homomorphism reasoning
↓
Set / subgroup reasoning
↓
Coset / modulo
↓
Symbolic scalar constraints
↓
Indeterminacy
↓
Toda bracket
```

in that dependency order.

Therefore the natural next Phase is Homomorphism reasoning for additive
expressions.

The next Phase should begin from a minimal actual rule such as preservation of
addition by a map, rather than from speculative generic-engine refactoring.

Possible mathematical needs include:

```text
f(α+β)=f(α)+f(β)
f(-α)=-f(α)
f(nα)=n f(α)
f(0)=0
```

with E, H, and P treated as homomorphisms only to the extent justified by the
actual map / theorem semantics being implemented.

The generic engine should remain unchanged unless the concrete homomorphism
rules demonstrate a missing generic capability.
