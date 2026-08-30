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
18. Toda bracket minimum representation, membership, definedness, provenance,
19. Toda bracket membership theorem bridge from an actual literature-backed fact,
20. explicit inference-scope / termination boundaries.

Current architecture:

```text
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy / Toda statements
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
- Phase 18: Toda bracket minimum representation — completed
- Phase 19: Toda bracket membership / first theorem bridge — completed

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


# Phase 18: Toda bracket minimum representation

Phase 18 introduces a first-class representation of a three-fold unstable Toda
bracket while keeping the bracket input structure distinct from any selected
value.

The central design boundary is:

```text
bracket input structure
≠
bracket value
```

## TodaBracket

The three-fold bracket:

```text
{a,b,c}
```

is represented by:

```text
TodaBracket(
  first=a,
  second=b,
  third=c,
)
```

`TodaBracket` is intentionally not an `Expression`.

Its entries are `Expression` values, but the bracket object itself represents
set-valued / indeterminate mathematical structure rather than one homotopy
element.

Entry order is preserved structurally.

```text
TodaBracket(a,b,c)
!=structural
TodaBracket(a,c,b)
```

This is a representation statement, not a theorem asserting mathematical
inequality of two well-typed brackets.

No constructor-side sorting, permutation normalization, or theorem-aware
canonicalization is performed.

## Toda bracket membership

First-class membership is represented by:

```text
TodaBracketMembershipStatement(
  element=x,
  bracket=TodaBracket(a,b,c),
)
```

with semantics:

```text
x ∈ {a,b,c}
```

This is distinct from the Phase 14 subgroup membership statement:

```text
MembershipStatement(x,A)
```

and the existing subgroup API is not widened to arbitrary set-valued objects.

The bracket entries `a,b,c` are inputs defining the bracket. They are not
candidate values of the bracket.

Therefore:

```text
x ∈ {a,b,c}
↛
x=a
```

```text
x ∈ {a,b,c}
↛
x=b
```

```text
x ∈ {a,b,c}
↛
x=c
```

## Toda bracket definedness

Three-fold bracket definedness is represented separately:

```text
TodaBracketDefinedStatement(
  bracket=TodaBracket(a,b,c),
)
```

Phase 18 connects existing composition / ZERO reasoning to bracket
definedness.

Implemented chain:

```text
a∘b=0
b∘c=0
↓ existing composition equality → generic ZERO
ZERO(a∘b)
ZERO(b∘c)
↓
TodaBracketDefinedStatement({a,b,c})
```

The two zero-composition premises must share the middle entry `b`.

A mismatched pair:

```text
a∘b=0
d∘c=0
```

does not establish `{a,b,c}` definedness.

This Phase trusts already constructed `Composition` facts. Full source / target
sphere validation is not yet introduced.

## Definedness / membership boundary

Definedness and membership remain distinct:

```text
{a,b,c} defined
↛
x ∈ {a,b,c}
```

Zero-composition defining facts do not select a bracket value.

No rule of the form:

```text
a∘b=0
b∘c=0
→
x∈{a,b,c}
```

is introduced.

## Phase 17 indeterminacy coexistence

Toda bracket membership may coexist with existing Phase 17 partial
information about the same element.

Examples:

```text
x ∈ {a,b,c}
x = ±α
```

and:

```text
x ∈ {a,b,c}
x ∈ β+A
```

These statements share the same `x` but remain mathematically distinct.

Phase 18 does not introduce automatic bridges:

```text
x ∈ {a,b,c}
↛
x = ±α
```

```text
x ∈ {a,b,c}
↛
x ∈ β+A
```

and the reverse directions are also absent unless a later concrete theorem
justifies them.

In particular:

```text
x ∈ {a,b,c}
+
x = ±α
↛
x=α
```

and:

```text
x ∈ {a,b,c}
+
x = ±α
↛
x=-α
```

## Provenance

The defining-condition derivation retains the full dependency chain:

```text
known a∘b=0
↓ composition equality → ZERO
ZERO(a∘b)

known b∘c=0
↓ composition equality → ZERO
ZERO(b∘c)

ZERO(a∘b)
+
ZERO(b∘c)
↓ Toda definedness rule
{a,b,c} defined
```

The final definedness `ProofStep` directly records the two ZERO steps as
premises.

Each ZERO step directly records its original known composition equality.

Unrelated facts are not inserted into the direct provenance of the Toda
definedness branch.

## Representative fixed-point scenario

A representative Phase 18 knowledge state may begin with:

```text
a∘b=0
b∘c=0
x∈{a,b,c}
x=±α
```

Active rules:

```text
composition equality → generic ZERO
ZERO + ZERO → Toda bracket definedness
```

Derived knowledge:

```text
ZERO(a∘b)
ZERO(b∘c)
{a,b,c} defined
```

while the given facts:

```text
x∈{a,b,c}
x=±α
```

remain in the same knowledge state.

Not derived:

```text
x=α
```

The representative run reaches:

```text
FIXED_POINT
```

with two productive rounds.

## Termination / inference scope

The current Toda rule family does not introduce recursive structural growth.

For the representative finite knowledge state:

```text
round 1:
  composition equality → ZERO

round 2:
  ZERO + ZERO → definedness

terminal check:
  no new steps
```

An explicit terminal inference round confirms:

```text
new_steps == ()
```

Toda-specific statements remain outside generic equality-rule scope:

```text
TodaBracketDefinedStatement
≠
RelationType.EQUALITY
```

```text
TodaBracketMembershipStatement
≠
RelationType.EQUALITY
```

The generic inference engine remains unchanged.

---


# Phase 19: Toda bracket membership / first theorem bridge

Phase 19 introduces the first actual literature-backed bridge from a concrete
Toda theorem fact to a `TodaBracketMembershipStatement`.

The first actual example is the unstable Toda-bracket fact represented in the
current unindexed proof layer as:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

The literature notation carries an index `_1`. Phase 19 intentionally stores
only the current three-fold unindexed projection:

```text
{η₃,Eν′,ν₇}
```

The missing index is a known representation limitation and is deferred to
Phase 20.

The expression `Eν′` is represented structurally as:

```text
Suspension(ν′)
```

rather than being encoded into one generator name.

## Known membership fact

`TodaBracketMembershipStatement` now supports literature provenance:

```text
element
bracket
source
note
```

A known membership may be introduced as a `ProofRule.GIVEN` step by:

```text
toda_bracket_membership_proof_step()
```

This remains useful for directly stored literature facts.

## Membership theorem fact

Phase 19 adds the narrow theorem statement:

```text
TodaBracketMembershipTheoremStatement
```

with fields:

```text
element
bracket
source
note
```

Its semantics are intentionally narrower than a general theorem language:

```text
for this specific literature-backed bracket,
if the bracket is established as defined,
the specified element is a member
```

The theorem statement is not itself membership:

```text
TodaBracketMembershipTheoremStatement
≠
TodaBracketMembershipStatement
```

A theorem fact may be stored as a `ProofRule.GIVEN` step by:

```text
toda_bracket_membership_theorem_proof_step()
```

No universal theorem hierarchy, quantifier system, or theorem registry is
introduced.

## First theorem bridge

The Phase 19 bridge is:

```text
matching Toda membership theorem fact
+
{a,b,c} defined
↓
x ∈ {a,b,c}
```

implemented by:

```text
toda_bracket_membership_from_theorem_inference_rule()
```

The theorem fact and definedness statement must refer to the same structural
`TodaBracket`.

A mismatched bracket does not trigger the rule.

Critical boundaries:

```text
{a,b,c} defined
↛
x ∈ {a,b,c}
```

```text
Toda theorem fact
↛
x ∈ {a,b,c}
```

Only the combination of the matching theorem fact and established definedness
produces membership.

## Actual ε₃ multi-round chain

The representative actual chain begins with:

```text
η₃∘Eν′ = 0
Eν′∘ν₇ = 0
Toda membership theorem fact for ε₃
```

Using the existing Phase 18 composition / ZERO / definedness rules together
with the Phase 19 theorem bridge:

```text
round 1
η₃∘Eν′ = 0
Eν′∘ν₇ = 0
↓
ZERO(η₃∘Eν′)
ZERO(Eν′∘ν₇)

round 2
ZERO(η₃∘Eν′)
ZERO(Eν′∘ν₇)
↓
{η₃,Eν′,ν₇} defined

round 3
Toda membership theorem fact
+
{η₃,Eν′,ν₇} defined
↓
ε₃ ∈ {η₃,Eν′,ν₇}
```

The run then reaches:

```text
FIXED_POINT
```

with exactly three productive rounds.

## Phase 17 indeterminacy coexistence

The theorem-derived membership can coexist with existing Phase 17 partial
information such as:

```text
ε₃ = ±α
```

and:

```text
ε₃ ∈ β+A
```

without selecting an exact representative.

In particular:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
+
ε₃ = ±α
↛
ε₃ = α
```

```text
ε₃ ∈ {η₃,Eν′,ν₇}
+
ε₃ = ±α
↛
ε₃ = -α
```

```text
ε₃ ∈ {η₃,Eν′,ν₇}
+
ε₃ ∈ β+A
↛
ε₃ = β
```

Toda membership does not automatically generate sign or coset indeterminacy.

No candidate-set intersection or narrowing is introduced.

## Provenance

The theorem-derived membership preserves the complete dependency tree:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
│
├─ Toda membership theorem fact
│
└─ {η₃,Eν′,ν₇} defined
   │
   ├─ ZERO(η₃∘Eν′)
   │  └─ η₃∘Eν′ = 0
   │
   └─ ZERO(Eν′∘ν₇)
      └─ Eν′∘ν₇ = 0
```

The direct premises of the final membership step are exactly:

```text
theorem fact
definedness step
```

Sign / coset facts and unrelated facts do not enter this direct provenance
branch.

No new recursive provenance framework is added.

## Termination / inference scope

The active Phase 19 family is:

```text
composition equality → ZERO
ZERO + ZERO → Toda definedness
Toda theorem fact + Toda definedness → Toda membership
```

For the representative finite knowledge state it reaches a genuine fixed
point:

```text
round_count == 3
termination_reason == FIXED_POINT
```

An explicit terminal inference round confirms:

```text
new_steps == ()
```

The Phase 19 theorem statement remains outside generic equality scope:

```text
TodaBracketMembershipTheoremStatement
≠
RelationType.EQUALITY
```

The existing Toda statements remain outside generic equality scope as well.

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

The current Phase 19 Toda theorem-bridge family is finite for the representative fixed known term set.

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
- general Toda-bracket value-set algebra,
- Toda bracket containment in cosets,
- indexed unstable Toda notation, including the literature `_1` index used by the current ε₃ example,
- stable Toda brackets,
- higher Toda brackets.

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

Phase 19 Toda focused suite:

```powershell
python -m pytest tests/test_toda_rules.py -q
```

Verified result:

```text
36 passed in 3.06s
```

Phase 19 completion full suite:

```text
1064 passed in 61.64s
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

# Phase 18 completion boundary

Phase 18 is complete because the proof layer can now represent a minimal
three-fold unstable Toda bracket without collapsing its set-valued semantics
into an exact value.

Completion means:

1. `TodaBracket` is first-class.
2. `TodaBracket` stores exactly three ordered `Expression` entries.
3. `TodaBracket` itself is not an `Expression`.
4. entry order is preserved structurally.
5. no constructor-side permutation normalization is performed.
6. `TodaBracketMembershipStatement` is first-class.
7. `x∈{a,b,c}` is distinct from subgroup membership.
8. bracket entries are not interpreted as candidate values.
9. `TodaBracketDefinedStatement` is first-class.
10. `a∘b=0` and `b∘c=0` can establish `{a,b,c}` definedness.
11. the existing composition-equality → generic ZERO bridge is reused.
12. the two defining compositions must share the middle entry.
13. mismatched middle entries are rejected.
14. one zero-composition fact alone does not establish definedness.
15. definedness does not imply arbitrary bracket membership.
16. bracket membership does not imply exact equality.
17. bracket membership may coexist with sign indeterminacy.
18. bracket membership may coexist with coset indeterminacy.
19. Toda membership does not automatically imply sign indeterminacy.
20. Toda membership does not automatically imply coset indeterminacy.
21. sign is not selected automatically.
22. provenance traces definedness through both ZERO facts to the original
    composition equalities.
23. unrelated facts do not enter direct Toda provenance.
24. representative Toda + Phase 17 partial-information scenario reaches
    `FIXED_POINT`.
25. the representative scenario uses two productive rounds.
26. an explicit terminal check yields `new_steps == ()`.
27. Toda definedness is outside generic equality-rule scope.
28. Toda membership is outside generic equality-rule scope.
29. no general set-valued expression hierarchy is introduced.
30. no indexed unstable Toda notation is introduced.
31. no stable Toda bracket is introduced.
32. no higher Toda bracket framework is introduced.
33. full source / target typing is not introduced.
34. the generic inference engine remains unchanged.
35. the full regression suite passes.

Phase 18 completion:

```text
tests/test_toda_rules.py
20 passed in 3.36s
```

```text
full suite
1048 passed in 61.09s
```

---

# Phase 19 completion boundary

Phase 19 is complete because an actual literature-backed Toda theorem fact can now be connected to existing bracket definedness and produce theorem-derived membership without collapsing set-valued or indeterminate semantics.

Completion means:

1. the actual ε₃ example is represented in the current unindexed three-fold layer.
2. `Eν′` is structural `Suspension(ν′)`.
3. membership statements can preserve `source` / `note` provenance.
4. a narrow `TodaBracketMembershipTheoremStatement` is first-class.
5. theorem facts can be stored as `ProofRule.GIVEN`.
6. theorem fact and membership conclusion remain distinct.
7. matching theorem fact + definedness derives membership.
8. mismatched brackets are rejected.
9. theorem fact alone does not derive membership.
10. definedness alone does not derive membership.
11. the actual ε₃ chain runs through ZERO, definedness, and membership in three productive rounds.
12. theorem-derived membership coexists with sign indeterminacy.
13. theorem-derived membership coexists with coset indeterminacy.
14. no sign or coset representative is selected automatically.
15. Toda membership does not automatically generate sign or coset indeterminacy.
16. membership provenance reaches the theorem fact and both defining composition equalities.
17. unrelated facts do not enter the direct provenance tree.
18. the representative scenario reaches `FIXED_POINT`.
19. an explicit terminal check yields `new_steps == ()`.
20. `TodaBracketMembershipTheoremStatement` remains outside generic equality scope.
21. no general theorem hierarchy is introduced.
22. no indexed unstable Toda notation is introduced.
23. the literature `_1` index remains intentionally unrepresented until Phase 20.
24. no typed source / target system is introduced.
25. the generic inference engine remains unchanged.
26. the full regression suite passes.

Phase 19 completion:

```text
tests/test_toda_rules.py
36 passed in 3.06s
```

```text
full suite
1064 passed in 61.64s
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
↓
Toda bracket minimum representation
↓
Toda bracket membership / first theorem bridge
```

The next candidate Phase is:

```text
Phase 20: indexed unstable Toda notation
```

with notation such as:

```text
{a,E^t b,E^t c}_t
```

The suspension exponent and bracket index must be represented as distinct
structural fields even when the same symbol `t` appears in notation.

Stable notation:

```text
<a,b,c>
```

remains deferred and must stay distinct from unstable Toda notation.

No general higher-Toda theorem prover, universal set algebra, or fully
quantified theorem language should be introduced before a concrete
mathematical example requires it.
