# ehp_proof 設計メモ

この文書は Phase 22 完了時点の current architecture / semantics /
design boundary を正本としてまとめる。

過去の development log にある「未実装」「今後の課題」は historical
statement であり、current specification とは限らない。

---

# 1. 全体アーキテクチャ

```text
homotopy / EHP domain inference rules
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

基本原則:

```text
new mathematical knowledge
=
new domain InferenceRule
```

generic engine を変更するのは actual mathematical rule が current rule
language では正しく表現できないと実証された場合のみ。

---

# 2. Algebra layer

責務:

- finitely generated abelian groups
- relation matrices
- integer lattices
- HNF / SNF
- homomorphisms
- kernel / image / cokernel
- subgroup / quotient
- exact sequence

群は:

```text
Z^r ⊕ finite torsion
```

として扱う。

proof-level Toda index / iterated suspension / generator notation /
indeterminacy semantics は algebra layer に埋め込まない。

---

# 3. Expression layer

Current tree:

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

Separate structural objects:

```text
MapSymbol
ScalarSymbol
GeneratorSymbol
TodaBracket
IndexedTodaBracketData
```

Expression layer は syntax / structure を lossless に保持する。

担当しないもの:

- theorem applicability
- scalar solving
- candidate enumeration
- stable-range judgement
- constructor-level source / target validation
- ambient homotopy-group validation
- generator-table lookup
- generator-to-typing inference
- equality / zero proof
- commutative / associative normalization
- repeated-sum expansion
- iterated-suspension normalization
- Toda value selection
- Toda theorem applicability

---

# 4. Structural equality principle

Python equality は structural equality。

Mathematical equality とは区別する。

Examples:

```text
Sum(alpha,beta)
!=structural
Sum(beta,alpha)
```

```text
Multiple(2,alpha)
!=structural
Sum(alpha,alpha)
```

```text
IteratedSuspension(alpha,1)
!=structural
Suspension(alpha)
```

```text
GeneratorSymbol(family="η",index=3)
!=structural
GeneratorSymbol(family="μ",index=3)
```

数学的に等しい場合は explicit theorem / relation で扱う。

---

# 5. ScalarSymbol semantics

`ScalarSymbol` は symbolic integer syntax。

Uses:

```text
kβ
E^t α
```

Current structural types:

```text
Multiple.coefficient:
  int | ScalarSymbol
```

```text
IteratedSuspension.exponent:
  int | ScalarSymbol
```

`ScalarSymbol("t")` は concrete integer を選択しない。

General symbolic arithmetic object ではない。

---

# 6. Generic inference engine boundary

Engine responsibilities:

```text
match
bind
apply
deduplicate
iterate
trace
```

Termination:

```text
FIXED_POINT
MAX_ROUNDS
```

`max_rounds` は safety bound。

Phase 22 は structural-expression layer の拡張であり、
generic inference engine を変更しない。

---

# 7. Phase 14–17 summary

## Phase 14

```text
α∈A
A⊆B
A=B
α∈Ker(f)
α∈Im(f)
```

Role-aware subgroup reference を保持。

## Phase 15

```text
α+A
α≡β mod A
α+A=β+A
```

Modulo と ordinary equality を区別。

## Phase 16

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

General symbolic arithmetic solver は導入しない。

## Phase 17

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

Partial information を exact value に潰さない。

---

# 8. Phase 18 Toda design

`TodaBracket` は three-fold unstable Toda bracket の structural object。

```text
{a,b,c}
```

Dedicated statements:

```text
TodaBracketDefinedStatement
TodaBracketMembershipStatement
```

Boundary:

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

`TodaBracket` 自体は `Expression` ではない。

---

# 9. Phase 19 theorem bridge

追加:

```text
TodaBracketMembershipTheoremStatement
```

Bridge:

```text
matching theorem fact
+
matching bracket definedness
↓
Toda bracket membership
```

Actual source notation:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Phase 19 では `_1` を保持できなかった。

この gap が Phase 20 の actual requirement。

---

# 10. Phase 20 design

Target:

```text
{a,E^t b,E^t c}_t
```

Current:

```text
TodaBracket.index:
  int | ScalarSymbol | None
```

```text
IteratedSuspension.exponent:
  int | ScalarSymbol
```

```text
IndexedTodaBracketData.suspension_exponent:
  int | ScalarSymbol
```

Key boundary:

```text
IteratedSuspension(α,1)
!=structural
Suspension(α)
```

```text
suspension exponent role
!=
bracket index role
```

`IndexedTodaBracketData.is_consistent()` は pure structural query。

```text
constructible
≠
consistent
```

```text
consistent
≠
theorem applicable
```

---

# 11. Phase 21 typed homotopy-element semantics

Current `HomotopyElement` before Phase 22 connection:

```text
HomotopyElement
  name: str
  dimension: int
  source: int | None
  target: int | None
```

Phase 21 introduces minimal concrete source / target context without introducing a
universal homotopy type system.

`None` is not a wildcard.

It means that the corresponding concrete typing information is not stored.

---

# 12. Suspension source / target semantics

For:

```text
α : S^m → S^n
```

ordinary suspension exposes:

```text
Eα : S^(m+1) → S^(n+1)
```

Known information shifts by `+1`.

Unknown information remains `None`.

No constructor validation is introduced.

---

# 13. IteratedSuspension typing semantics

For concrete non-negative:

```text
r: int
```

Phase 21 derives:

```text
E^r α : S^(m+r) → S^(n+r)
```

For:

```text
ScalarSymbol("t")
```

Phase 21 does not create symbolic dimension expressions.

Therefore concrete typing query returns:

```text
source=None
target=None
```

for symbolic exponent.

Negative exponents remain structurally constructible but do not produce concrete
source / target typing.

---

# 14. Composition compatibility semantics

Current:

```text
Composition.is_type_compatible() -> bool
```

For:

```text
α : S^m → S^n
β : S^p → S^m
```

checks:

```text
α.source == β.target
```

The predicate returns `True` only when the required boundary dimensions are both
concrete and equal.

Current `False` intentionally combines:

```text
known mismatch
unknown typing
unsupported typing
```

Critical:

```text
Composition(...)
```

remains constructible even when incompatible.

---

# 15. Toda entry compatibility semantics

For:

```text
{a,b,c}
```

current pure query:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

checks:

```text
a∘b
b∘c
```

Both must be confirmed compatible.

Critical separation:

```text
entry compatibility
≠
ZERO composition
```

and:

```text
entry compatibility
≠
Toda definedness
```

---

# 16. Phase 22 design goal

Target actual notation:

```text
ν
ν′
decorated ν
η_n
μ_n
ι_n
```

Purpose:

```text
display-only name string
↓
minimum structural generator identity
```

Constraints:

1. existing `HomotopyElement` API を不必要に壊さない。
2. generator notation と homotopy expression を分離する。
3. family / index / decoration を structural に保持する。
4. `Eν′` の `E` を generator name に埋め込まない。
5. generator identity から source / target を自動推論しない。
6. name / generator の consistency validation を先取りしない。
7. generator table を先取りしない。
8. stable / unstable classification を先取りしない。
9. indexed Toda theorem applicability を先取りしない。
10. generic inference engine を変更しない。

---

# 17. GeneratorSymbol semantics

Current:

```text
GeneratorSymbol
  family: str
  index: int | None
  decoration: str | None
```

`GeneratorSymbol` は `Expression` ではない。

Role:

```text
GeneratorSymbol
=
generator identity / notation
```

Examples:

```text
GeneratorSymbol(family="ν")
```

represents:

```text
ν
```

```text
GeneratorSymbol(
  family="ν",
  decoration="′",
)
```

represents:

```text
ν′
```

```text
GeneratorSymbol(
  family="η",
  index=3,
)
```

represents:

```text
η₃
```

---

# 18. Generator structural equality

All fields participate in ordinary dataclass structural equality.

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

Important:

```text
index=None
```

is not a wildcard.

Likewise:

```text
decoration=None
```

is not a wildcard.

They are ordinary stored structural values.

---

# 19. Decoration semantics

Current type:

```text
str | None
```

Examples:

```text
"′"
"bar"
```

Phase 22 deliberately does not introduce:

```text
PrimeDecoration
BarDecoration
TildeDecoration
HatDecoration
```

and does not normalize alternate spellings.

Therefore:

```text
"′"
"prime"
"'"
```

are not automatically equal.

The same applies to possible bar / tilde / hat spellings.

This is a representation layer, not a notation-normalization system.

---

# 20. Indexed generator semantics

The same `GeneratorSymbol` structure represents:

```text
η_n
μ_n
ι_n
```

Examples:

```text
η₃
=
GeneratorSymbol(family="η",index=3)
```

```text
μ₃
=
GeneratorSymbol(family="μ",index=3)
```

```text
ι₇
=
GeneratorSymbol(family="ι",index=7)
```

No parallel indexed-generator hierarchy is introduced.

Important role separation:

```text
GeneratorSymbol.index
!=
source
!=
target
!=
stem
```

The expression layer does not interpret `index=3` as a sphere dimension theorem.

---

# 21. HomotopyElement generator connection

Current Phase 22 shape:

```text
HomotopyElement
  name: str
  dimension: int
  source: int | None
  target: int | None
  generator: GeneratorSymbol | None
```

Role separation:

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

may be represented by explicitly storing:

```text
generator=GeneratorSymbol(family="η",index=3)
source=4
target=3
```

This is explicit data, not an automatic theorem.

---

# 22. Generator / typing boundary

Critical:

```text
generator notation
↛
automatic typing
```

For:

```text
HomotopyElement(
  generator=GeneratorSymbol(family="η",index=3),
)
```

without explicit source / target:

```text
source=None
target=None
```

remains the result.

Phase 22 does not implement:

```text
η_n → S^(n+1) → S^n
```

as an automatic rule.

Likewise no automatic typing is added for:

```text
ν_n
μ_n
ι_n
ν′
```

Typing knowledge belongs to a later table / theorem / validation layer.

---

# 23. HomotopyElement backward compatibility

The `generator` field is optional.

Legacy:

```text
HomotopyElement(name, dimension)
```

remains supported.

Omitted generator is equivalent to:

```text
generator=None
```

Existing helpers remain unchanged:

```text
eta()
nu()
sigma()
```

Phase 22 does not automatically change them to return structured-generator forms.

This avoids unexpected structural-equality changes in existing code and tests.

When a generator is explicitly present, it participates in ordinary dataclass
structural equality.

---

# 24. Validation boundary

Phase 22 preserves:

```text
constructible
≠
validated
```

For example:

```text
name="η₃"
generator=GeneratorSymbol(family="μ",index=3)
```

remains constructible.

Phase 22 does not check:

```text
name ↔ generator
dimension ↔ generator
source / target ↔ generator
stable / unstable role
ambient homotopy group
```

This is intentional.

Structural representation is complete before theorem-aware validation is added.

---

# 25. Suspension / generator role separation

For:

```text
Eν′
```

storage is:

```text
Suspension(
  expression=
    HomotopyElement(
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    ),
)
```

The operation `E` is not folded into:

```text
family="Eν"
```

or:

```text
name="Eν′"
```

as a new generator identity.

Thus:

```text
generator identity
!=
homotopy operation
```

---

# 26. Phase 22 representative literature scenario

Representative notation:

```text
{η₃,Eν′,ν₇}_1
```

Structural roles:

```text
η₃
=
GeneratorSymbol(family="η",index=3)
```

```text
ν′
=
GeneratorSymbol(family="ν",decoration="′")
```

```text
Eν′
=
Suspension(ν′)
```

```text
ν₇
=
GeneratorSymbol(family="ν",index=7)
```

```text
_1
=
TodaBracket.index
```

This is lossless at the current representation level.

No Toda membership conclusion follows merely from this construction.

---

# 27. Phase 22 completion criteria

1. `GeneratorSymbol`.
2. family field.
3. optional index.
4. optional decoration.
5. `GeneratorSymbol` separate from `Expression`.
6. family structural equality.
7. index structural equality.
8. decoration structural equality.
9. indexed / unindexed distinction.
10. undecorated / decorated distinction.
11. `ν`, `ν′`, decorated `ν` distinction.
12. `η_n` representation.
13. `μ_n` representation.
14. `ι_n` representation.
15. one structure shared by all indexed generator families.
16. `HomotopyElement.generator`.
17. generator + source / target coexistence.
18. generator does not derive source / target.
19. legacy constructor compatibility.
20. `generator=None` compatibility.
21. existing `eta()`, `nu()`, `sigma()` compatibility.
22. generator participates in HomotopyElement structural equality when present.
23. `Eν′` remains `Suspension(ν′)`.
24. representative `{η₃,Eν′,ν₇}_1`.
25. name / generator mismatch remains constructible.
26. no decoration normalization.
27. no constructor validation.
28. no generator lookup table.
29. no automatic generator typing.
30. no ambient homotopy-group validation.
31. no stem / stable-context classification.
32. no indexed Toda theorem applicability.
33. no generic-engine change.
34. full regression PASS.

Verified:

```text
tests/test_expression.py
118 passed in 0.44s
```

```text
full suite
1153 passed in 24.83s
```

---

# 28. Phase 22 non-goals

Not implemented:

- decoration enum / canonicalization,
- multiple-decoration grammar,
- generator-name parser,
- generator factory registry,
- generator table lookup,
- automatic source / target derivation,
- generator / dimension validation,
- name / generator consistency validation,
- ambient homotopy-group validation,
- stem validation,
- stable / unstable generator classification,
- automatic structured conversion of `eta()`, `nu()`, `sigma()`,
- Toda definedness typing guard,
- indexed Toda theorem applicability,
- stable homotopy-group model,
- stable Toda bracket,
- higher Toda bracket.

---

# 29. Next design boundary

Natural next candidate:

```text
Phase 23
Indexed Toda theorem / validity connection
```

The next layer may combine:

```text
indexed theorem fact
+
matching indexed bracket
+
required definedness
+
explicit consistency / typing side conditions
↓
indexed Toda membership
```

but only for actual literature-backed facts.

Important:

```text
is_consistent() == True
↛
theorem applies
```

```text
type-compatible
↛
Toda definedness
```

```text
structured generator identity
↛
theorem applicability
```

No general theorem prover should be introduced unless actual theorem requirements
show that the existing narrow theorem representation is insufficient.

---

# 30. Testing principle

For each new mathematical layer:

1. representation
2. structural distinction
3. validity / applicability
4. invalid-case behavior
5. integration
6. provenance if inference exists
7. representative scenario
8. termination / scope boundary
9. full regression

Structural-only Phase では存在しない inference / provenance を先取りしない。

---

# 31. Documentation policy

```text
README.md
=
current capabilities / current status

docs/design.md
=
current architecture / semantics / boundaries

docs/development_log.md
=
chronological implementation history

docs/roadmap.md
=
future capability dependency
```

Current specification は latest README / design を優先する。
