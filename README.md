# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined
from mathematical input such as EHP exact sequences, element orders, additive
relations, Suspension, Freudenthal theory, composition, generalized Hopf
invariants, homomorphisms, subgroup / modulo information, symbolic scalar
constraints, indeterminacy, Toda brackets, typed homotopy elements, structured
generator notation, indexed Toda theorem facts, and literature-backed facts.

The project separates:

```text
mathematical rule / theorem
generic inference mechanism
abelian-group calculation
```

Development principle:

```text
actual mathematical need
↓
minimal representation
↓
domain rule when needed
↓
existing generic engine
```

---

# Current status

Completed:

- Phase 1: finite abelian-group calculations
- Phase 2: structured subgroup calculations
- Phase 3: quotient / exact sequence / extension
- Phase 4: presentation-based finitely generated abelian groups
- Phase 5: generic proof / inference engine
- Phase 6: EHP domain inference
- Phase 7: ORDER reasoning
- Phase 8: Suspension reasoning
- Phase 9: Freudenthal / stable-range reasoning
- Phase 10: composition / Suspension-composition functoriality
- Phase 11: generalized Hopf-invariant reasoning
- Phase 12: additive expressions
- Phase 13: homomorphism reasoning
- Phase 14: set / subgroup reasoning
- Phase 15: coset / modulo reasoning
- Phase 16: symbolic scalar constraints
- Phase 17: indeterminacy
- Phase 18: Toda bracket minimum representation
- Phase 19: Toda membership / first theorem bridge
- Phase 20: indexed unstable Toda notation
- Phase 21: typed homotopy elements / source-target context
- Phase 22: structured generator representation
- Phase 23: indexed Toda theorem / validity connection

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

---

# Expression model

Current expression classes include:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

Separate structural objects include:

```text
MapSymbol
ScalarSymbol
GeneratorSymbol
TodaBracket
IndexedTodaBracketData
```

The expression layer is primarily structural syntax.

Phase 21 adds minimal source / target context and pure compatibility queries.

Phase 22 adds structured generator identity while preserving the existing
`HomotopyElement` API and keeping generator notation separate from typing rules,
table lookup, and theorem applicability.

Phase 23 connects indexed Toda theorem facts to membership under explicit
matching / validity guards while preserving the narrow literature-backed bridge
for specific actual notation.

---

# Toda bracket model

`TodaBracket` represents a three-fold unstable bracket:

```text
{a,b,c}
```

and stores an optional index:

```text
index: int | ScalarSymbol | None
```

Therefore:

```text
{a,b,c}
{a,b,c}_1
{a,b,c}_2
{a,b,c}_t
```

remain structurally distinct.

Dedicated statements represent:

```text
{a,b,c} defined
x∈{a,b,c}
```

Important:

```text
definedness
↛
membership
```

```text
membership
↛
exact equality
```

---

# Indexed unstable Toda notation

The canonical indexed structural form is:

```text
{a,E^t b,E^t c}_t
```

with:

```text
TodaBracket.index
IteratedSuspension
IndexedTodaBracketData
```

`IndexedTodaBracketData.is_consistent()` checks:

```text
bracket.second
==
IteratedSuspension(second_base, suspension_exponent)

bracket.third
==
IteratedSuspension(third_base, suspension_exponent)

bracket.index
==
suspension_exponent
```

Important:

```text
constructible
≠
structurally consistent
```

```text
structurally consistent
≠
theorem applicable
```

```text
IteratedSuspension(α,1)
!=structural
Suspension(α)
```

No automatic normalization is performed.

---

# Typed homotopy elements

`HomotopyElement` stores:

```text
name
dimension
source
target
generator
```

with:

```text
source: int | None
target: int | None
generator: GeneratorSymbol | None
```

For typed input:

```text
α : S^m → S^n
```

Suspension exposes:

```text
Eα : S^(m+1) → S^(n+1)
```

For concrete non-negative `r`:

```text
E^r α : S^(m+r) → S^(n+r)
```

For symbolic exponents, no symbolic sphere-dimension algebra is introduced.

`Composition.is_type_compatible()` checks:

```text
left.source == right.target
```

and:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

checks both displayed entry compositions.

Important:

```text
type-compatible
≠
composition is zero
≠
Toda bracket defined
```

Current boolean semantics are intentionally narrow:

```text
True
=
compatibility is confirmed

False
=
compatibility is not confirmed
```

Unknown typing is not treated as a wildcard.

---

# Structured generator representation

`GeneratorSymbol` stores:

```text
family: str
index: int | None
decoration: str | None
```

Examples:

```text
ν
ν′
barν
η₃
μ₃
ι₇
```

`GeneratorSymbol` is not an `Expression`.

Structural distinctions include:

```text
ν != ν′
ν′ != barν
η₃ != η₄
η₃ != μ₃
ι₇ != ι₈
```

`HomotopyElement.generator` is optional, so legacy construction remains valid:

```text
HomotopyElement(name, dimension)
```

Important:

```text
generator notation
↛
automatic source / target typing
```

```text
generator identity
!=
Suspension operation
```

For example:

```text
Eν′
=
Suspension(ν′)
```

rather than a new generator family.

---

# Phase 23: Indexed Toda theorem / validity connection

Phase 23 connects indexed Toda theorem facts to Toda membership while preserving
the distinction between structural representation and theorem applicability.

## Indexed theorem fact

The existing narrow theorem statement is reused:

```text
TodaBracketMembershipTheoremStatement
```

It can now losslessly store an indexed bracket such as:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

including:

```text
value
full bracket structure
bracket index
generator family / index / decoration
source
note
```

No parallel indexed theorem-statement hierarchy is introduced.

## Bracket index matching

The theorem bridge uses whole-bracket structural equality.

Therefore:

```text
{a,b,c}_1
==
{a,b,c}_1
```

may match, while:

```text
{a,b,c}_1
!=
{a,b,c}_2
```

and:

```text
{a,b,c}_1
!=
{a,b,c}
```

do not match.

`index=None` is not a wildcard.

## Generator structure matching

Generator family, generator index, and decoration participate in structural
matching through `HomotopyElement.generator`.

Therefore a theorem application is rejected when a bracket differs only in:

```text
GeneratorSymbol.family
GeneratorSymbol.index
GeneratorSymbol.decoration
```

even if display names are otherwise equal.

No special generator-specific matching code is required.

## Definedness dependency

The narrow theorem bridge preserves:

```text
matching theorem fact
+
matching TodaBracketDefinedStatement
↓
TodaBracketMembershipStatement
```

and:

```text
theorem fact alone
↛
membership
```

```text
definedness alone
↛
membership
```

## Canonical indexed guarded bridge

Phase 23 adds:

```text
indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data
)
```

for canonical indexed data.

Its guard requires:

```text
indexed_data.is_consistent()
```

and:

```text
indexed_data.bracket
.are_defining_compositions_type_compatible()
```

together with exact structural agreement between:

```text
theorem bracket
definedness bracket
indexed_data.bracket
```

The guarded bridge therefore has the form:

```text
matching indexed theorem fact
+
matching definedness
+
structural consistency
+
confirmed typing compatibility
↓
indexed Toda membership
```

Important:

```text
structural consistency alone
↛
membership
```

```text
type compatibility alone
↛
membership
```

```text
unknown typing
→
guard rejection
```

No typing fact statement hierarchy is introduced.

## General canonical form vs specific literature form

The canonical guarded bridge targets structures of the form:

```text
{a,E^t b,E^t c}_t
```

represented by `IndexedTodaBracketData`.

The actual literature-backed representative:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

is stored losslessly as:

```text
η₃
Eν′ = Suspension(ν′)
ν₇
index = 1
```

This specific form is intentionally not forced into canonical
`IndexedTodaBracketData`, because:

```text
Suspension(ν′)
!=structural
IteratedSuspension(ν′,1)
```

and the project does not currently infer an underlying `ν₆` from `ν₇`.

Therefore the actual `ε₃` theorem continues to use the narrow literature-backed
bridge:

```text
specific theorem fact
+
exactly matching definedness
↓
membership
```

This separation is intentional.

## Provenance

Derived indexed membership keeps direct provenance:

```text
membership
├── theorem step
└── definedness step
```

Unrelated facts are not included in the membership premises.

The theorem `source` and `note` are propagated to the derived membership.

## No indexed-to-unindexed collapse

An indexed conclusion remains indexed.

For example:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

does not automatically create:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

The Phase 19 unindexed projection is no longer required for the actual
literature notation.

---

# Phase 23 completion boundary

Implemented:

1. indexed Toda theorem facts are losslessly representable.
2. existing `TodaBracketMembershipTheoremStatement` is reused.
3. bracket index participates in theorem matching.
4. indexed and unindexed brackets remain distinct.
5. generator family participates in theorem matching.
6. generator index participates in theorem matching.
7. generator decoration participates in theorem matching.
8. theorem fact alone does not imply membership.
9. definedness alone does not imply membership.
10. matching theorem + matching definedness derives membership.
11. canonical indexed structural consistency guard.
12. canonical indexed typing compatibility guard.
13. inconsistent canonical indexed data is rejected.
14. known type mismatch is rejected.
15. unknown typing is rejected.
16. canonical guarded bridge reaches a fixed point.
17. guarded bridge provenance excludes unrelated facts.
18. theorem source / note propagate to membership.
19. actual `ε₃ ∈ {η₃,Eν′,ν₇}_1` is represented losslessly.
20. actual `ε₃` theorem uses the narrow literature-backed bridge.
21. actual `ε₃` notation is not forced into `IndexedTodaBracketData`.
22. `Suspension(ν′)` is not normalized to `IteratedSuspension(ν′,1)`.
23. no inverse generator lookup such as `ν₇ → ν₆` is introduced.
24. indexed membership does not collapse to an unindexed projection.
25. generic inference engine remains unchanged.

---

# Current limitations

Not yet implemented as general systems:

- generator table lookup,
- automatic source / target derivation from generator identity,
- name / generator consistency validation,
- generator / dimension / typing validation,
- ambient homotopy-group / stem / stable-context typing,
- theorem-repository / knowledge-table integration,
- general theorem quantification,
- general theorem-side condition language,
- canonicalization between `Suspension(α)` and `IteratedSuspension(α,1)`,
- automatic recovery of generator bases from suspended indexed generators,
- general indexed Toda definedness theorem system,
- stable homotopy-group model,
- stable Toda bracket `<a,b,c>`,
- higher / variable-arity Toda brackets,
- general candidate-set algebra.

---

# Tests

Focused Toda test:

```powershell
python -m pytest tests/test_toda_rules.py -q
```

Verified current Phase 23 result:

```text
66 passed in 1.01s
```

Full suite:

```powershell
python -m pytest -q
```

Verified:

```text
1175 passed in 22.96s
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

# Next development boundary

The completed dependency chain now includes:

```text
Additive expressions
↓
Homomorphism reasoning
↓
Set / subgroup reasoning
↓
Coset / modulo reasoning
↓
Symbolic scalar constraints
↓
Indeterminacy
↓
Toda bracket minimum representation
↓
Toda membership theorem bridge
↓
Indexed unstable Toda notation
↓
Typed homotopy elements / source-target context
↓
Structured generator representation
↓
Indexed Toda theorem / validity connection
```

Natural next candidate:

```text
Phase 24
Theorem fact / knowledge-table integration
```

The next layer should focus on storing and supplying literature-backed theorem
facts and related metadata without introducing a universal theorem prover.

Potential later dependencies include:

```text
theorem / knowledge table
↓
generator typing / ambient-group facts
↓
stable homotopy representation
↓
stable Toda brackets
```

Phase numbering after Phase 23 remains provisional and should continue to follow
actual mathematical need.
