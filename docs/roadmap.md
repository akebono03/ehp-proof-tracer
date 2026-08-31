# EHP Proof Tracer Roadmap

## 1. この文書の目的

この文書は、EHP Proof Tracer の将来拡張に関する長期的な設計方針を記録する。

`README.md` は current capabilities / current status、
`docs/design.md` は current architecture / semantics / boundaries、
`docs/development_log.md` は chronological implementation history を扱う。

この `docs/roadmap.md` は、まだ未実装の機能を含む将来構想と、
それらの依存関係・実装優先順位を整理するための文書とする。

この文書に記載された項目は、記載されているだけでは実装済みを意味しない。
各機能は必要な Phase において個別に仕様化し、
既存 API と generic inference engine を不必要に壊さない最小変更で導入する。

---

# 2. Phase 21 完了時点の実装基盤

Implemented foundations:

```text
Abelian group calculation
EHP reasoning
ORDER
Suspension
Freudenthal
Composition
Generalized Hopf invariant
Additive expressions
Homomorphism reasoning
Set / subgroup reasoning
Coset / modulo reasoning
Symbolic scalar constraints
Indeterminacy
Toda bracket minimum representation
Toda bracket membership
Toda bracket definedness
Toda membership theorem bridge
Literature-backed Toda membership
Toda bracket index
IteratedSuspension
IndexedTodaBracketData
symbolic iterated-suspension exponent
symbolic Toda index
indexed Toda structural consistency predicate
typed homotopy-element source / target context
typed HomotopyElement structural equality
Suspension source / target shift
concrete IteratedSuspension source / target shift
Composition type compatibility predicate
Toda entry composition compatibility predicate
```

Current expression structures:

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

Separate structures:

```text
MapSymbol
ScalarSymbol
TodaBracket
IndexedTodaBracketData
```

Current representative indexed Toda form:

```text
{a,E^t b,E^t c}_t
```

---

# 3. 基本設計原則

## 3.1 actual mathematical need first

```text
actual mathematical need
↓
minimal representation
↓
domain rule if needed
↓
existing generic engine
```

完全な theorem prover / symbolic algebra / higher Toda system を先に実装しない。

## 3.2 structural syntax と theorem semantics を分離する

```text
representable
≠
mathematically valid
```

```text
structurally consistent
≠
theorem applicable
```

Phase 20 の `is_consistent()` は structural consistency のみ扱う。

## 3.3 不定性を消さない

```text
membership
≠
exact value
```

```text
coset information
≠
chosen representative
```

```text
sign information
≠
chosen sign
```

## 3.4 candidate enumeration を避ける

Infinite / large candidate generation を避け、
constraint / membership / theorem fact を first-class knowledge として保持する。

## 3.5 active inference scope を明示する

数学的に正しい rule でも無制限 generation を行わない。

## 3.6 generic engine を domain semantics で汚さない

Domain-specific validity は statement / rule / guard 側に置く。

---

# 4. Completed Phase chain

```text
Phase 12  Additive expressions
Phase 13  Homomorphism reasoning
Phase 14  Set / subgroup reasoning
Phase 15  Coset / modulo reasoning
Phase 16  Symbolic scalar constraints
Phase 17  Indeterminacy
Phase 18  Toda bracket minimum representation
Phase 19  Toda bracket membership / first theorem bridge
Phase 20  Indexed unstable Toda notation
```

All completed.

---

# 5. Phase 18 完了：Toda bracket minimum representation

Implemented:

```text
TodaBracket(a,b,c)
TodaBracketDefinedStatement
TodaBracketMembershipStatement
```

Bridge:

```text
a∘b=0
b∘c=0
↓
ZERO
↓
{a,b,c} defined
```

Safety:

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

# 6. Phase 19 完了：first Toda theorem bridge

Actual source notation:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Implemented:

```text
TodaBracketMembershipTheoremStatement
```

Bridge:

```text
matching theorem fact
+
matching definedness
↓
membership
```

Phase 19 では `_1` をまだ lossless に保持できなかった。

That gap became the immediate Phase 20 requirement.

---

# 7. Phase 20 完了：Indexed Unstable Toda Notation

## 7.1 Toda bracket index

Implemented:

```text
TodaBracket.index
=
int | ScalarSymbol | None
```

Examples:

```text
{a,b,c}
{a,b,c}_1
{a,b,c}_t
```

## 7.2 IteratedSuspension

Implemented:

```text
IteratedSuspension(
  expression=α,
  exponent=n_or_t,
)
```

with:

```text
exponent: int | ScalarSymbol
```

Examples:

```text
E^2 α
E^t α
```

No normalization to nested ordinary `Suspension`.

## 7.3 IndexedTodaBracketData

Implemented fields:

```text
bracket
second_base
third_base
suspension_exponent
```

with:

```text
suspension_exponent: int | ScalarSymbol
```

## 7.4 target notation

Implemented structural representation:

```text
{a,E^t b,E^t c}_t
```

The roles remain separate:

```text
suspension exponent
bracket index
```

even when both are written as `t`.

## 7.5 consistency

Implemented:

```text
IndexedTodaBracketData.is_consistent()
```

Checks:

```text
second = E^t(second_base)
third  = E^t(third_base)
index  = t
```

for the stored exponent.

Both symbolic and concrete forms are supported.

## 7.6 API boundary

Inconsistent data remains constructible.

```text
is_consistent() == False
```

reports the mismatch.

No constructor validation.

No theorem inference.

## 7.7 verified status

```text
tests/test_expression.py
64 passed in 1.46s
```

```text
full suite
1098 passed in 61.30s
```

Generic inference engine unchanged.

---

# 8. Phase 21 完了：Typed Homotopy Elements / Source-Target Context

## 8.1 motivation

Phase 20 で indexed Toda notation 自体は lossless に保持可能になった。

Phase 21 は actual composition / Toda validity に必要な最小 source / target context
を導入した。

Universal type system は導入していない。

## 8.2 typed HomotopyElement

Implemented:

```text
HomotopyElement.source
HomotopyElement.target
```

Types:

```text
int | None
```

Example:

```text
α : S^5 → S^3
```

Typed fields participate in structural equality.

```text
typed α
!=structural
untyped α
```

## 8.3 Suspension typing

Implemented:

```text
α : S^m → S^n
↓
Eα : S^(m+1) → S^(n+1)
```

Unknown dimensions remain unknown.

Nested ordinary Suspension repeats the shift.

## 8.4 IteratedSuspension typing

Concrete non-negative exponent:

```text
E^r α : S^(m+r) → S^(n+r)
```

Symbolic:

```text
E^t α
```

does not trigger general symbolic dimension arithmetic.

Negative exponent does not produce concrete typing.

## 8.5 Composition compatibility

Implemented:

```text
Composition.is_type_compatible()
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

Critical boundary:

```text
constructible
≠
type-compatible
```

Current boolean `False` includes both:

```text
known mismatch
unknown typing
```

No three-valued compatibility model yet.

## 8.6 Toda entry compatibility

Implemented:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

Checks:

```text
a∘b
b∘c
```

using `Composition.is_type_compatible()`.

Both must be confirmed compatible.

Important:

```text
type compatibility
≠
ZERO
≠
Toda definedness
```

Existing Toda inference rules are unchanged.

## 8.7 representative / regression

Representative chain:

```text
typed HomotopyElement
↓
Suspension shift
↓
concrete IteratedSuspension shift
↓
Composition compatibility
↓
Toda entry compatibility
```

Final regression fixes:

```text
typed != untyped
symbolic E^t → no concrete dimensions
negative exponent → no concrete dimensions
known mismatch → False
unknown typing → False
mismatch remains constructible
first Toda mismatch → False
second Toda mismatch → False
indexed / unindexed structural distinction
compatibility ↛ ZERO
compatibility ↛ Toda definedness
```

## 8.8 verified status

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

Generic inference engine unchanged.

---

# 9. Phase 22 candidate：Structured Generator Representation

Toda literature uses distinctions such as:

```text
ν
ν′
arν
η_n
μ_n
ι_n
```

Potential future structure:

```text
GeneratorSymbol
  family
  index
  decoration
  source
  target
  stable_or_unstable
```

Important:

```text
ν
ν′
arν
```

must not collapse as display variants.

Operations such as `E` remain structural operation nodes, not generator-name text.

Introduce only when actual tables / literature input require it.

---

# 10. Indexed Toda theorem connection

Phase 20 adds representation / consistency only.

Future actual theorem bridge may take the form:

```text
indexed theorem fact
+
indexed bracket definedness
+
required consistency / typing side conditions
↓
indexed Toda membership
```

This must be based on an actual literature fact.

Do not derive membership merely from:

```text
is_consistent() == True
```

---

# 11. Stable Homotopy Groups

Future stable context:

```text
α ∈ π_k^S
```

must remain distinct from unstable:

```text
α ∈ π_m(S^n)
```

Bridge using:

```text
Suspension
Freudenthal
stabilization theorem
```

not notation-only conversion.

---

# 12. Stable Toda Bracket

Stable notation:

```text
<a,b,c>
```

must remain distinct from unstable:

```text
{a,b,c}
```

Possible future statements:

```text
x ∈ <a,b,c>
```

Stable degree / stem convention must be fixed before theorem checking.

---

# 13. Higher Toda Brackets

Higher / variable-arity brackets remain deferred until concrete literature
examples require them.

Do not infer bracket order solely from entry count.

Distinguish:

```text
number of entries
Toda order
bracket index
stem
stable / unstable context
```

---

# 14. Theorem Representation

Long-term theorem data:

```text
name
source
variables
types
quantification
assumptions
side conditions
conclusion
```

Current `InferenceRule` and narrow theorem statements should be reused where possible.

Do not introduce a general first-order logic engine before actual need.

---

# 15. Knowledge Tables

Goal:

```text
table / repository
↓
known fact
↓
Statement / Relation
↓
InferenceRule
↓
derived conclusion
```

Possible inputs:

```text
π_n(S^k)=G
π_k^S=G
ord(α)=n
α∘β=γ
H(α)=β
Toda membership facts
```

Literature provenance must remain attached.

---

# 16. ORDER / Divisibility / Annihilator

Current:

```text
ord(a)=n
→
na=0
```

Future need:

```text
n | m
+
ord(a)=n
→
ma=0
```

Do not enumerate all multiples.

Potential goal-directed / divisibility-statement approach.

---

# 17. Recommended future order

```text
Phase 21
Typed homotopy elements / source-target context
        ↓
Phase 22 candidate
Structured generator representation
        ↓
Indexed Toda theorem / validity connection
        ↓
Theorem representation / knowledge-table integration
        ↓
Stable homotopy representation
        ↓
Stable Toda bracket
  <a,b,c>
        ↓
Higher Toda bracket
  only when actual examples require it
```

Phase 21 以降の numbering は provisional。

Actual mathematical need に応じて再配置可能。

---

# 18. 実装状況

| 項目 | 状態 | 備考 |
|---|---|---|
| Additive expression `α+β` | IMPLEMENTED | Phase 12 |
| additive inverse `-α` | IMPLEMENTED | Phase 12 |
| symbolic coefficient `kβ` | IMPLEMENTED | Phase 16 |
| homomorphism reasoning | IMPLEMENTED | Phase 13 |
| membership `α∈A` | IMPLEMENTED | Phase 14 |
| subset `A⊆B` | IMPLEMENTED | Phase 14 |
| coset `α+A` | IMPLEMENTED | Phase 15 |
| modulo `α≡β mod A` | IMPLEMENTED | Phase 15 |
| scalar parity / congruence | IMPLEMENTED | Phase 16 |
| coefficient indeterminacy | IMPLEMENTED | Phase 17 |
| sign indeterminacy | IMPLEMENTED | Phase 17 |
| coset membership indeterminacy | IMPLEMENTED | Phase 17 |
| Toda bracket `{a,b,c}` | IMPLEMENTED | Phase 18 |
| Toda bracket membership | IMPLEMENTED | Phase 18 |
| Toda definedness | IMPLEMENTED | Phase 18 |
| Toda theorem + definedness → membership | IMPLEMENTED | Phase 19 |
| literature-backed ε₃ Toda bridge | IMPLEMENTED | Phase 19 |
| Toda bracket concrete index | IMPLEMENTED | Phase 20 |
| Toda bracket symbolic index | IMPLEMENTED | Phase 20 |
| `IteratedSuspension(α,n)` | IMPLEMENTED | Phase 20 |
| `IteratedSuspension(α,t)` | IMPLEMENTED | Phase 20 |
| `IndexedTodaBracketData` | IMPLEMENTED | Phase 20 |
| `{a,E^t b,E^t c}_t` structural form | IMPLEMENTED | Phase 20 |
| indexed Toda consistency predicate | IMPLEMENTED | Phase 20 |
| typed source / target | IMPLEMENTED | Phase 21 |
| Suspension source / target shift | IMPLEMENTED | Phase 21 |
| concrete IteratedSuspension source / target shift | IMPLEMENTED | Phase 21 |
| Composition type compatibility | IMPLEMENTED | Phase 21 |
| Toda entry composition compatibility | IMPLEMENTED | Phase 21 |
| structured generator notation | NEXT CANDIDATE | Phase 22 |
| ambient homotopy group validation | PLANNED | later typing layer |
| indexed Toda theorem bridge | PLANNED | actual theorem need |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| theorem representation | PLANNED | assumptions / conclusion / source |
| knowledge-table integration | PLANNED | facts with provenance |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer required |
| stable degree / stem checking | PLANNED | convention to be fixed |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 19. Phase 20 completion boundary

Implemented:

```text
TodaBracket.index
IndexedTodaBracketData
IteratedSuspension
IndexedTodaBracketData.is_consistent()
```

Types:

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

Representative:

```text
{a,E^t b,E^t c}_t
```

Boundary:

```text
IteratedSuspension
!=
ordinary Suspension normalization
```

```text
suspension exponent role
!=
bracket index role
```

```text
inconsistent data
remains constructible
```

```text
is_consistent()
!=
theorem applicability
```

```text
is_consistent()
!=
inference
```

No stable / higher Toda layer.

No full typing.

Generic inference engine unchanged.

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


# 20. Phase 21 completion boundary

Implemented:

```text
HomotopyElement.source
HomotopyElement.target
typed structural equality
Suspension source / target shift
concrete IteratedSuspension source / target shift
Composition.is_type_compatible()
TodaBracket.are_defining_compositions_type_compatible()
```

Boundaries:

```text
typed
!=
untyped
```

```text
constructible
!=
type-compatible
```

```text
symbolic E^t
!=
symbolic dimension arithmetic
```

```text
type compatibility
!=
ZERO
```

```text
type compatibility
!=
Toda definedness
```

No constructor type validation.

No three-valued compatibility model.

No Composition source / target derivation.

No ambient homotopy-group / stem / stable-context typing.

No Toda definedness typing guard.

Generic inference engine unchanged.

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

# 21. Phase 22 candidate boundary

Natural next candidate:

```text
Phase 22
Structured Generator Representation
```

Target actual need:

```text
ν
ν′
decorated generator families
η_n
μ_n
ι_n
```

Potential structure:

```text
family
index
decoration
source
target
stable_or_unstable
```

Do not introduce every field immediately.

Use actual tables / literature notation to determine the minimum structure.

Current `HomotopyElement` should remain backward compatible unless an actual
generator representation requirement proves otherwise.

Indexed Toda theorem applicability, theorem representation, stable homotopy groups,
stable Toda brackets, and higher Toda brackets remain later layers.

---

# 22. Testing Principle

新しい mathematical layer を追加するときは:

1. representation test
2. structural distinction test
3. validity / applicability test
4. invalid-case rejection
5. integration
6. provenance if inference is involved
7. representative mathematical scenario
8. termination / inference-scope boundary
9. full regression

Actual scope に存在しない theorem / inference のテストを先取りしない。

---

# 23. Documentation Policy

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

roadmap の項目が実装された場合は、その Phase 完了時に状態を更新する。

---

# 24. 長期目標

最終的には:

```text
known unstable homotopy groups
+
known stable homotopy groups
+
generator / map tables
+
quantified theorems
+
EHP exactness
+
ORDER
+
Suspension / stabilization
+
composition
+
Hopf invariant
+
additive reasoning
+
subgroup / modulo reasoning
+
symbolic scalar constraints
+
indeterminacy
+
unstable Toda brackets
+
indexed unstable Toda notation
+
stable Toda brackets
↓
new homotopy-theoretic conclusions
```

を同一 proof graph 上で扱う。

その際:

```text
exact value
partial information
sign uncertainty
coefficient uncertainty
coset uncertainty
Toda-bracket membership
indexed Toda structure
stable Toda-bracket membership
```

を provenance 付き knowledge として保持する。
