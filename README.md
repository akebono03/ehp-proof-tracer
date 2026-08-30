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
- set / subgroup relations
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
13. homomorphism reasoning for additive expressions,
14. set / subgroup reasoning with role-aware image / kernel references,
15. provenance and explicit inference-scope / termination boundaries.

Current architecture:

```text
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
proof-level set / subgroup statements
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
- Phase 13: homomorphism reasoning — completed
- Phase 14: set / subgroup reasoning — completed

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

exactness is represented algebraically by:

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
MapApplication
Suspension
```

Current generic map identity is represented by:

```text
MapSymbol
```

`MapSymbol` is not itself a homotopy-element expression. `MapApplication`
stores the structural expression `f(α)`.

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

EHP-, ORDER-, Suspension-, Freudenthal-, composition-, Hopf-, additive-,
homomorphism-, and subgroup-derived facts reconnect through shared generic
reasoning where their semantics permit it.

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

`Sum(left,right)` represents:

```text
α+β
```

while preserving binary tree structure.

The additive inverse is represented by:

```text
-α = Multiple(-1, α)
```

The following remain structurally distinct:

```text
2α
α+α
```

```text
0
0α
```

```text
α+0
α
```

Mathematical laws are explicit rules:

```text
α+(-α)=0
α+β=β+α
(α+β)+γ=α+(β+γ)
α+α=2α
```

The ORDER bridge supports:

```text
ord(α)=2
↓
2α=0

α+α=2α
↓
α+α=0
```

The finite representative Phase 12 rule family reaches `FIXED_POINT`.

---

# Phase 13: Homomorphism reasoning

Generic map application is represented by:

```text
MapApplication(f, α)
```

and homomorphism status is explicit:

```text
HomomorphismStatement(f)
```

Map existence alone does not imply homomorphism status.

Implemented laws include:

```text
f(α+β)=f(α)+f(β)
f(0)=0
f(-α)=-f(α)
f(nα)=n f(α)
```

Known ZERO preservation reconnects existing zero facts to map reasoning.

For Suspension / `E`, a dedicated bridge reconnects generic map additivity to
the existing `Suspension(expression)` syntax.

The project does not automatically activate unrestricted untyped
`Homomorphism(H)` or `Homomorphism(P)`.

ORDER integration derives:

```text
ord(α)=n
→ n f(α)=0
```

but not exact order preservation:

```text
ord(f(α))=n
```

The finite concrete Phase 13 rule family reaches `FIXED_POINT`.

---

# Phase 14: Set / subgroup reasoning

Phase 14 introduces first-class proof-level set / subgroup statements while
reusing algebra-layer subgroup values.

## Membership

Membership is represented by:

```text
MembershipStatement(
  element=α,
  subgroup=A,
)
```

with intended notation:

```text
α ∈ A
```

## Subset

Containment is represented by:

```text
SubsetStatement(
  subset=A,
  superset=B,
)
```

with intended notation:

```text
A ⊆ B
```

Basic propagation:

```text
α ∈ A
A ⊆ B
↓
α ∈ B
```

## Subgroup equality

Proof-level subgroup equality is represented by:

```text
SubgroupEqualityStatement(
  left=A,
  right=B,
)
```

Membership transfers across explicit equality:

```text
α ∈ A
A = B
↓
α ∈ B
```

and in the reverse direction as well.

## Image / kernel references

A central Phase 14 design decision is that image and kernel roles are not
identified merely because their computed subgroup values happen to be equal.

Role-aware references are:

```text
ImageSubgroupReference(group_map=f)
KernelSubgroupReference(group_map=g)
```

Both expose the existing algebra-layer subgroup through:

```text
reference.subgroup
```

but the references themselves remain distinct terms.

Therefore:

```text
ImageSubgroupReference(E).subgroup
==
KernelSubgroupReference(H).subgroup
```

does not imply structural identity:

```text
ImageSubgroupReference(E)
==
KernelSubgroupReference(H)
```

This distinction preserves theorem provenance.

## SubgroupTerm

The proof-level subgroup term type is:

```text
SubgroupTerm
=
Subgroup
| ImageSubgroupReference
| KernelSubgroupReference
```

`MembershipStatement`, `SubsetStatement`, and `SubgroupEqualityStatement`
accept `SubgroupTerm`.

Raw algebra-layer `Subgroup` remains supported for existing APIs and tests.

## Kernel membership bridge

The helper:

```text
kernel_membership_statement(
  element=α,
  group_map=f,
)
```

constructs membership in:

```text
KernelSubgroupReference(f)
```

rather than collapsing directly to the raw subgroup value.

The theorem bridge is:

```text
α ∈ Ker(f)
↓
f(α)=0
```

and conversely:

```text
f(α)=0
↓
α ∈ Ker(f)
```

The proof-layer map symbol remains explicit, so the algebra-layer `GroupMap`
and proof-expression `MapSymbol` are not silently identified by name.

## Image membership bridge

The helper:

```text
image_membership_statement(
  element=α,
  group_map=f,
)
```

constructs membership in:

```text
ImageSubgroupReference(f)
```

so image provenance is retained even when another map has a kernel with the
same computed subgroup value.

## Exactness bridge

For consecutive maps:

```text
A --f--> B --g--> C
```

exactness now produces the role-aware proof statement:

```text
ImageSubgroupReference(f)
=
KernelSubgroupReference(g)
```

rather than collapsing immediately to equality of raw `Subgroup` values.

This enables:

```text
g(α)=0
↓
α ∈ Ker(g)

Exactness(f,g)
↓
Im(f)=Ker(g)

↓ subgroup equality membership propagation

α ∈ Im(f)
```

while preserving the distinction between image role and kernel role.

## Equality / subset closure

Phase 14 adds subgroup-relation closure:

```text
A = B
→ B = A
```

```text
A = B
B = C
→ A = C
```

```text
A ⊆ B
B ⊆ C
→ A ⊆ C
```

## Equality / subset interconnection

Equality implies containment:

```text
A = B
→ A ⊆ B
```

Together with equality symmetry:

```text
A = B
→ B = A
→ B ⊆ A
```

Mutual containment implies subgroup equality:

```text
A ⊆ B
B ⊆ A
→ A = B
```

No theorem is inferred merely from equality of the underlying raw subgroup
values.

## Representative scenario

The Phase 14 representative scenario combines:

```text
Exactness
mapped ZERO
kernel membership
image membership
role-aware subgroup equality
subgroup equality symmetry / transitivity
subset transitivity
equality → subset
mutual subset → equality
membership transport
```

Representative chain:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)

H(α)=0
↓
α∈Ker(H)

Im(E)=Ker(H)
+
α∈Ker(H)
↓
α∈Im(E)
```

The same equality also produces:

```text
Im(E)⊆Ker(H)
Ker(H)⊆Im(E)
```

while preserving separate role-aware terms.

## Provenance

Representative derived steps retain:

```text
ProofRule.INFERENCE
inference_rule
premises
```

In particular:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

is traceable to the exactness premise, while:

```text
H(α)=0
↓
α∈Ker(H)
```

is traceable to the mapped-zero premise.

The final image-membership fact uses those intermediate proof steps as direct
premises rather than collapsing the dependency graph.

## Theorem boundary

The following is intentionally not valid:

```text
Im(E).subgroup == Ker(H).subgroup
↓
Im(E)=Ker(H)
```

Underlying algebraic value equality is not a substitute for a theorem-level
role bridge.

If the Exactness rule is absent, then:

```text
H(α)=0
→ α∈Ker(H)
```

does not imply:

```text
α∈Im(E)
```

even when the computed image and kernel subgroup values happen to coincide.

## Termination boundary

Equality / subset rules contain logical cycles such as:

```text
A=B
→ A⊆B

A=B
→ B=A
→ B⊆A

A⊆B
B⊆A
→ A=B
```

but they do not generate unbounded new structural terms.

For a finite set of `SubgroupTerm` values, ordinary duplicate rejection reaches
a genuine:

```text
FIXED_POINT
```

This is distinct from structural families such as repeated Suspension that can
increase expression depth indefinitely.

The generic inference engine remains unchanged.

---

# Current limitations

- Duplicate identity uses ordinary Python equality.
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
- Generic additive homomorphism preservation is implemented for explicit
  `HomomorphismStatement` facts and concrete rule scopes.
- Suspension / `E` is connected to generic homomorphism additivity, but `H` and
  `P` are not yet activated as unrestricted untyped `MapSymbol` homomorphisms.
- Map source / target and ambient homotopy-group typing are not yet represented
  in the proof-expression map layer.
- Universal map congruence `x=y → f(x)=f(y)` is not implemented.
- There is no first-class `NONZERO` relation type.
- General inverse-map construction / unrestricted desuspension are not
  implemented.
- Image membership currently records membership in an image role; explicit
  preimage / witness generation is not implemented.
- Subgroup equality / subset reflexivity is not generated as a premise-free
  theorem family.
- General set complements, unions, intersections, arbitrary set-valued
  expressions, cosets, and modulo relations are not yet first-class.
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

Phase 14 completion:

```text
921 passed in 62.89s
```

Useful focused suites include:

```powershell
python -m pytest tests/test_set_rules.py -v
```

```powershell
python -m pytest tests/test_stable_rules.py::test_phase9_inference_scope_termination_and_theorem_boundary -v
```

The Phase 9 representative termination / theorem-boundary regression remains
green at Phase 14 completion.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time.
Current behavior is defined by the latest README and design documents.

---

# Phase 14 completion boundary

Phase 14 is complete because proof-level subgroup reasoning now supports:

```text
α ∈ A
A ⊆ B
A = B
α ∈ Ker(f)
α ∈ Im(f)
```

with role-aware image / kernel identity, Exactness bridging, membership
propagation, relation closure, provenance, and fixed-point termination.

Completion means:

1. `MembershipStatement` is first-class.
2. `SubsetStatement` is first-class.
3. `SubgroupEqualityStatement` is first-class.
4. raw `Subgroup` remains supported.
5. `ImageSubgroupReference` preserves image role identity.
6. `KernelSubgroupReference` preserves kernel role identity.
7. `SubgroupTerm` unifies raw / image / kernel subgroup terms.
8. membership propagates through subset.
9. membership propagates through explicit subgroup equality.
10. `f(α)=0 ↔ α∈Ker(f)` is represented by explicit rule bridges.
11. image membership has a role-aware helper.
12. Exactness derives `Im(f)=Ker(g)` as role-aware equality.
13. same underlying subgroup value does not collapse role identity.
14. subgroup equality symmetry is implemented.
15. subgroup equality transitivity is implemented.
16. subset transitivity is implemented.
17. subgroup equality implies subset.
18. mutual subset implies subgroup equality.
19. equality / subset cycles reach finite `FIXED_POINT`.
20. representative Exactness + membership + closure scenario is regression-fixed.
21. provenance is retained through intermediate role-aware facts.
22. removing Exactness removes the image/kernel theorem bridge.
23. the generic inference engine remains unchanged.
24. the full regression suite passes.

Phase 14 completion full suite:

```text
921 passed in 62.89s
```

---

# Next development boundary

The roadmap dependency now passes through:

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

Phases 12, 13, and 14 have completed the minimal additive-expression,
homomorphism, and set/subgroup layers.

The natural next Phase is therefore:

```text
Phase 15: Coset / modulo reasoning
```

Likely representation needs include forms such as:

```text
α mod A
α + A
α ≡ β mod A
```

and theorem-level statements connecting differences or sums to subgroup
membership.

Phase 15 should preserve the Phase 14 distinction between:

```text
underlying algebraic value
```

and:

```text
proof-level mathematical role / provenance
```

and should not yet introduce symbolic scalar constraints, general
indeterminacy, or Toda brackets unless an actual coset/modulo rule requires
them.

The generic inference engine should remain unchanged unless a concrete
coset/modulo theorem demonstrates a missing generic capability.
