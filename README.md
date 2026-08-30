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
- homomorphism laws
- set / subgroup relations
- coset / modulo relations
- symbolic scalar constraints
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
15. coset / modulo reasoning,
16. provenance and explicit inference-scope / termination boundaries.

Current architecture:

```text
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / set / subgroup / modulo statements
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
- Phase 15: coset / modulo reasoning — completed

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

The algebra layer does not encode Toda-, EHP-, Hopf-, modulo-, or theorem-specific
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
- associative reassociation,
- quotient / modulo simplification.

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
homomorphism-, subgroup-, and modulo-derived facts reconnect through shared
generic reasoning where their semantics permit it.

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

Structural functorial rules can increase depth, so staged / bounded execution
is used where required.

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

```text
MembershipStatement(
  element=α,
  subgroup=A,
)
```

represents:

```text
α ∈ A
```

## Subset

```text
SubsetStatement(
  subset=A,
  superset=B,
)
```

represents:

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

```text
SubgroupEqualityStatement(
  left=A,
  right=B,
)
```

represents theorem-level subgroup equality.

Membership transfers across explicit equality:

```text
α ∈ A
A = B
↓
α ∈ B
```

and in the reverse direction as well.

## Role-aware image / kernel references

```text
ImageSubgroupReference(group_map=f)
KernelSubgroupReference(group_map=g)
```

Both expose the existing algebra-layer subgroup through `reference.subgroup`,
but the proof-level references themselves remain distinct terms.

Therefore:

```text
ImageSubgroupReference(E).subgroup
==
KernelSubgroupReference(H).subgroup
```

does not imply:

```text
ImageSubgroupReference(E)
==
KernelSubgroupReference(H)
```

This distinction preserves theorem provenance.

## SubgroupTerm

```text
SubgroupTerm
=
Subgroup
| ImageSubgroupReference
| KernelSubgroupReference
```

is used throughout membership / subset / subgroup-equality statements.

## Exactness bridge

```text
Exactness(f,g)
↓
Im(f)=Ker(g)
```

produces role-aware theorem equality.

Combined with:

```text
g(α)=0
↓
α ∈ Ker(g)
```

this gives:

```text
α ∈ Im(f)
```

through explicit subgroup equality propagation.

## Equality / subset closure

```text
A=B → B=A
```

```text
A=B
B=C
→ A=C
```

```text
A⊆B
B⊆C
→ A⊆C
```

```text
A=B → A⊆B
```

```text
A⊆B
B⊆A
→ A=B
```

The finite current subgroup relation family reaches genuine `FIXED_POINT`.

---

# Phase 15: Coset / modulo reasoning

Phase 15 adds a proof-level quotient / congruence layer on top of Phase 14.

The central design principle remains:

```text
mathematical meaning
≠
low-level structural equality
```

## Coset

A coset is represented structurally by:

```text
Coset(
  representative=α,
  subgroup=A,
)
```

with intended notation:

```text
α + A
```

`subgroup` is a `SubgroupTerm`, so raw subgroups and role-aware image / kernel
references are supported.

`Coset` Python equality remains structural. Mathematical equality of two cosets
is not encoded by changing `Coset.__eq__`.

## ModuloStatement

Congruence is a dedicated theorem statement:

```text
ModuloStatement(
  left=α,
  right=β,
  modulus=A,
)
```

with intended notation:

```text
α ≡ β mod A
```

This is deliberately separate from both generic `RelationType.EQUALITY` and
coset structural equality.

## Difference membership bridge

Current additive syntax represents:

```text
α-β
=
Sum(
  left=α,
  right=Multiple(-1, β),
)
```

Phase 15 implements:

```text
α ≡ β mod A
↔
α-β ∈ A
```

The reverse bridge recognizes only the explicit structural difference form
`Sum(α, Multiple(-1,β))`.

Ordinary membership, `α+β∈A`, or `α+2β∈A` are not misidentified as a modulo
premise.

No theorem-aware difference normalization is performed.

## CosetEqualityStatement

Mathematical coset equality is represented by:

```text
CosetEqualityStatement(
  left=Coset(α,A),
  right=Coset(β,A),
)
```

and Phase 15 implements:

```text
α ≡ β mod A
↔
α+A = β+A
```

The reverse bridge requires the two cosets to use the same proof-level
`SubgroupTerm`.

Therefore equal underlying subgroup values do not erase image / kernel role
identity.

## Equality → modulo

With an explicitly selected modulus `A`:

```text
α = β
→
α ≡ β mod A
```

The modulus is supplied to the concrete rule factory. Equality by itself does
not enumerate arbitrary subgroup moduli.

This is an inference-scope decision, not a mathematical limitation.

## ZERO → modulo

With an explicitly selected modulus `A`:

```text
α = 0
→
α ≡ 0 mod A
```

The reverse implication is intentionally absent:

```text
α ≡ 0 mod A
↛
α = 0
```

because congruence to zero modulo `A` only implies membership in `A`.

Phase 15 also does not globally convert ZERO relations into ordinary equality
relations merely to support modulo reasoning.

## Subgroup equality propagation

Explicit theorem equality transports the modulus:

```text
A = B
α ≡ β mod A
→
α ≡ β mod B
```

and in the reverse direction.

The bridge compares proof-level `SubgroupTerm` identity, not only the computed
raw subgroup value.

Therefore:

```text
Image(E).subgroup == Kernel(H).subgroup
```

alone does not transport modulo facts between `Im(E)` and `Ker(H)`.

An explicit theorem fact such as Exactness is required:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
↓
modulo transport
```

## Representative scenario

Phase 15 combines Phase 14 and Phase 15 facts in one fixed-point run:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

```text
α = β
↓
α ≡ β mod Ker(H)
↓
α ≡ β mod Im(E)
├→ α-β ∈ Im(E)
└→ α+Im(E)=β+Im(E)
```

and:

```text
β = 0
↓
β ≡ 0 mod Ker(H)
↓
β ≡ 0 mod Im(E)
```

No new shortcut theorem is required for these paths.

## Provenance

Derived modulo / membership / coset facts retain:

```text
ProofRule.INFERENCE
inference_rule
premises
```

When the same conclusion has multiple derivations:

```text
first accepted ProofStep
```

is retained in the knowledge state.

Alternative applications remain visible in execution traces through candidate
and duplicate-rejected steps.

Phase 15 does not yet store all alternative proofs as equal first-class proofs
inside the knowledge state.

## Termination boundary

Current Phase 15 cycles include:

```text
Modulo
↔ difference membership
```

```text
Modulo
↔ coset equality
```

and:

```text
Modulo mod A
↔ Modulo mod B
```

through explicit subgroup equality.

These rules do not construct unbounded nested terms. For a finite set of known
expressions and active `SubgroupTerm` values, ordinary duplicate rejection
reaches genuine:

```text
FIXED_POINT
```

Phase 15 termination does not rely on `MAX_ROUNDS`.

This does not imply that all future symbolic quotient / scalar rule families
will terminate.

---

# Current limitations

- Duplicate identity uses ordinary Python equality.
- There is no theorem-aware canonical normalization.
- The knowledge state keeps the first accepted `ProofStep` for an equal
  conclusion; alternative applications remain in execution traces.
- Pattern matching is structured but not a fully general recursive unification
  language.
- Exhaustive premise assignment can grow combinatorially.
- Arbitrary symbolic rule families are not guaranteed to terminate.
- `max_rounds` is a safety bound, not semantic cycle detection.
- Repeated Suspension, composition functoriality, and recursive Hopf formula
  application can generate unbounded structural depth.
- Automatic rule scheduling / theorem-depth planning is not implemented.
- Canonical `E^n`, additive, composition, or quotient normalization is not
  implemented.
- Composition associativity, identity, and bilinearity are not implemented.
- Additive zero identity is not a general theorem family.
- General `nα ↔ repeated Sum` expansion is not implemented.
- Suspension / `E` is connected to generic homomorphism additivity, but `H` and
  `P` are not activated as unrestricted untyped `MapSymbol` homomorphisms.
- Proof-level map source / target / ambient homotopy-group typing is not yet
  general.
- Universal map congruence `x=y → f(x)=f(y)` is not implemented.
- There is no first-class `NONZERO` relation type.
- General inverse-map construction / unrestricted desuspension is not
  implemented.
- Modulo reflexivity / symmetry / transitivity are not separate automatic
  theorem families.
- Coset equality symmetry / transitivity are not separate automatic theorem
  families.
- Modulo propagation through subset is obtained by composition through
  difference membership; no shortcut rule is added.
- No theorem-aware simplification of `α-0`, quotient representatives, or cosets
  is performed.
- Symbolic integer / scalar constraints are not yet first-class.
- `±α` and other coefficient indeterminacy are not yet first-class.
- Toda bracket value sets and Toda bracket indeterminacy remain future work.
- Steenrod operations, double EHP, and odd-primary-specific theorem families
  remain future work.

---

# Tests

Run the full project suite with:

```powershell
python -m pytest -v
```

Phase 15 completion:

```text
956 passed in 64.09s
```

Useful focused suites include:

```powershell
python -m pytest tests/test_set_rules.py -v
```

```powershell
python -m pytest tests/test_stable_rules.py::test_phase9_inference_scope_termination_and_theorem_boundary -v
```

The long-lived Phase 9 theorem-scope / termination regression remains green at
Phase 15 completion.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time.
Current behavior is defined by the latest README and design documents.

---

# Phase 15 completion boundary

Phase 15 is complete because the proof layer now supports:

```text
α + A
α ≡ β mod A
α + A = β + A
α - β ∈ A
```

with explicit theorem bridges:

```text
α ≡ β mod A
↔ α-β ∈ A
```

```text
α ≡ β mod A
↔ α+A = β+A
```

```text
α=β
→ α≡β mod A
```

```text
α=0
→ α≡0 mod A
```

```text
A=B
α≡β mod A
→ α≡β mod B
```

Completion also means:

1. `Coset` is first-class structural syntax.
2. `ModuloStatement` is a first-class theorem statement.
3. `CosetEqualityStatement` is a first-class theorem statement.
4. raw `Subgroup` remains supported as modulus.
5. role-aware image / kernel references remain supported as modulus.
6. structural equality remains separate from mathematical equality.
7. the difference bridge uses existing additive syntax.
8. the reverse difference bridge rejects non-difference membership.
9. coset equality does not redefine Python `Coset` equality.
10. the reverse coset bridge requires the same `SubgroupTerm` role.
11. equality / ZERO modulo bridges use explicit modulus scope.
12. modulo does not imply ordinary equality or ZERO.
13. subgroup equality transports modulo facts explicitly.
14. Exactness connects `Im(E)=Ker(H)` to modulo transport.
15. same underlying subgroup value does not collapse role identity.
16. representative Phase 14 + Phase 15 reasoning reaches one fixed point.
17. duplicate derivations retain first accepted provenance and alternative trace.
18. current bidirectional Phase 15 cycles reach finite `FIXED_POINT`.
19. terminal inference rounds produce no new steps.
20. the generic inference engine remains unchanged.
21. the full regression suite passes.

Phase 15 completion full suite:

```text
956 passed in 64.09s
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

Phases 12–15 have now completed the minimal additive, homomorphism,
set/subgroup, and coset/modulo layers.

The natural next Phase is therefore:

```text
Phase 16: Symbolic scalar constraints
```

Likely actual needs include forms such as:

```text
α = kβ + γ
k odd
```

```text
k ≡ 1 mod 2
```

```text
k ∈ Z
```

and restrictions that allow coefficient uncertainty to be preserved without
prematurely selecting a concrete integer.

Phase 16 should build on the existing additive and modulo layers without yet
introducing general Toda-bracket indeterminacy unless an actual scalar theorem
requires it.

The generic inference engine should remain unchanged unless a concrete symbolic
scalar theorem demonstrates a missing generic capability.
