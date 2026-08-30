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
17. indeterminacy representation and bridges,
18. provenance and explicit inference-scope / termination boundaries.

Current architecture:

```text
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy statements
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
- Phase 17: indeterminacy — completed

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

The algebra layer does not encode Toda-, EHP-, Hopf-, modulo-,
scalar-constraint-, indeterminacy-, or theorem-specific meaning.

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

Special mathematical information that should not be forced into ordinary
element equality is represented by dedicated statement classes.

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

Examples:

```text
kβ
α = kβ + γ
```

are represented structurally with existing `Multiple`, `Sum`, and generic
equality.

The expression layer is structural syntax only.

It does not itself perform:

- theorem application,
- scalar constraint solving,
- candidate enumeration,
- normalization,
- stable-range checks,
- dimension validation,
- equality proof,
- zero proof,
- commutative reordering,
- associative reassociation,
- quotient / modulo simplification.

For example:

```text
α+β
β+α
```

and:

```text
2α
α+α
```

remain structurally distinct.

Mathematical equality is represented explicitly.

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

Duplicate conclusion identity continues to use ordinary Python equality.
The first accepted `ProofStep` remains in the knowledge state; alternative
derivations can remain visible in execution traces.

The pattern language is structured but is not a fully recursive unification
system over arbitrary nested mathematical syntax. Domain rules may use
`match_guard` and `conclusion_builder` when nested semantic inspection is
required.

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
homomorphism-, subgroup-, modulo-, scalar-, and indeterminacy-derived facts
reconnect through shared generic reasoning only where explicit bridges permit it.

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

---

# Phase 8: Suspension reasoning

```text
x=y  → E(x)=E(y)
x=0  → E(x)=0
nα=0 → nE(α)=0
```

Repeated Suspension can generate unbounded structural depth, so unrestricted
fixed-point termination is not assumed.

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

Known composition facts are structured equalities:

```text
α∘β = γ
```

Suspension preservation and Suspension-composition functoriality give:

```text
α∘β=γ
↓
E(α∘β)=Eγ
```

and:

```text
α∘β=γ
↓
E(α∘β)=Eα∘Eβ
```

Generic equality reasoning can then derive:

```text
Eα∘Eβ=Eγ
```

---

# Phase 11: Generalized Hopf-invariant reasoning

Generalized Hopf facts are represented by:

```text
H(expression)=value
```

where `value` is an `Expression`.

Important theorem boundary:

```text
H(x)=0
↛
x=0
```

The EHP bridge can derive:

```text
Exactness(E,H)
↓
H(Eα)=0
```

without changing the generic inference engine.

---

# Phase 12: Additive expression / reasoning

`Sum(left,right)` represents:

```text
α+β
```

The additive inverse is:

```text
-α = Multiple(-1, α)
```

Mathematical laws are explicit rules:

```text
α+(-α)=0
α+β=β+α
(α+β)+γ=α+(β+γ)
α+α=2α
```

No theorem-aware constructor normalization is performed.

---

# Phase 13: Homomorphism reasoning

Generic map application is represented by:

```text
MapApplication(f, α)
```

and homomorphism status by:

```text
HomomorphismStatement(f)
```

With explicit homomorphism status:

```text
f(α+β)=f(α)+f(β)
f(0)=0
f(-α)=-f(α)
f(nα)=n f(α)
```

Map existence alone does not imply homomorphism status.

---

# Phase 14: Set / subgroup reasoning

First-class statements include:

```text
α ∈ A
A ⊆ B
A = B
α ∈ Ker(f)
α ∈ Im(f)
```

Role-aware references preserve the distinction between:

```text
ImageSubgroupReference(f)
KernelSubgroupReference(g)
```

even when their underlying algebra-layer subgroup values happen to compare equal.

Exactness can explicitly derive:

```text
Im(f)=Ker(g)
```

and membership may then propagate through theorem-level subgroup equality.

---

# Phase 15: Coset / modulo reasoning

First-class structures:

```text
Coset
ModuloStatement
CosetEqualityStatement
```

Notation:

```text
α+A
α≡β mod A
α+A=β+A
```

Implemented theorem bridges include:

```text
α≡β mod A
↔
α-β∈A
```

```text
α≡β mod A
↔
α+A=β+A
```

```text
α=β
→
α≡β mod A
```

and role-aware modulus transport.

Modulo information does not imply ordinary equality.

---

# Phase 16: Symbolic scalar constraints

First-class symbolic-scalar structures:

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

Representative reasoning:

```text
k odd
↓
k≡1 mod 2
```

```text
ord(β)=2
+
k≡1 mod 2
↓
kβ=β
```

Symbolic scalar reasoning reconnects to modulo reasoning only through explicit
active bridges.

The system does not enumerate:

```text
k=1,3,5,...
```

and does not implement a general symbolic arithmetic solver.

Phase 16 completion full suite:

```text
988 passed in 61.87s
```

---

# Phase 17: Indeterminacy

Phase 17 adds a proof-level layer for mathematical information whose value is
not uniquely determined.

The central design principle is:

```text
uncertainty
≠
candidate enumeration
```

and:

```text
partial information
≠
exact equality
```

## Coset membership indeterminacy

```text
CosetMembershipStatement(
  element=x,
  coset=β+A,
)
```

represents:

```text
x ∈ β+A
```

It reuses the Phase 15 `Coset` structure.

It does not enumerate the elements of the coset.

## Sign indeterminacy

```text
SignIndeterminacyStatement(
  value=x,
  representative=α,
)
```

represents:

```text
x = ±α
```

This does not imply either:

```text
x=α
```

or:

```text
x=-α
```

without additional information.

## Coefficient indeterminacy

```text
CoefficientIndeterminacyStatement(
  value=x,
  expression=kβ+γ,
  constraint=k odd,
)
```

represents the family:

```text
x ∈ {kβ+γ | k odd}
```

without enumerating concrete coefficients.

The constraint reuses the existing Phase 16 `OddScalarStatement`.

## Modulo / coset bridge

Phase 17 connects modulo information to value indeterminacy:

```text
x≡β mod A
↓
x∈β+A
```

and the reverse bridge:

```text
x∈β+A
↓
x≡β mod A
```

These form a finite theorem cycle for finite known terms.

Duplicate rejection prevents infinite accumulation and the current rule family
reaches `FIXED_POINT`.

## Equality / sign bridge

Exact information may be weakened to sign-indeterminate information:

```text
x=α
↓
x=±α
```

The reverse rule is intentionally absent:

```text
x=±α
↛
x=α
```

## Symbolic scalar bridge

```text
x=kβ+γ
k odd
↓
CoefficientIndeterminacyStatement
```

The coefficient appearing in the equality must match the scalar constrained by
`OddScalarStatement`.

The implemented slice intentionally recognizes the current structural form:

```text
kβ+γ
```

and does not introduce general recursive symbolic-expression search or
commutative normalization.

## Representative fixed-point scenario

A representative Phase 17 run may begin with:

```text
x=kβ+γ
k odd
x≡δ mod A
```

and derive, in the same knowledge state:

```text
k≡1 mod 2
CoefficientIndeterminacyStatement
SignIndeterminacyStatement
CosetMembershipStatement
ModuloStatement
```

without deriving:

```text
x=δ
```

and without enumerating concrete odd coefficients.

## Provenance

Derived indeterminacy facts retain explicit premises and `inference_rule`.

Examples:

```text
x=kβ+γ
+
k odd
↓
CoefficientIndeterminacyStatement
```

```text
x≡δ mod A
↓
x∈δ+A
```

The knowledge state retains the first accepted proof for an equal conclusion;
alternative duplicate derivations may remain visible in execution traces.

## Termination / inference scope

The current Phase 17 bidirectional modulo/coset bridge:

```text
Modulo
↔
CosetMembership
```

does not create unbounded structural depth.

For finite known terms, duplicate rejection yields genuine:

```text
FIXED_POINT
```

Critical non-collapse boundaries:

```text
x=±α
↛
x=α
```

```text
x=±α
↛
x=-α
```

```text
x∈β+A
↛
x=β
```

```text
CoefficientIndeterminacyStatement
≠
RelationType.EQUALITY
```

The generic inference engine remains unchanged.

---

# Current limitations

## Conclusion identity

Duplicate identity uses ordinary Python equality.

No theorem-aware canonical mathematical normalization exists.

## Alternative proofs

The knowledge state keeps the first accepted `ProofStep` for an equal
conclusion. Alternative derivations can remain in duplicate-rejected traces.

## Pattern-language depth

The pattern language is not a fully recursive unification system over arbitrary
nested mathematical syntax.

Domain rules may inspect nested structures using `match_guard` and
`conclusion_builder`.

## Search complexity

Exhaustive premise assignment may grow combinatorially.

No general indexing, semi-naive evaluation, rule prioritization, or agenda-based
optimization is implemented.

## Termination

`max_rounds` remains a safety bound.

Some structural theorem families can still generate unbounded distinct
expressions.

The current Phase 17 modulo/coset cycle itself is finite.

## Typing

Proof-level expressions still do not fully enforce:

```text
source
target
ambient homotopy group
stable / unstable context
```

## Indeterminacy

Implemented:

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

Not yet implemented as general systems:

- arbitrary finite candidate sets,
- arbitrary set-valued expressions,
- intersection / narrowing of independent indeterminacies,
- theorem-aware candidate-set algebra,
- general coefficient constraint families,
- automatic collapse of indeterminacy from additional facts,
- Toda-bracket value sets.

The absence of a general `Indeterminacy` superclass is intentional.

---

# Tests

Run the full project suite with:

```powershell
python -m pytest -q
```

Phase 17 focused suite:

```powershell
python -m pytest tests/test_indeterminacy_rules.py -q
```

Verified result:

```text
36 passed
```

Phase 17 completion full suite:

```text
1024 passed in 66.01s
```

No failures.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time.
Current behavior is defined by the latest README and design documents.

---

# Phase 17 completion boundary

Phase 17 is complete because the proof layer can now preserve three concrete
forms of non-unique mathematical information without prematurely selecting a
value:

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

Completion means:

1. `CosetMembershipStatement` is first-class.
2. existing `Coset` is reused.
3. `SignIndeterminacyStatement` is first-class.
4. sign uncertainty is not represented as ordinary equality.
5. `CoefficientIndeterminacyStatement` is first-class.
6. existing `ScalarSymbol`, `Multiple`, `Sum`, and `OddScalarStatement` are reused.
7. symbolic odd coefficients are not enumerated.
8. modulo implies coset membership.
9. coset membership implies modulo.
10. exact equality implies sign indeterminacy.
11. sign indeterminacy does not imply exact equality.
12. symbolic equality plus matching odd-scalar constraint derives coefficient
    indeterminacy.
13. mismatched scalar constraints are rejected.
14. the current structural `kβ+γ` form is explicit.
15. no general recursive symbolic-expression matcher was added.
16. modulo/coset bridges coexist in one fixed-point run.
17. symbolic-scalar and indeterminacy branches coexist in one fixed-point run.
18. provenance is retained for coefficient, sign, and coset indeterminacy.
19. modulo/coset cycles terminate through duplicate rejection.
20. terminal rounds have no new steps.
21. coset membership does not select a representative.
22. sign indeterminacy does not select a sign.
23. coefficient indeterminacy is not treated as ordinary equality.
24. no concrete candidate enumeration is introduced.
25. no general `CandidateFamily` abstraction is introduced.
26. no general `Indeterminacy` superclass is introduced.
27. Toda bracket is not yet introduced.
28. the generic inference engine remains unchanged.
29. the full regression suite passes.

Phase 17 completion:

```text
tests/test_indeterminacy_rules.py
36 passed
```

```text
full suite
1024 passed in 66.01s
```

---

# Next development boundary

The completed dependency chain is now:

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
```

The next natural Phase is:

```text
Phase 18: Toda bracket minimum representation
```

Phase 18 should begin from an actual bracket form rather than from a universal
set-expression hierarchy.

Primary candidates:

```text
{a,b,c}
```

and, when the indexed unstable notation is required:

```text
{a,E^t b,E^t c}_t
```

Stable Toda notation:

```text
<a,b,c>
```

should remain distinct from unstable notation.

Phase 18 should first establish:

```text
bracket input structure
≠
bracket value
```

and:

```text
Toda bracket
=
set-valued / indeterminate mathematical object
```

rather than modeling a bracket as a function returning one exact element.

The Phase 17 indeterminacy layer should be reused for statements such as:

```text
x ∈ TodaBracket(...)
```

or later:

```text
TodaBracket(...) ⊆ x+A
```

only when the actual bracket example requires them.

The first Phase 18 implementation should not yet introduce a fully general
higher-Toda-bracket theorem prover, quantified theorem language, or general
symbolic set algebra.
