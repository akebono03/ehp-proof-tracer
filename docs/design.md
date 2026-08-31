# ehp_proof 設計メモ

この文書は Phase 21 完了時点の current architecture / semantics /
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

proof-level Toda index / iterated suspension / indeterminacy semantics は
algebra layer に埋め込まない。

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

Phase 20 は structural-expression layer の拡張であり、
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

# 10. Phase 20 design goal

Target:

```text
{a,E^t b,E^t c}_t
```

Constraints:

1. existing unindexed `TodaBracket` を壊さない。
2. bracket index を explicit に保持する。
3. suspension exponent を explicit に保持する。
4. bracket index と suspension exponent を role として分離する。
5. symbolic exponent のために general symbolic algebra を作らない。
6. stable / higher Toda を先取りしない。
7. generic engine を変更しない。

---

# 11. TodaBracket index semantics

Current shape:

```text
TodaBracket
  first: Expression
  second: Expression
  third: Expression
  index: int | ScalarSymbol | None
```

Semantics:

```text
index=None
```

は従来の unindexed bracket。

Concrete:

```text
index=1
```

Symbolic:

```text
index=ScalarSymbol("t")
```

Structural distinctions:

```text
{a,b,c}
!=
{a,b,c}_1
```

```text
{a,b,c}_1
!=
{a,b,c}_2
```

```text
{a,b,c}_t
!=
{a,b,c}_s
```

No theorem-aware index normalization.

---

# 12. IteratedSuspension semantics

Current:

```text
IteratedSuspension
  expression: Expression
  exponent: int | ScalarSymbol
```

Represents:

```text
E^n α
E^t α
```

Boundary:

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

Phase 20 では以下を導入しない:

```text
E^1 α → Eα
E^2 α → E(Eα)
E^t(E^s α) → E^(t+s) α
```

---

# 13. IndexedTodaBracketData semantics

Current:

```text
IndexedTodaBracketData
  bracket: TodaBracket
  second_base: Expression
  third_base: Expression
  suspension_exponent: int | ScalarSymbol
```

Purpose:

```text
{a,E^t b,E^t c}_t
```

について base と exponent を explicit に保持する。

これは `TodaBracket` を置き換える新しい数学的 bracket object ではない。

Existing Toda statements は引き続き `bracket` を使う。

---

# 14. Exponent / index role separation

For:

```text
{a,E^t b,E^t c}_t
```

storage roles:

```text
second.expression = b
second.exponent = t

third.expression = c
third.exponent = t

data.suspension_exponent = t

data.bracket.index = t
```

同じ `t` が出現しても role は分離される。

Therefore inconsistent data is representable:

```text
suspension_exponent=t
bracket.index=s
```

---

# 15. is_consistent()

`IndexedTodaBracketData.is_consistent()` は pure query predicate。

Checks:

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

No proof search.

No inference.

No mutation.

No constructor failure.

---

# 16. Consistency boundary

Critical:

```text
constructible
≠
consistent
```

and:

```text
consistent
≠
mathematically valid Toda theorem
```

`is_consistent()` は以下を検査しない:

- defining composition validity
- source / target spheres
- ambient homotopy group
- theorem side conditions
- stable / unstable context
- literature theorem applicability

Therefore:

```text
is_consistent() == True
↛
Toda theorem applies
```

---

# 17. Concrete / symbolic unification

Same structures support:

```text
{a,E^2 b,E^2 c}_2
```

and:

```text
{a,E^t b,E^t c}_t
```

without parallel class hierarchies.

Types:

```text
IteratedSuspension.exponent
=
int | ScalarSymbol
```

```text
IndexedTodaBracketData.suspension_exponent
=
int | ScalarSymbol
```

```text
TodaBracket.index
=
int | ScalarSymbol | None
```

---

# 18. Phase 20 representative scenario

Representative:

```text
a
b
c
t = ScalarSymbol("t")
```

Construct:

```text
second = E^t b
third  = E^t c
bracket = {a,second,third}_t
```

Data:

```text
second_base=b
third_base=c
suspension_exponent=t
```

Expected:

```text
bracket.second.exponent == t
bracket.third.exponent == t
bracket.index == t
suspension_exponent == t
is_consistent() == True
```

Independent `ScalarSymbol("t")` instances compare structurally equal.

---

# 19. Phase 20 structural boundaries

Final regression fixes:

```text
E^1 b
!=structural
E b
```

```text
E^2 b
!=structural
E(Eb)
```

```text
E^t b
!=structural
E^2 b
```

```text
{a,E^t b,E^t c}_t
!=structural
{a,E^t b,E^t c}_2
```

and:

```text
inconsistent IndexedTodaBracketData
is constructible
and
is_consistent() == False
```

---

# 20. Phase 20 completion criteria

1. explicit Toda bracket index.
2. unindexed backward compatibility.
3. concrete / symbolic bracket index.
4. first-class `IteratedSuspension`.
5. concrete / symbolic iterated exponent.
6. no implicit normalization to `Suspension`.
7. `IndexedTodaBracketData`.
8. base entries preserved explicitly.
9. suspension exponent separate from bracket index.
10. symbolic exponent in indexed data.
11. `{a,E^t b,E^t c}_t` representative form.
12. structural equality preserved.
13. `is_consistent()` predicate.
14. symbolic consistent case.
15. concrete consistent case.
16. index mismatch → `False`.
17. second mismatch → `False`.
18. third mismatch → `False`.
19. inconsistent object remains constructible.
20. no constructor validation.
21. no theorem applicability from consistency.
22. no inference from consistency.
23. no generic-engine change.
24. no stable Toda bracket.
25. no higher Toda bracket.
26. no full typing.
27. full regression PASS.

Verified:

```text
tests/test_expression.py
64 passed in 1.46s
```

```text
full suite
1098 passed in 61.30s
```

---

# 21. Phase 20 non-goals

Not implemented:

- `__post_init__` consistency enforcement
- automatic repair of indexed data
- `Suspension` / `IteratedSuspension` auto conversion
- symbolic exponent addition / simplification
- `E^t` theorem reasoning
- source / target checking for `E^t`
- source / target checking for Toda entries
- general theorem quantification
- stable homotopy-group model
- stable Toda bracket
- higher Toda bracket
- arbitrary bracket arity
- general set-valued algebra

---


# 22. Phase 21 typed homotopy-element semantics

Phase 21 introduces minimal source / target context without introducing a universal
homotopy type system.

Current `HomotopyElement` shape:

```text
HomotopyElement
  name: str
  dimension: int
  source: int | None
  target: int | None
```

Example:

```text
α : S^5 → S^3
```

is represented by:

```text
source=5
target=3
```

`source` / `target` participate in structural equality.

Therefore:

```text
HomotopyElement(
  name="α",
  dimension=3,
  source=5,
  target=3,
)
!=structural
HomotopyElement(
  name="α",
  dimension=3,
  source=6,
  target=3,
)
```

and:

```text
typed α
!=structural
untyped α
```

`None` is not a wildcard. It means that the corresponding concrete typing
information is not stored.

---

# 23. Suspension source / target semantics

For:

```text
α : S^m → S^n
```

ordinary suspension exposes derived typing:

```text
Eα : S^(m+1) → S^(n+1)
```

Current `Suspension` does not store redundant source / target fields.

Instead:

```text
Suspension.source
Suspension.target
```

are derived properties.

Known information shifts by `+1`.

Unknown information remains `None`.

Nested ordinary suspension repeats this shift.

No constructor validation is introduced.

---

# 24. IteratedSuspension typing semantics

For concrete non-negative:

```text
r: int
```

Phase 21 derives:

```text
E^r α : S^(m+r) → S^(n+r)
```

when the underlying concrete typing is available.

For:

```text
ScalarSymbol("t")
```

Phase 21 does not create symbolic dimension expressions:

```text
m+t
n+t
```

Therefore concrete typing query returns:

```text
source=None
target=None
```

for symbolic exponent.

Negative exponents remain structurally constructible but do not produce concrete
source / target typing.

This preserves:

```text
constructible
≠
validated suspension semantics
```

No iterated-suspension normalization is introduced.

---

# 25. Composition compatibility semantics

Current:

```text
Composition(
  left=α,
  right=β,
)
```

represents:

```text
α∘β
```

For:

```text
α : S^m → S^n
β : S^p → S^m
```

the compatibility condition is:

```text
α.source == β.target
```

Current pure query:

```text
Composition.is_type_compatible() -> bool
```

Supported typed operand structures are currently:

```text
HomotopyElement
Suspension
IteratedSuspension
```

The predicate returns `True` only when the required boundary dimensions are both
concrete and equal.

Current `False` intentionally combines:

```text
known mismatch
unknown typing
unsupported typing
```

No three-valued `TypeCompatibility` enum exists yet.

Critical:

```text
Composition(...)
```

remains constructible even when incompatible.

No `__post_init__` rejection.

No inference.

No ZERO conclusion.

---

# 26. Toda entry compatibility semantics

For:

```text
{a,b,c}
```

the displayed defining compositions are:

```text
a∘b
b∘c
```

Current pure query:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

constructs those two `Composition` structures and reuses:

```text
Composition.is_type_compatible()
```

Both must return `True`.

The bracket index does not alter this displayed-entry compatibility predicate.

Thus the same compatibility query can be applied to:

```text
{a,b,c}
{a,b,c}_r
```

without treating the index as a composition-boundary dimension.

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

Existing Toda definedness inference remains unchanged.

---

# 27. Phase 21 representative scenario

Representative dependency:

```text
typed HomotopyElement
↓
ordinary Suspension typing
↓
concrete IteratedSuspension typing
↓
Composition compatibility
↓
Toda entry compatibility
```

The scenario confirms a typed chain such as:

```text
a : S^5 → S^3
b : S^7 → S^5
c : S^9 → S^7
```

satisfies:

```text
a∘b compatible
b∘c compatible
```

and therefore:

```text
{a,b,c}
```

has compatible displayed defining compositions.

Separately, inference regression fixes:

```text
type compatibility
↛
ZERO
↛
Toda definedness
```

---

# 28. Phase 21 completion criteria

1. `HomotopyElement.source`.
2. `HomotopyElement.target`.
3. optional source / target preserve legacy constructor usage.
4. source / target participate in structural equality.
5. typed / untyped structural distinction.
6. ordinary Suspension shifts known source by `+1`.
7. ordinary Suspension shifts known target by `+1`.
8. unknown Suspension typing remains unknown.
9. nested ordinary Suspension repeats the shift.
10. concrete non-negative IteratedSuspension shifts by exponent.
11. symbolic IteratedSuspension does not create symbolic sphere dimensions.
12. negative IteratedSuspension does not produce concrete typing.
13. `Composition.is_type_compatible()`.
14. compatibility checks `left.source == right.target`.
15. known matching boundary returns `True`.
16. known mismatch returns `False`.
17. unknown typing returns `False`.
18. incompatible Composition remains constructible.
19. `TodaBracket.are_defining_compositions_type_compatible()`.
20. both displayed Toda compositions must be compatible.
21. first mismatch returns `False`.
22. second mismatch returns `False`.
23. unknown Toda typing returns `False`.
24. indexed bracket can use the same compatibility query.
25. compatibility does not imply ZERO.
26. compatibility does not imply Toda definedness.
27. no constructor-level type validation.
28. no three-valued compatibility model.
29. no symbolic dimension solver.
30. no ambient homotopy-group validation.
31. no stem / stable-context model.
32. no generic-engine change.
33. full regression PASS.

Verified:

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

# 29. Phase 21 non-goals

Not implemented:

- constructor rejection for source / target mismatch
- universal `Expression` typing protocol
- `Composition.source`
- `Composition.target`
- three-valued compatibility result
- symbolic sphere-dimension arithmetic
- negative-suspension semantics
- ambient homotopy-group validation
- stem validation
- stable / unstable context
- automatic typing of `eta()`, `nu()`, `sigma()`
- Toda definedness typing guard
- indexed Toda theorem applicability from typing
- structured generator notation
- stable homotopy-group model
- stable Toda bracket
- higher Toda bracket

---

# 30. Phase 22 boundary

Natural next candidate:

```text
Phase 22
structured generator representation
```

Purpose:

```text
ν
ν′
decorated generator families
η_n
μ_n
ι_n
```

を display-only text ではなく、actual literature / table input に必要な範囲で
structural に区別すること。

Potential fields:

```text
family
index
decoration
source
target
stable_or_unstable
```

ただし Phase 22 でも actual source need のない field は先取りしない。

Current typed `HomotopyElement` API を不必要に壊さず、必要なら additive structure として
導入する。

Indexed Toda theorem applicability / theorem representation / stable homotopy are
later dependency layers.

---

# 31. Testing principle

For each new mathematical layer:

1. representation
2. structural distinction
3. validity / applicability
4. invalid-case rejection
5. integration
6. provenance if inference exists
7. representative scenario
8. termination / scope boundary
9. full regression

Structural-only Phase では存在しない inference / provenance を先取りしない。

---

# 32. Documentation policy

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
