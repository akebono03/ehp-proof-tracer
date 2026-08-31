# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined
from mathematical input such as EHP exact sequences, element orders, additive
relations, Suspension, Freudenthal theory, composition, generalized Hopf
invariants, homomorphisms, subgroup / modulo information, symbolic scalar
constraints, indeterminacy, Toda brackets, and literature-backed facts.

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
TodaBracket
IndexedTodaBracketData
```

The expression layer is primarily structural syntax. Phase 21 adds minimal
source / target context and pure compatibility queries, but it still does not
perform theorem application, constructor-level validity enforcement, symbolic
dimension solving, candidate enumeration, or Toda theorem applicability.

---

# Phase 18: Toda bracket minimum representation

`TodaBracket` represents a three-fold unstable bracket:

```text
{a,b,c}
```

Dedicated statements represent:

```text
{a,b,c} defined
x∈{a,b,c}
```

Definedness may be derived from:

```text
a∘b=0
b∘c=0
↓
ZERO(a∘b)
ZERO(b∘c)
↓
{a,b,c} defined
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

# Phase 19: Toda membership theorem bridge

Phase 19 introduced a narrow literature-backed theorem bridge:

```text
matching theorem fact
+
matching bracket definedness
↓
Toda bracket membership
```

The actual source notation contains:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Phase 19 intentionally represented only:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

because bracket index information had not yet been modeled.

Verified at Phase 19 completion:

```text
tests/test_toda_rules.py
36 passed in 3.06s
```

```text
full suite
1064 passed in 61.64s
```

---

# Phase 20: Indexed unstable Toda notation

Phase 20 closes the Phase 19 representation gap and generalizes to:

```text
{a,E^t b,E^t c}_t
```

## TodaBracket.index

`TodaBracket` now stores:

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

remain structurally distinguishable.

The index is not display-only decoration.

## IteratedSuspension

`IteratedSuspension` represents:

```text
E^n α
E^t α
```

with:

```text
exponent: int | ScalarSymbol
```

Structural boundaries are intentional:

```text
IteratedSuspension(α,1)
!=
Suspension(α)
```

```text
IteratedSuspension(α,2)
!=
Suspension(Suspension(α))
```

No constructor normalization is performed.

## IndexedTodaBracketData

`IndexedTodaBracketData` stores:

```text
bracket
second_base
third_base
suspension_exponent
```

where:

```text
suspension_exponent: int | ScalarSymbol
```

This preserves the distinction between:

```text
suspension exponent
bracket index
```

even when both are written with the same symbol `t`.

## Representative indexed form

Phase 20 can structurally represent:

```text
{a,E^t b,E^t c}_t
```

with:

```text
second = E^t(second_base)
third  = E^t(third_base)
bracket.index = t
suspension_exponent = t
```

## Consistency predicate

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

The same predicate works for symbolic and concrete cases:

```text
{a,E^t b,E^t c}_t
{a,E^2 b,E^2 c}_2
```

Important API boundary:

```text
construction
≠
validation
```

Inconsistent data is still constructible.

For example:

```text
suspension_exponent=t
bracket.index=s
```

is representable, but:

```text
is_consistent() == False
```

No `__post_init__` rejection is introduced.

---

# Phase 20 completion boundary

Phase 20 completion means:

1. `TodaBracket.index` is explicit.
2. unindexed brackets remain supported.
3. concrete bracket indices are supported.
4. symbolic bracket indices are supported.
5. `IteratedSuspension` is first-class.
6. concrete iterated exponents are supported.
7. symbolic iterated exponents are supported.
8. iterated suspension is not normalized to ordinary nested `Suspension`.
9. `IndexedTodaBracketData` stores underlying second / third bases.
10. suspension exponent is separate from bracket index.
11. symbolic suspension exponent is supported.
12. `{a,E^t b,E^t c}_t` is structurally representable.
13. `is_consistent()` checks second-entry correspondence.
14. `is_consistent()` checks third-entry correspondence.
15. `is_consistent()` checks bracket-index correspondence.
16. symbolic consistent data returns `True`.
17. concrete consistent data returns `True`.
18. index mismatch returns `False`.
19. entry mismatch returns `False`.
20. inconsistent data remains constructible.
21. consistency is not theorem applicability.
22. consistency is not inference.
23. no general symbolic exponent normalization is introduced.
24. no stable Toda bracket is introduced.
25. no higher Toda bracket is introduced.
26. no full source / target typing is introduced.
27. the generic inference engine remains unchanged.
28. full regression passes.

Verified Phase 20 completion:

```text
tests/test_expression.py
64 passed in 1.46s
```

```text
full suite
1098 passed in 61.30s
```

---


# Phase 21: Typed homotopy elements / source-target context

Phase 21 introduces the minimum source / target information needed to ask whether
homotopy-theoretic compositions and Toda-bracket entry chains are type-compatible.

## Typed HomotopyElement

`HomotopyElement` now stores:

```text
name
dimension
source
target
```

with:

```text
source: int | None
target: int | None
```

Example:

```text
α : S^5 → S^3
```

can be represented with:

```text
source = 5
target = 3
```

Typed source / target fields participate in structural equality.

Therefore:

```text
α : S^5 → S^3
!=structural
α : S^6 → S^3
```

and typed / untyped forms remain structurally distinct.

## Suspension typing

For typed input:

```text
α : S^m → S^n
```

ordinary suspension exposes derived typing:

```text
Eα : S^(m+1) → S^(n+1)
```

Unknown source / target information remains unknown.

Nested ordinary suspensions repeat the shift.

## IteratedSuspension typing

For a concrete non-negative exponent `r`:

```text
E^r α : S^(m+r) → S^(n+r)
```

is available as derived source / target information.

For a symbolic exponent:

```text
E^t α
```

Phase 21 does not construct symbolic sphere dimensions such as `m+t`.

Therefore:

```text
source = None
target = None
```

for the concrete typing query.

Negative exponents remain constructible as syntax, but do not produce concrete
source / target typing.

## Composition compatibility

`Composition.is_type_compatible()` checks the boundary:

```text
α : S^m → S^n
β : S^p → S^m

α∘β
```

using:

```text
α.source == β.target
```

The predicate is a pure query.

Important:

```text
constructible
≠
type-compatible
```

A mismatched `Composition` remains representable.

Current boolean semantics are intentionally narrow:

```text
True
=
compatibility is confirmed

False
=
compatibility is not confirmed
```

Thus known mismatch and unknown typing are not yet separated into a three-valued
status model.

## Toda entry compatibility

`TodaBracket.are_defining_compositions_type_compatible()` checks both displayed
entry compositions:

```text
a∘b
b∘c
```

using the existing composition compatibility predicate.

Both must be confirmed compatible for the result to be `True`.

This query is separate from Toda definedness.

```text
type-compatible
≠
composition is zero
≠
Toda bracket defined
```

No Toda inference rule was changed in Phase 21.

## Representative scenario

Phase 21 fixes an integrated scenario connecting:

```text
typed HomotopyElement
↓
ordinary Suspension shift
↓
concrete IteratedSuspension shift
↓
Composition compatibility
↓
Toda entry compatibility
```

while preserving the inference boundary:

```text
typing compatibility
↛
ZERO
↛
Toda definedness
```

## Phase 21 completion boundary

Implemented:

```text
HomotopyElement.source
HomotopyElement.target
typed structural equality
Suspension.source
Suspension.target
IteratedSuspension concrete source / target shift
Composition.is_type_compatible()
TodaBracket.are_defining_compositions_type_compatible()
```

Not implemented:

```text
constructor rejection for type mismatch
three-valued TypeCompatibility
symbolic sphere-dimension arithmetic
Composition source / target derivation
ambient homotopy-group validation
stem validation
stable / unstable context
typing guard on Toda definedness inference
indexed Toda theorem applicability from typing
structured generator representation
stable homotopy-group model
stable Toda bracket
higher Toda bracket
```

Generic inference engine:

```text
unchanged
```

Verified Phase 21 completion:

```text
tests/test_expression.py
90 passed in 0.33s
```

```text
tests/test_toda_rules.py
44 passed in 0.73s
```

```text
full suite
1125 passed in 22.75s
```

---

# Current limitations

Not yet implemented as general systems:

- ambient homotopy-group / stem / stable-context typing,
- indexed Toda theorem applicability based on typing,
- general symbolic exponent arithmetic,
- automatic `Suspension` / `IteratedSuspension` normalization,
- stable homotopy-group model,
- stable Toda bracket `<a,b,c>`,
- higher / variable-arity Toda brackets,
- general theorem quantification,
- general candidate-set algebra.

---

# Tests

Run:

```powershell
python -m pytest tests/test_expression.py -q
```

Verified current Phase 21 result:

```text
90 passed in 0.33s
```

Full suite:

```powershell
python -m pytest -q
```

Verified:

```text
1125 passed in 22.75s
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
```

Natural next candidate:

```text
Phase 22
structured generator representation
```

The next Phase should introduce only the minimum generator structure required by
actual tables or literature input, keeping notation such as `ν`, `ν′`, decorated
families, and indexed unstable generators structurally distinct.

Indexed Toda theorem applicability, stable homotopy notation, and stable Toda
notation remain later layers.
