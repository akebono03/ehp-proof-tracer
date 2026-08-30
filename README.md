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
- indeterminacy
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
16. symbolic scalar constraints with parity / mod-two / order-two integration,
17. provenance and explicit inference-scope / termination boundaries.

Current architecture:

```text
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo statements
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
- Phase 16: symbolic scalar constraints — completed

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

The algebra layer does not encode Toda-, EHP-, Hopf-, modulo-, scalar-constraint-,
or theorem-specific meaning.

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

Symbolic integer coefficients can be represented by:

```text
ScalarSymbol
```

For example:

```text
kβ
```

is represented structurally by:

```text
Multiple(
  coefficient=ScalarSymbol("k"),
  expression=β,
)
```

and:

```text
α = kβ + γ
```

can be represented by a generic equality relation whose right-hand side is a
`Sum`.

Current generic map identity is represented by:

```text
MapSymbol
```

`MapSymbol` is not itself a homotopy-element expression. `MapApplication`
stores the structural expression `f(α)`.

The expression layer is structural syntax only.

It does not itself perform:

- theorem application,
- scalar constraint solving,
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

Duplicate conclusion identity continues to use ordinary Python equality.
The first accepted `ProofStep` remains in the knowledge state; alternative
derivations can remain visible in execution traces.

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
homomorphism-, subgroup-, modulo-, and scalar-derived facts reconnect through
shared generic reasoning where their semantics permit it.

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

is used throughout membership / subset / subgroup-equality / modulo statements.

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

The finite current subgroup relation family reaches genuine `FIXED_POINT`.

---

# Phase 15: Coset / modulo reasoning

Phase 15 adds a proof-level quotient / congruence layer on top of Phase 14.

## Coset

```text
Coset(
  representative=α,
  subgroup=A,
)
```

represents the structural coset:

```text
α + A
```

Mathematical equality of cosets is represented separately by
`CosetEqualityStatement`.

## ModuloStatement

```text
ModuloStatement(
  left=α,
  right=β,
  modulus=A,
)
```

represents:

```text
α ≡ β mod A
```

It is deliberately separate from generic `RelationType.EQUALITY`.

## Difference membership bridge

Current subtraction syntax is:

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

The reverse bridge accepts the explicit difference structure only.

## Coset equality bridge

Phase 15 also implements:

```text
α ≡ β mod A
↔
α+A = β+A
```

The reverse bridge requires the same proof-level modulus role.

## Equality / ZERO modulo scope

With an explicitly selected modulus `A`:

```text
α=β
→ α≡β mod A
```

```text
α=0
→ α≡0 mod A
```

These rules do not enumerate arbitrary moduli automatically.

## Role-aware modulus transport

Explicit theorem equality transports congruence:

```text
A=B
α≡β mod A
→
α≡β mod B
```

This reconnects Phase 14 Exactness to modulo reasoning:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
↓
role-aware modulo transport
```

Current Phase 15 bidirectional bridge families reach finite `FIXED_POINT`.

---

# Phase 16: Symbolic scalar constraints

Phase 16 introduces the minimal proof-level representation and theorem bridges
needed for symbolic integer coefficients without introducing a general symbolic
arithmetic solver.

## ScalarSymbol

A symbolic scalar such as:

```text
k
```

can occur as a `Multiple` coefficient:

```text
kβ
```

and therefore inside larger additive relations such as:

```text
α = kβ + γ
```

No concrete integer value is selected merely because the scalar is symbolic.

## Parity statements

Phase 16 adds first-class theorem statements:

```text
OddScalarStatement(k)
EvenScalarStatement(k)
```

These mean that the symbolic integer scalar is known to be odd or even.

Parity is proof-level mathematical knowledge; it is not inferred from the
scalar name or from structural syntax.

## ScalarCongruenceStatement

Phase 16 adds:

```text
ScalarCongruenceStatement(
  scalar=k,
  residue=r,
  modulus=m,
)
```

with intended notation:

```text
k ≡ r mod m
```

Current concrete parity bridges are:

```text
k odd
→
k ≡ 1 mod 2
```

```text
k even
→
k ≡ 0 mod 2
```

These are explicit `InferenceRule`s.

## Order-two bridge

The principal Phase 16 theorem bridge is:

```text
ord(β)=2
k≡1 mod 2
↓
kβ=β
```

represented as ordinary generic equality:

```text
Relation(
  lhs=Multiple(k, β),
  rhs=β,
  relation_type=EQUALITY,
)
```

This reuses existing `Multiple`, ORDER, and equality infrastructure.

The rule requires exact order two and specifically congruence to one modulo two.
It does not fire for:

```text
ord(β)=3
```

or:

```text
k≡0 mod 2
```

## Generic equality reconnection

Symbolic additive equalities remain ordinary generic equality facts.

For example:

```text
α = kβ + γ
```

uses the same equality symmetry / transitivity machinery as concrete
expressions.

Phase 16 does not introduce a separate symbolic-equality relation type.

## Modulo reconnection

Phase 16 itself does not directly infer modulo facts from parity.

Instead the existing layers compose:

```text
k odd
↓
k≡1 mod 2

ord(β)=2
+
k≡1 mod 2
↓
kβ=β

explicit equality→modulo bridge
↓
kβ≡β mod A
```

This preserves the architecture:

```text
scalar reasoning
↓
ordinary equality
↓
existing modulo reasoning
```

rather than adding scalar-specific modulo shortcuts.

## Exactness / role-aware modulo integration

The representative Phase 16 scenario connects:

```text
k odd
ord(β)=2
Exactness(E,H)
```

to:

```text
k≡1 mod 2
↓
kβ=β
↓
kβ≡β mod Ker(H)
```

and independently:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

therefore:

```text
kβ≡β mod Ker(H)
↓
kβ≡β mod Im(E)
```

Existing Phase 15 bridges then produce:

```text
kβ-β ∈ Ker(H)
kβ-β ∈ Im(E)
```

and:

```text
[kβ]=[β] mod Ker(H)
[kβ]=[β] mod Im(E)
```

No special scalar–Exactness shortcut is introduced.

## Provenance

The representative chain preserves intermediate premises:

```text
OddScalarStatement(k)
↓
ScalarCongruenceStatement(k,1,2)
```

then:

```text
ord(β)=2
+
ScalarCongruenceStatement(k,1,2)
↓
kβ=β
```

then:

```text
kβ=β
↓
kβ≡β mod Ker(H)
```

and:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

then:

```text
kβ≡β mod Ker(H)
+
Im(E)=Ker(H)
↓
kβ≡β mod Im(E)
```

When two derivation paths produce the same symbolic membership conclusion, the
first accepted proof step remains in the knowledge state and the alternative
derivation remains in duplicate-rejected execution trace data.

## Termination

The current Phase 16 scalar rules do not recursively construct deeper scalar
syntax.

The finite representative family:

```text
odd/even
→ scalar congruence
→ order-two equality
→ modulo
↔ membership
↔ coset equality
↔ explicit role-aware modulus transport
```

reaches genuine:

```text
FIXED_POINT
```

for finite known expressions and finite active moduli.

The terminal inference round produces:

```text
new_steps == ()
```

No semantic cycle detector is added.

## Inference-scope boundary

A crucial boundary is:

```text
k odd
ord(β)=2
```

with Phase 16 scalar / order rules can derive:

```text
k≡1 mod 2
kβ=β
```

but does not derive:

```text
kβ≡β mod A
```

unless a concrete:

```text
equality_implies_modulo_inference_rule(modulus=A)
```

is explicitly active.

Likewise, membership and coset facts do not appear without the required modulo
bridges.

This preserves:

```text
mathematical applicability
≠
active inference scope
```

---

# Current limitations

The following remain current limitations after Phase 16.

## Generic engine

- Duplicate conclusion identity uses ordinary Python equality.
- The knowledge state keeps the first accepted proof step for an equal
  conclusion; alternative applications are execution-trace data.
- Pattern matching is structured but is not a fully general symbolic
  unification / theorem-proving language.
- Exhaustive premise assignment can grow combinatorially.
- `max_rounds` remains a safety bound rather than semantic cycle detection.
- Arbitrary future rule families are not guaranteed to terminate.

## Expression / normalization

- No canonical commutative / associative additive normal form.
- No general scalar arithmetic normalization.
- `2α` and `α+α` remain structurally distinct unless an explicit theorem rule
  connects them.
- No general symbolic simplification of `kα+lα`.
- No theorem-aware subtraction normalization.

## Symbolic scalars

Implemented:

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
odd → 1 mod 2
even → 0 mod 2
order-two + 1 mod 2 → scalar-multiple equality
```

Not implemented:

- general symbolic integer arithmetic,
- general congruence arithmetic,
- divisibility / nondivisibility solver,
- arbitrary modulus propagation for scalar congruences,
- symbolic inequality,
- automatic deduction of parity from arbitrary formulas,
- coefficient-domain constraint solving,
- quantifiers over integer coefficients.

## Modulo / quotient

- No canonical coset representative selection.
- No quotient arithmetic normalization.
- No premise-free arbitrary modulus enumeration.
- No theorem-aware Python equality for cosets.
- No automatic conversion of every equality / ZERO fact into every possible
  modulo statement.

## Map / theorem language

- Proof-level `MapSymbol` does not yet carry complete source / target / ambient
  homotopy-group typing.
- General theorem quantifiers are not first-class.
- Existential witnesses are not first-class.

## Future homotopy-theoretic layers

Not yet implemented as general systems:

- first-class coefficient / sign indeterminacy,
- `±α` as an indeterminacy object,
- Toda-bracket value sets,
- Toda-bracket indeterminacy,
- indexed / iterated suspension parameters for general Toda-bracket notation,
- general theorem representation with quantified assumptions,
- Steenrod operations,
- double EHP,
- odd-primary-specific theorem families.

---

# Tests

Run the full project suite with:

```powershell
python -m pytest -q
```

Phase 16 completion:

```text
988 passed in 61.87s
```

Focused Phase 16 scalar / set integration:

```powershell
python -m pytest tests/test_scalar_rules.py tests/test_set_rules.py -q
```

Phase 16-8 representative scenario:

```powershell
python -m pytest tests/test_set_rules.py::test_phase16_representative_symbolic_scalar_order_exactness_modulo_scenario -q
```

Phase 16-9 provenance / termination / scope regressions:

```powershell
python -m pytest tests/test_set_rules.py::test_phase16_alternative_derivation_keeps_first_provenance_and_duplicate_trace tests/test_set_rules.py::test_phase16_bidirectional_scalar_modulo_bridges_terminate_at_fixed_point tests/test_set_rules.py::test_phase16_symbolic_scalar_reasoning_stays_outside_modulo_scope_without_explicit_bridge -q
```

Verified Phase 16-9 focused result:

```text
3 passed in 2.10s
```

Verified full suite:

```text
988 passed in 61.87s
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

# Phase 16 completion boundary

Phase 16 is complete because the proof layer now supports the minimal symbolic
scalar constraint slice needed to connect symbolic coefficients to existing
ORDER and modulo reasoning.

Completion means:

1. `ScalarSymbol` can occur as a `Multiple` coefficient.
2. symbolic additive equality such as `α=kβ+γ` is structurally representable.
3. symbolic additive equality uses existing generic equality reasoning.
4. `OddScalarStatement` is first-class.
5. `EvenScalarStatement` is first-class.
6. `ScalarCongruenceStatement` is first-class.
7. odd scalar implies congruence to one modulo two.
8. even scalar implies congruence to zero modulo two.
9. the odd rule rejects an even premise.
10. the even rule rejects an odd premise.
11. exact order two plus congruence to one modulo two derives `kβ=β`.
12. the order-two bridge rejects non-order-two elements.
13. the order-two bridge rejects scalar congruence zero modulo two.
14. odd scalar plus order two reaches the symbolic equality in a fixed-point run.
15. symbolic equality reconnects to existing modulo reasoning only through an
    explicitly active modulo bridge.
16. Phase 15 modulo / membership / coset bridges work unchanged for symbolic
    multiples.
17. Exactness transports the symbolic modulo fact between `Ker(H)` and `Im(E)`.
18. role-aware image / kernel identity remains explicit.
19. representative scalar + order + exactness + modulo reasoning reaches one
    fixed point.
20. provenance is preserved through parity, order, equality, modulo, Exactness,
    and modulus transport.
21. alternative derivations preserve the first accepted provenance and retain
    the alternative duplicate trace.
22. current bidirectional Phase 16 / Phase 15 bridge family reaches finite
    `FIXED_POINT`.
23. the terminal inference round has `new_steps == ()`.
24. scalar/order reasoning does not cross into modulo scope without the explicit
    equality-to-modulo bridge.
25. the generic inference engine remains unchanged.
26. the full regression suite passes.

Phase 16 completion full suite:

```text
988 passed in 61.87s
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

Phases 12–16 have completed the minimal additive, homomorphism, set/subgroup,
coset/modulo, and symbolic-scalar layers.

The natural next Phase is therefore:

```text
Phase 17: Indeterminacy
```

The next actual mathematical needs should be selected before implementation.
Likely candidate forms include:

```text
α = kβ + γ
k odd
```

viewed not merely as a scalar constraint, but as information describing a
family of possible representatives, and expressions involving sign or
coefficient uncertainty.

Phase 17 should preserve uncertainty explicitly rather than prematurely
choosing a representative.

It should not yet implement the full Toda-bracket system unless an actual
indeterminacy representation requires a minimal bracket-facing interface.

The generic inference engine should remain unchanged unless a concrete
indeterminacy theorem demonstrates a missing generic capability.
