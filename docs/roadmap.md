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

# 2. Phase 20 完了時点の実装基盤

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

# 8. Phase 21 candidate：Typed Homotopy Elements / Source-Target Context

## 8.1 motivation

Phase 20 で indexed Toda notation 自体は保持可能になった。

次の actual mathematical validity check では:

```text
composition compatibility
Toda defining conditions
suspension dimension shift
ambient homotopy group
```

が必要になる。

Natural next candidate:

```text
Phase 21
typed homotopy elements / source-target context
```

## 8.2 minimal target

Actual theorem need に必要な情報だけ導入する。

Candidates:

```text
source sphere
target sphere
ambient homotopy group
stem
stable / unstable context
```

最初から universal type system を作らない。

## 8.3 composition compatibility

Future target:

```text
α : S^m → S^n
β : S^p → S^m
```

then:

```text
α∘β
```

is type-compatible.

Mismatch should become explicit non-applicability / validity failure.

## 8.4 suspension typing

Future:

```text
α : S^m → S^n
↓
Eα : S^(m+1) → S^(n+1)
```

and for concrete iterated suspension:

```text
E^r α : S^(m+r) → S^(n+r)
```

Symbolic `t` should not trigger a general symbolic dimension solver unless
an actual theorem requires it.

## 8.5 Toda compatibility

Future Toda validity may require both:

```text
a∘b
b∘c
```

to be type-correct before zero-composition facts are accepted as defining
conditions.

Phase 21 should not alter unrelated Toda semantics.

---

# 9. Structured Generator Representation

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
Phase 21 candidate
Typed homotopy elements / source-target context
        ↓
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
| typed source / target | NEXT CANDIDATE | Phase 21 |
| ambient homotopy group validation | PLANNED | typing layer |
| structured generator notation | PLANNED | actual tables / literature |
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

# 20. Testing Principle

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

# 21. Documentation Policy

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

# 22. 長期目標

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
