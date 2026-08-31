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

# 2. Phase 23 完了時点の実装基盤

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
indexed theorem fact preservation
bracket-index theorem matching
generator-structure theorem matching
indexed theorem / definedness connection
canonical indexed structural-consistency guard
canonical indexed typing guard
indexed guarded theorem → membership bridge
actual ε₃ ∈ {η₃,Eν′,ν₇}_1 representative bridge
indexed / unindexed membership separation
indexed theorem provenance regression
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

Current representative canonical indexed form:

```text
{a,E^t b,E^t c}_t
```

Current representative actual literature form:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
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

## 3.7 canonical representation と literature-specific representation を無理に統合しない

Current example:

```text
canonical:
{a,E^t b,E^t c}_t
```

```text
specific literature:
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

同じ数学的テーマでも current structural roles が異なる場合は、
実際の theorem requirement が出るまで無理に normalization しない。

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
Phase 23  Indexed Toda theorem / validity connection
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

`HomotopyElement` stores:

```text
generator: GeneratorSymbol | None
```

Important:

```text
generator notation
↛
automatic source / target typing
```

Representative literature structure:

```text
{η₃,Eν′,ν₇}_1
```

is losslessly representable.

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

# 10. Phase 23 完了：Indexed Toda theorem / validity connection

Phase 23 は:

```text
indexed Toda structure
+
typed entries
+
structured generator identity
+
actual theorem fact
```

を membership inference に接続した。

## 10.1 theorem fact

既存:

```text
TodaBracketMembershipTheoremStatement
```

を再利用。

No parallel indexed theorem class.

## 10.2 bracket-index match

Whole-bracket structural equality により:

```text
_1 == _1
_1 != _2
_1 != None
```

を theorem applicability に反映。

## 10.3 generator structure match

Theorem / definedness matching は:

```text
GeneratorSymbol.family
GeneratorSymbol.index
GeneratorSymbol.decoration
```

まで含む。

## 10.4 definedness dependency

```text
theorem alone
↛ membership

definedness alone
↛ membership

theorem + matching definedness
→ membership
```

## 10.5 canonical indexed guarded bridge

追加:

```text
indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data
)
```

Canonical target:

```text
{a,E^t b,E^t c}_t
```

Requires:

```text
indexed_data.is_consistent()
```

and:

```text
bracket.are_defining_compositions_type_compatible()
```

plus matching theorem / definedness.

Therefore:

```text
theorem
+
definedness
+
structural consistency
+
typing compatibility
↓
membership
```

## 10.6 invalid canonical cases

Reject:

```text
index / exponent mismatch
entry / base mismatch
known typing mismatch
unknown typing
```

## 10.7 actual ε₃ representative

Actual:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

uses:

```text
Eν′ = Suspension(ν′)
ν₇ = structured generator
index = 1
```

It is not forced into canonical `IndexedTodaBracketData`.

Specific theorem uses narrow literature bridge:

```text
specific theorem fact
+
exactly matching definedness
↓
membership
```

## 10.8 provenance

Membership direct provenance:

```text
theorem_step
defined_step
```

Unrelated facts are excluded.

Theorem source / note are preserved.

## 10.9 indexed / unindexed separation

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

does not automatically create:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

Phase 19 の `_1` loss limitation は解消。

Verified Phase 23 completion:

```text
tests/test_toda_rules.py
66 passed in 1.01s
```

```text
full suite
1175 passed in 22.96s
```

Generic inference engine unchanged.

---

# 11. Phase 24 candidate：Theorem fact / knowledge-table integration

Natural next dependency:

```text
structured theorem facts
+
LiteratureReference
+
current Statement / Relation models
↓
knowledge repository / table
↓
ProofStep.GIVEN
↓
existing inference rules
```

Phase 23 では theorem fact を Python code 上で直接組み立てている。

Phase 24 candidate では、actual literature-backed facts を:

```text
data / table
↓
structured theorem statement
↓
proof graph
```

へ供給する最小 layer を検討する。

Important:

```text
knowledge table
!=
universal theorem prover
```

```text
stored fact
!=
automatically applicable theorem
```

```text
source metadata
=
must remain attached
```

Potential first targets:

```text
Toda membership theorem facts
composition facts
order facts
Hopf-invariant facts
generator identity facts
```

ただし最初からすべてを共通 schema に押し込まない。

Actual repeated need がある fact family から始める。

---

# 12. Theorem Representation

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

Phase 24 candidate はまず theorem fact repository / loading を優先し、
general quantified theorem language は deferred とするのが安全。

---

# 13. Knowledge Tables

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

but Phase 22/23 deliberately do not perform this lookup automatically.

---

# 14. Generator typing / ambient-group facts

Potential later layer:

```text
generator fact
+
source / target table
↓
explicit typing knowledge
```

Examples may eventually include:

```text
η_n
ν_n
μ_n
ι_n
```

Important:

```text
GeneratorSymbol
↛
automatic typing
```

until an explicit fact/table layer is introduced.

Do not silently derive typing from generator index.

---

# 15. Stable Homotopy Groups

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

# 16. Stable Toda Bracket

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

# 17. Higher Toda Brackets

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

# 18. ORDER / Divisibility / Annihilator

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

# 19. Recommended future order

```text
Phase 24 candidate
Theorem fact / knowledge-table integration
        ↓
Generator typing / ambient-group facts
        ↓
Theorem representation generalization
  only when actual quantified theorems require it
        ↓
Stable homotopy representation
        ↓
Stable Toda bracket
  <a,b,c>
        ↓
Higher Toda bracket
  only when actual examples require it
```

Phase 24 以降の numbering は provisional。

Actual mathematical need に応じて再配置可能。

---

# 20. 実装状況

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
| Toda bracket definedness | IMPLEMENTED | Phase 18 |
| Toda theorem + definedness → membership | IMPLEMENTED | Phase 19 |
| literature-backed ε₃ Toda bridge | IMPLEMENTED | Phase 19 / Phase 23 actual indexed form |
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
| indexed theorem fact preservation | IMPLEMENTED | Phase 23 |
| bracket-index theorem matching | IMPLEMENTED | Phase 23 |
| generator-structure theorem matching | IMPLEMENTED | Phase 23 |
| indexed theorem + definedness → membership | IMPLEMENTED | Phase 23 |
| canonical indexed structural guard | IMPLEMENTED | Phase 23 |
| canonical indexed typing guard | IMPLEMENTED | Phase 23 |
| canonical guarded theorem bridge | IMPLEMENTED | Phase 23 |
| actual `ε₃ ∈ {η₃,Eν′,ν₇}_1` bridge | IMPLEMENTED | Phase 23 |
| indexed → unindexed collapse prevention | IMPLEMENTED | Phase 23 |
| theorem fact / knowledge-table integration | NEXT CANDIDATE | Phase 24 |
| generator table lookup | PLANNED | actual table need |
| automatic generator typing | PLANNED | later typing / table layer |
| ambient homotopy group validation | PLANNED | later typing layer |
| general theorem representation | PLANNED | quantified theorem need |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer required |
| stable degree / stem checking | PLANNED | convention to be fixed |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 21. Phase 23 completion boundary

Implemented:

```text
indexed theorem fact
indexed bracket matching
structured generator matching
definedness dependency
canonical consistency guard
canonical typing guard
guarded indexed theorem bridge
actual ε₃ representative bridge
provenance boundary
indexed / unindexed separation
```

General canonical bridge:

```text
theorem
+
definedness
+
consistency
+
typing
↓
membership
```

Specific actual bridge:

```text
ε₃ theorem fact
+
matching definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Boundary:

```text
is_consistent()
!=
theorem applicability by itself
```

```text
type-compatible
!=
Toda definedness
```

```text
Suspension(ν′)
!=
IteratedSuspension(ν′,1)
```

```text
canonical guarded bridge
!=
specific literature bridge
```

```text
indexed membership
!=
unindexed membership
```

No generator lookup.

No automatic typing.

No universal theorem prover.

Generic inference engine unchanged.

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

# 22. Testing Principle

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
structured generator identity
+
literature-backed theorem facts
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
theorem provenance
stable Toda-bracket membership
```

を provenance 付き knowledge として保持する。
