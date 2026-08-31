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

# 2. Phase 22 完了時点の実装基盤

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
GeneratorSymbol
generator family / index / decoration structure
structured generator equality
ν / ν′ / decorated ν distinction
η_n / μ_n / ι_n indexed generator representation
HomotopyElement.generator
structured generator + source / target coexistence
legacy HomotopyElement backward compatibility
representative {η₃,Eν′,ν₇}_1 generator structure
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
GeneratorSymbol
TodaBracket
IndexedTodaBracketData
```

Current representative indexed Toda form:

```text
{a,E^t b,E^t c}_t
```

Current representative structured-generator literature form:

```text
{η₃,Eν′,ν₇}_1
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

```text
structured generator identity
≠
typing theorem
```

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
Phase 21  Typed homotopy elements / source-target context
Phase 22  Structured generator representation
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

Implemented:

```text
TodaBracket.index
IteratedSuspension
IndexedTodaBracketData
IndexedTodaBracketData.is_consistent()
```

Types:

```text
TodaBracket.index
=
int | ScalarSymbol | None
```

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

Target structural representation:

```text
{a,E^t b,E^t c}_t
```

Critical:

```text
suspension exponent
!=
bracket index
```

```text
is_consistent()
!=
theorem applicability
```

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

# 8. Phase 21 完了：Typed Homotopy Elements / Source-Target Context

Implemented:

```text
HomotopyElement.source
HomotopyElement.target
Suspension source / target shift
concrete IteratedSuspension source / target shift
Composition.is_type_compatible()
TodaBracket.are_defining_compositions_type_compatible()
```

Critical boundaries:

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
!=
Toda definedness
```

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

# 9. Phase 22 完了：Structured Generator Representation

Phase 22 adds the minimum structure needed to preserve generator identity from
actual literature and tables.

Implemented:

```text
GeneratorSymbol
  family
  index
  decoration
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

Structural distinctions include:

```text
ν != ν′
ν′ != barν
η₃ != η₄
η₃ != μ₃
ι₇ != ι₈
```

`GeneratorSymbol` is separate from `Expression`.

`HomotopyElement` now optionally stores:

```text
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

Important:

```text
generator notation
↛
automatic source / target typing
```

Existing:

```text
eta()
nu()
sigma()
```

remain backward compatible.

Representative literature structure:

```text
{η₃,Eν′,ν₇}_1
```

with:

```text
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
```

No theorem applicability follows merely from structured representation.

Verified:

```text
tests/test_expression.py
118 passed in 0.44s
```

```text
full suite
1153 passed in 24.83s
```

Generic inference engine unchanged.

---

# 10. Phase 23 candidate：Indexed Toda theorem / validity connection

Natural next dependency:

```text
structured indexed Toda notation
+
typed homotopy entries
+
structured generator identity
+
actual literature-backed theorem fact
↓
narrow theorem applicability / membership bridge
```

Potential rule shape:

```text
indexed theorem fact
+
matching indexed bracket definedness
+
matching generator structure
+
required explicit typing / consistency side conditions
↓
indexed Toda membership
```

Important:

```text
IndexedTodaBracketData.is_consistent() == True
↛
theorem applies
```

```text
TodaBracket.are_defining_compositions_type_compatible() == True
↛
Toda bracket defined
```

```text
structured generator match
↛
theorem applies
```

The rule must be based on an actual literature fact and explicit assumptions.

Do not introduce a universal theorem prover.

---

# 11. Theorem Representation

Long-term theorem data may need:

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

Only generalize theorem representation when actual theorem requirements prove that
the current narrow bridge is insufficient.

---

# 12. Knowledge Tables

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
generator identity / typing facts
```

Literature provenance must remain attached.

Potential later use:

```text
GeneratorSymbol
+
generator table
↓
explicit source / target / ambient group fact
```

but Phase 22 deliberately does not perform this lookup automatically.

---

# 13. Stable Homotopy Groups

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

Generator identity may eventually be shared between stable and unstable contexts,
but the context must remain explicit.

---

# 14. Stable Toda Bracket

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

# 15. Higher Toda Brackets

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
Phase 23 candidate
Indexed Toda theorem / validity connection
        ↓
Theorem representation / knowledge-table integration
        ↓
Generator typing / ambient-group facts when actual tables require them
        ↓
Stable homotopy representation
        ↓
Stable Toda bracket
  <a,b,c>
        ↓
Higher Toda bracket
  only when actual examples require it
```

Phase 23 以降の numbering は provisional。

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
| `GeneratorSymbol` | IMPLEMENTED | Phase 22 |
| generator family / index / decoration | IMPLEMENTED | Phase 22 |
| `ν / ν′ / decorated ν` distinction | IMPLEMENTED | Phase 22 |
| `η_n / μ_n / ι_n` structured notation | IMPLEMENTED | Phase 22 |
| `HomotopyElement.generator` | IMPLEMENTED | Phase 22 |
| generator + source / target coexistence | IMPLEMENTED | Phase 22 |
| legacy HomotopyElement compatibility | IMPLEMENTED | Phase 22 |
| `{η₃,Eν′,ν₇}_1` structured-generator form | IMPLEMENTED | Phase 22 |
| indexed Toda theorem validity connection | NEXT CANDIDATE | Phase 23 |
| generator table lookup | PLANNED | actual table need |
| automatic generator typing | PLANNED | later typing / table layer |
| ambient homotopy group validation | PLANNED | later typing layer |
| theorem representation | PLANNED | assumptions / conclusion / source |
| knowledge-table integration | PLANNED | facts with provenance |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer required |
| stable degree / stem checking | PLANNED | convention to be fixed |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 19. Phase 22 completion boundary

Implemented:

```text
GeneratorSymbol
HomotopyElement.generator
```

with:

```text
GeneratorSymbol.family: str
GeneratorSymbol.index: int | None
GeneratorSymbol.decoration: str | None
```

Representative:

```text
ν
ν′
barν
η₃
μ₃
ι₇
{η₃,Eν′,ν₇}_1
```

Boundary:

```text
GeneratorSymbol
!=
Expression
```

```text
family / index / decoration
=
structural identity
```

```text
generator notation
!=
automatic typing
```

```text
generator identity
!=
Suspension operation
```

```text
constructible
!=
validated
```

```text
legacy HomotopyElement API
=
preserved
```

No decoration normalization.

No generator table lookup.

No automatic source / target derivation.

No name / generator validation.

No ambient homotopy-group / stem / stable-context validation.

No indexed Toda theorem applicability.

Generic inference engine unchanged.

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

# 20. Testing Principle

新しい mathematical layer を追加するときは:

1. representation test
2. structural distinction test
3. validity / applicability test
4. invalid-case behavior
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
structured generator identity
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
structured generator identity
stable Toda-bracket membership
```

を provenance 付き knowledge として保持する。
