# ehp_proof 設計メモ

この文書は Phase 23 完了時点の current architecture / semantics /
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
indeterminacy semantics / theorem applicability は algebra layer に埋め込まない。

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
- general theorem quantification

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

```text
TodaBracket(...,index=1)
!=structural
TodaBracket(...,index=None)
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

Phase 23 でも generic inference engine は変更しない。

Domain-specific validity は `InferenceRule.match_guard` など domain rule 側に置く。

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

この gap が Phase 20 の actual requirement となった。

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

Current `HomotopyElement`:

```text
HomotopyElement
  name: str
  dimension: int
  source: int | None
  target: int | None
  generator: GeneratorSymbol | None
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

# 16. Phase 22 generator design

`GeneratorSymbol` は generator identity / notation の最小構造。

```text
GeneratorSymbol
  family: str
  index: int | None
  decoration: str | None
```

`GeneratorSymbol` は `Expression` ではない。

Examples:

```text
ν
ν′
barν
η₃
μ₃
ι₇
```

All fields participate in ordinary dataclass structural equality.

```text
η₃ != η₄
η₃ != μ₃
ν != ν′
ν′ != barν
```

`index=None` と `decoration=None` は wildcard ではない。

---

# 17. HomotopyElement generator connection

Current shape:

```text
HomotopyElement
  name
  dimension
  source
  target
  generator
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

Critical:

```text
generator notation
↛
automatic typing
```

Existing helpers:

```text
eta()
nu()
sigma()
```

は backward compatible のため legacy form のまま。

---

# 18. Suspension / generator role separation

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

The operation `E` is not folded into generator identity.

Thus:

```text
generator identity
!=
homotopy operation
```

---

# 19. Phase 23 design goal

Phase 23 の目的は、indexed Toda theorem fact を structural representation
から実際の membership inference へ接続すること。

対象は2種類に分ける。

```text
A. canonical indexed form
   {a,E^t b,E^t c}_t

B. specific literature form
   ε₃ ∈ {η₃,Eν′,ν₇}_1
```

この2つを無理に同じ validity representation に統合しない。

---

# 20. Indexed theorem fact semantics

既存:

```text
TodaBracketMembershipTheoremStatement
```

を再利用する。

新しい indexed theorem statement hierarchy は作らない。

Statement が保持する:

```text
element
bracket
source
note
```

`bracket` は `TodaBracket` なので:

```text
index
GeneratorSymbol
Suspension / IteratedSuspension
```

を含む bracket 全体を lossless に保持できる。

---

# 21. Bracket index match

Theorem matching は whole-bracket structural equality を使う。

したがって:

```text
{a,b,c}_1
==
{a,b,c}_1
```

は match 可能。

一方:

```text
{a,b,c}_1
!=
{a,b,c}_2
```

```text
{a,b,c}_1
!=
{a,b,c}
```

は match しない。

```text
index=None
```

は wildcard ではない。

Index-only manual guard は追加しない。

---

# 22. Generator structure match

`HomotopyElement.generator` が structural equality に参加するため、
theorem bracket と definedness bracket の generator identity も
whole-bracket equality に含まれる。

Difference examples:

```text
family mismatch
index mismatch
decoration mismatch
```

Same display name でも generator field が異なれば structural mismatch。

Generator-specific manual theorem matcher は追加しない。

---

# 23. Definedness connection

Narrow theorem bridge:

```text
matching theorem fact
+
matching TodaBracketDefinedStatement
↓
TodaBracketMembershipStatement
```

Boundary:

```text
theorem fact
↛
membership
```

```text
definedness
↛
membership
```

Definedness は independent premise。

Phase 23 は typing compatibility から definedness を生成しない。

---

# 24. Canonical indexed structural consistency guard

Phase 23 で追加:

```text
indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data
)
```

この rule は canonical indexed form:

```text
{a,E^t b,E^t c}_t
```

を対象とする。

Guard の first condition:

```text
indexed_data.is_consistent()
```

This checks:

```text
bracket.second
==
IteratedSuspension(second_base,t)

bracket.third
==
IteratedSuspension(third_base,t)

bracket.index
==
t
```

Critical:

```text
is_consistent() == True
↛
theorem applies
```

```text
is_consistent() == False
→
canonical guarded bridge reject
```

---

# 25. Canonical indexed typing guard

Guard の second condition:

```text
indexed_data.bracket
.are_defining_compositions_type_compatible()
```

つまり displayed defining compositions:

```text
first ∘ second
second ∘ third
```

の type compatibility を確認する。

Current policy:

```text
known mismatch
→ reject

unknown typing
→ reject
```

ただし:

```text
type-compatible
↛
ZERO
↛
definedness
```

なので `TodaBracketDefinedStatement` は別 premise のまま。

---

# 26. Canonical guarded bridge

Canonical indexed rule の全体は:

```text
matching theorem fact
+
matching definedness
+
indexed structural consistency
+
confirmed entry typing compatibility
↓
indexed Toda membership
```

Theorem / definedness / `indexed_data.bracket` は structural に一致する必要がある。

Theorem source / note は membership に伝播する。

---

# 27. Actual ε₃ literature scenario

Actual notation:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Current storage:

```text
ε₃
=
GeneratorSymbol(family="ε",index=3)

η₃
=
GeneratorSymbol(family="η",index=3)

ν′
=
GeneratorSymbol(family="ν",decoration="′")

Eν′
=
Suspension(ν′)

ν₇
=
GeneratorSymbol(family="ν",index=7)

_1
=
TodaBracket.index
```

This is lossless.

---

# 28. Why actual ε₃ is not canonical IndexedTodaBracketData

`IndexedTodaBracketData` は:

```text
second = IteratedSuspension(base,t)
third  = IteratedSuspension(base,t)
```

を要求する。

しかし actual ε₃ bracket は:

```text
second = Suspension(ν′)
third  = ν₇
index  = 1
```

である。

Current structural semantics:

```text
Suspension(ν′)
!=
IteratedSuspension(ν′,1)
```

さらに:

```text
ν₇
→
ν₆
```

の inverse generator lookup は存在しない。

したがって actual ε₃ theorem を canonical data に無理に変換しない。

---

# 29. Narrow literature bridge responsibility

Actual ε₃ theorem は既存 narrow bridge:

```text
specific theorem fact
+
exactly matching definedness
↓
membership
```

を使う。

これは validity guard を省略した一般 theorem prover という意味ではない。

Specific literature theorem fact 自体が concrete bracket identity を持つため、
canonical symbolic-form consistency model を追加で課さない。

責務分離:

```text
canonical {a,E^t b,E^t c}_t
→ indexed guarded bridge
```

```text
specific ε₃ ∈ {η₃,Eν′,ν₇}_1
→ narrow literature bridge
```

---

# 30. Provenance semantics

Derived indexed membership direct premises:

```text
theorem_step
defined_step
```

Unrelated facts are not included.

Theorem:

```text
source
note
```

は derived membership に伝播する。

`IndexedTodaBracketData.is_consistent()` と typing compatibility は
proof-step premise ではなく rule applicability guard。

Current Phase 23 では consistency / typing の dedicated proof statement は
導入しない。

---

# 31. Indexed / unindexed boundary

Indexed conclusion:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

から unindexed:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

を自動生成しない。

```text
index=1
!=structural
index=None
```

Phase 19 の unindexed projection は current actual representation では不要。

---

# 32. Phase 23 completion criteria

1. indexed theorem fact を lossless に保持。
2. existing theorem statement を再利用。
3. bracket index match。
4. wrong index reject。
5. unindexed bracket reject。
6. generator family match。
7. wrong generator family reject。
8. generator decoration match。
9. wrong decoration reject。
10. generator index match。
11. wrong generator index reject。
12. theorem alone does not imply membership。
13. definedness alone does not imply membership。
14. theorem + matching definedness → membership。
15. canonical indexed consistency guard。
16. index / exponent inconsistency reject。
17. entry/base inconsistency reject。
18. canonical typing guard。
19. type mismatch reject。
20. unknown typing reject。
21. consistency + typing + theorem + definedness → membership。
22. canonical representative bridge。
23. source / note provenance。
24. direct premises fixed。
25. unrelated fact excluded from provenance。
26. actual ε₃ theorem fact lossless。
27. actual ε₃ narrow bridge。
28. actual ε₃ not forced into canonical indexed data。
29. no `Suspension` / `IteratedSuspension(...,1)` normalization。
30. no inverse generator lookup。
31. indexed membership does not collapse to unindexed membership。
32. generic inference engine unchanged。
33. full regression PASS。

Verified:

```text
tests/test_toda_rules.py
66 passed in 1.01s
```

```text
full suite
1175 passed in 22.96s
```

---

# 33. Phase 23 non-goals

Not implemented:

- general theorem quantification,
- theorem variable substitution system beyond current inference patterns,
- theorem database / repository,
- knowledge-table loader,
- generator table lookup,
- automatic generator typing,
- name / generator validation,
- ambient homotopy-group validation,
- stem validation,
- stable / unstable generator classification,
- general indexed Toda definedness theorem system,
- `Suspension` / `IteratedSuspension` normalization,
- inverse generator lookup,
- stable homotopy-group model,
- stable Toda bracket,
- higher Toda bracket.

---

# 34. Next design boundary

Natural next candidate:

```text
Phase 24
Theorem fact / knowledge-table integration
```

Purpose:

```text
literature-backed theorem / known fact
↓
structured storage
↓
Statement / Relation
↓
existing InferenceRule
↓
proof graph
```

まずは current narrow theorem statement / `LiteratureReference` を再利用し、
universal theorem prover を先に作らない。

Potential later dependency:

```text
theorem / knowledge table
↓
generator typing / ambient-group facts
↓
stable homotopy representation
↓
stable Toda bracket
```

---

# 35. Testing principle

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

# 36. Documentation policy

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
