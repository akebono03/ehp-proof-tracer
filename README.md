# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined
from mathematical input such as EHP exact sequences, element orders, additive
relations, Suspension, Freudenthal theory, composition, generalized Hopf
invariants, homomorphisms, subgroup / modulo information, symbolic scalar
constraints, indeterminacy, Toda brackets, typed homotopy elements, structured
generator notation, and literature-backed facts.

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

`TodaBracket` stores:

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

The same predicate works for symbolic and concrete cases.

Important API boundary:

```text
construction
≠
validation
```

Inconsistent data is still constructible.

No `__post_init__` rejection is introduced.

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

`HomotopyElement` stores:

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

Both must be confirmed compatible for the result to be `True`.

This query is separate from Toda definedness.

```text
type-compatible
≠
composition is zero
≠
Toda bracket defined
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

# Phase 22: Structured generator representation

Phase 22 introduces the minimum structure needed to preserve generator notation
from tables and literature without storing the whole identity only in
`HomotopyElement.name`.

## GeneratorSymbol

New separate structural object:

```text
GeneratorSymbol
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

can be represented as:

```text
ν
=
GeneratorSymbol(family="ν")

ν′
=
GeneratorSymbol(family="ν", decoration="′")

barν
=
GeneratorSymbol(family="ν", decoration="bar")

η₃
=
GeneratorSymbol(family="η", index=3)

μ₃
=
GeneratorSymbol(family="μ", index=3)

ι₇
=
GeneratorSymbol(family="ι", index=7)
```

`GeneratorSymbol` is not an `Expression`.

It represents generator identity / notation, not a homotopy operation node.

## Structural equality

Python equality remains structural.

Therefore:

```text
η₃ == η₃
η₃ != η₄
η₃ != μ₃
η != η₃
```

and:

```text
ν != ν′
ν != barν
ν′ != barν
```

`index=None` and `decoration=None` are not wildcards.

They are ordinary structural field values.

## Decoration semantics

Decoration is currently stored losslessly as:

```text
str | None
```

Phase 22 does not normalize alternate spellings or introduce dedicated decoration
classes.

For example:

```text
"′"
"prime"
"'"
```

are not automatically identified.

Likewise:

```text
"bar"
"\bar"
"¯"
```

are not normalized.

## Indexed generator notation

The same `GeneratorSymbol` structure handles:

```text
η_n
μ_n
ι_n
```

No separate indexed-generator class is introduced.

The `index` field is part of generator identity but is not interpreted by the
expression layer as a source dimension, target dimension, stem, or table key.

## HomotopyElement connection

`HomotopyElement` now stores:

```text
name: str
dimension: int
source: int | None
target: int | None
generator: GeneratorSymbol | None
```

The new field is optional.

This gives the role separation:

```text
GeneratorSymbol
=
generator identity / notation

HomotopyElement
=
homotopy expression + dimension / source / target context
```

Example:

```text
η₃ : S^4 → S^3
```

may be represented by explicitly supplying both pieces of information:

```text
generator = GeneratorSymbol(family="η", index=3)
source = 4
target = 3
```

Critical boundary:

```text
generator notation
↛
automatic source / target typing
```

A `GeneratorSymbol(family="η", index=3)` does not by itself derive:

```text
source = 4
target = 3
```

## Backward compatibility

Legacy construction remains supported:

```text
HomotopyElement(name, dimension)
```

and is equivalent to explicitly supplying:

```text
generator=None
```

Existing helpers remain unchanged:

```text
eta()
nu()
sigma()
```

They continue to return the legacy `HomotopyElement` form.

Phase 22 does not silently migrate existing helpers to structured generators.

The new `generator` field participates in ordinary dataclass structural equality
when it is present.

## Representative literature scenario

Phase 22 can structurally represent:

```text
{η₃,Eν′,ν₇}_1
```

with independent roles:

```text
η₃
=
HomotopyElement(
  ...,
  generator=GeneratorSymbol(family="η", index=3),
)

ν′
=
HomotopyElement(
  ...,
  generator=GeneratorSymbol(family="ν", decoration="′"),
)

Eν′
=
Suspension(ν′)

ν₇
=
HomotopyElement(
  ...,
  generator=GeneratorSymbol(family="ν", index=7),
)

_1
=
TodaBracket.index
```

The suspension operation is not embedded into a generator name.

Thus:

```text
Eν′
=
Suspension(ν′)
```

rather than a new generator family such as `"Eν′"`.

## Validation boundary

Phase 22 preserves:

```text
constructible
≠
validated
```

For example, a `HomotopyElement` with a display `name` that disagrees with its
`generator` remains constructible.

Phase 22 does not add:

```text
name / generator consistency validation
generator / dimension consistency validation
generator / source-target consistency validation
```

These require a later mathematical typing / table layer.

## Phase 22 completion boundary

Implemented:

1. `GeneratorSymbol`.
2. `GeneratorSymbol.family`.
3. optional `GeneratorSymbol.index`.
4. optional `GeneratorSymbol.decoration`.
5. `GeneratorSymbol` is separate from `Expression`.
6. family participates in structural equality.
7. index participates in structural equality.
8. decoration participates in structural equality.
9. `ν`, `ν′`, and decorated `ν` remain distinct.
10. `η_n`, `μ_n`, and `ι_n` are representable with the same structure.
11. indexed and unindexed generators remain distinct.
12. `HomotopyElement.generator`.
13. generator and source / target context can coexist.
14. generator notation does not derive typing.
15. legacy `HomotopyElement(name, dimension)` remains supported.
16. omitted generator and `generator=None` are equivalent.
17. existing `eta()`, `nu()`, `sigma()` helpers remain unchanged.
18. generator participates in `HomotopyElement` structural equality when present.
19. `Eν′` remains a `Suspension` node around `ν′`.
20. `{η₃,Eν′,ν₇}_1` is losslessly structurally representable.
21. name / generator mismatch remains constructible.
22. no decoration normalization is introduced.
23. no generator table lookup is introduced.
24. no source / target automatic derivation is introduced.
25. no stable / unstable generator classification is introduced.
26. no ambient homotopy-group / stem validation is introduced.
27. no indexed Toda theorem applicability is introduced.
28. generic inference engine remains unchanged.
29. full regression passes.

Verified Phase 22 completion:

```text
tests/test_expression.py
118 passed in 0.44s
```

```text
full suite
1153 passed in 24.83s
```

---

# Current limitations

Not yet implemented as general systems:

- generator table lookup,
- automatic source / target derivation from generator identity,
- name / generator consistency validation,
- generator / dimension / typing validation,
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

Verified current Phase 22 result:

```text
118 passed in 0.44s
```

Full suite:

```powershell
python -m pytest -q
```

Verified:

```text
1153 passed in 24.83s
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
↓
Structured generator representation
```

Natural next candidate:

```text
Phase 23
Indexed Toda theorem / validity connection
```

The next Phase should use actual literature facts and explicit side conditions to
connect indexed Toda representation with theorem applicability.

Important:

```text
structured generator representation
↛
theorem applicability
```

and:

```text
type compatibility
↛
Toda definedness
↛
membership
```

Stable homotopy notation, stable Toda notation, and higher Toda brackets remain
later layers.
