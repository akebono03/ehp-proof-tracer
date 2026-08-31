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

# 2. Phase 24 完了時点の実装基盤

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
TheoremFactEntry
TheoremFactRepository
LiteratureReference-backed theorem fact entry
registered ε₃ Toda membership theorem fact
THEOREM_FACT_REPOSITORY
structural theorem-fact lookup
unknown / empty lookup boundary
duplicate structural theorem rejection
statement materialization with source provenance
repository theorem fact → ProofStep.GIVEN
repository ε₃ end-to-end representative
repository provenance exclusion regression
repository inference fixed-point regression
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
TheoremFactEntry
TheoremFactRepository
```

Current representative canonical indexed form:

```text
{a,E^t b,E^t c}_t
```

Current representative actual literature form:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Current repository representative:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
↓
THEOREM_FACT_REPOSITORY
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

```text
stored repository fact
≠
derived mathematical conclusion
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

Repository semantics も generic inference engine から分離する。

## 3.7 canonical representation と literature-specific representation を無理に統合しない

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

## 3.8 repository identity を早すぎる汎用 key system にしない

Current Phase 24 lookup identity:

```text
structural theorem statement
```

Fact key / stable ID / external schema は actual need が出てから導入する。

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
Phase 24  Theorem fact / knowledge-table integration
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

The indexed-loss gap became Phase 20's requirement.

---

# 7. Phase 20 完了：Indexed Unstable Toda Notation

Implemented:

```text
TodaBracket.index
IteratedSuspension
IndexedTodaBracketData
IndexedTodaBracketData.is_consistent()
```

Target:

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

Critical:

```text
typed
!=
untyped
```

```text
type compatibility
!=
ZERO
!=
Toda definedness
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

Representative:

```text
{η₃,Eν′,ν₇}_1
```

is losslessly representable.

---

# 10. Phase 23 完了：Indexed Toda theorem / validity connection

Phase 23 connected:

```text
indexed Toda structure
+
typed entries
+
structured generator identity
+
actual theorem fact
```

to membership inference.

General canonical bridge:

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

Specific actual bridge:

```text
ε₃ theorem fact
+
matching definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Critical:

```text
Suspension(ν′)
!=
IteratedSuspension(ν′,1)
```

```text
indexed membership
!=
unindexed membership
```

No generator lookup.

No automatic typing.

Generic inference engine unchanged.

---

# 11. Phase 24 完了：Theorem fact / knowledge-table integration

Phase 24 added a minimal literature-backed theorem repository.

Dependency:

```text
structured theorem fact
+
LiteratureReference
↓
TheoremFactEntry
↓
TheoremFactRepository
↓
ProofStep.GIVEN
↓
existing inference rule
↓
proof graph
```

## 11.1 Repository representation

Implemented:

```text
TheoremFactEntry
TheoremFactRepository
```

Current narrow fact family:

```text
TodaBracketMembershipTheoremStatement
```

No universal theorem schema.

## 11.2 Literature provenance

Each fact entry stores:

```text
statement
reference
```

using existing:

```text
LiteratureReference
```

`materialize_statement()` explicitly transfers:

```text
entry.reference
→ statement.source
```

without mutating stored repository data.

## 11.3 Actual registered fact

Production representative:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
```

for:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

registered in:

```text
THEOREM_FACT_REPOSITORY
```

## 11.4 Lookup

Current API:

```text
repository.lookup(statement)
```

Behavior:

```text
known → entry
unknown → None
empty → None
```

No fact key / ID.

## 11.5 Duplicate boundary

Current theorem identity is structural statement equality.

Therefore:

```text
same theorem statement
+
another reference
→ duplicate
→ reject
```

This makes lookup result unique.

## 11.6 ProofStep connection

`TheoremFactEntry.to_proof_step()` reuses the existing Toda theorem helper.

```text
repository fact
↓
materialized theorem
↓
ProofStep.GIVEN
```

No new proof rule.

## 11.7 End-to-end representative

```text
repository ε₃ theorem fact
↓
GIVEN theorem step
+
matching definedness
↓
existing Toda theorem bridge
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

## 11.8 Provenance / scope

Direct premises remain:

```text
theorem_step
defined_step
```

Unrelated repository theorem steps are excluded.

Matching membership is not duplicated.

Inference reaches:

```text
FIXED_POINT
```

Generic inference engine unchanged.

Verified:

```text
tests/test_theorem_facts.py
15 passed
```

```text
full suite
1190 passed in 61.30s
```

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

Current `InferenceRule`, narrow theorem statements, and Phase 24 repository should
be reused where possible.

Only generalize theorem representation when actual quantified theorem
requirements prove that the current narrow model is insufficient.

Phase 24 did not introduce a universal theorem language.

---

# 13. Knowledge Tables

Current implemented slice:

```text
Toda membership theorem fact
↓
TheoremFactRepository
↓
ProofStep.GIVEN
↓
existing Toda inference
```

Long-term possible inputs remain:

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

Do not immediately force all fact families into one universal schema.

Actual repeated need should drive generalization.

---

# 14. Phase 25 candidate：Generator typing / ambient-group facts

Natural next dependency:

```text
GeneratorSymbol
+
explicit generator fact
↓
source / target / ambient-group knowledge
↓
typed theorem applicability
```

Potential examples:

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

and:

```text
GeneratorSymbol.index
↛
source / target
```

unless explicit fact knowledge supplies the connection.

Phase 25 should determine the first actual generator fact family before choosing
a table schema.

Possible minimal targets:

```text
generator identity
→ explicit source / target fact

generator identity
→ ambient π_m(S^n) fact
```

but the exact first representation should be chosen from actual mathematical
need.

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
but context must remain explicit.

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

Distinguish:

```text
number of entries
Toda order
bracket index
stem
stable / unstable context
```

Do not infer bracket order solely from entry count.

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
Phase 25 candidate
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

Possible parallel / later knowledge-table work:

```text
external JSON / YAML loader
fact key / stable ID
multiple-source bibliography
additional fact families
```

should be added only when actual data-management requirements arise.

Phase 25 以降の numbering は provisional。

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
| literature-backed ε₃ Toda bridge | IMPLEMENTED | Phase 19 / Phase 23 |
| Toda bracket concrete / symbolic index | IMPLEMENTED | Phase 20 |
| `IteratedSuspension` | IMPLEMENTED | Phase 20 |
| `IndexedTodaBracketData` | IMPLEMENTED | Phase 20 |
| `{a,E^t b,E^t c}_t` structural form | IMPLEMENTED | Phase 20 |
| indexed Toda consistency predicate | IMPLEMENTED | Phase 20 |
| typed source / target | IMPLEMENTED | Phase 21 |
| Suspension typing shift | IMPLEMENTED | Phase 21 |
| concrete IteratedSuspension typing shift | IMPLEMENTED | Phase 21 |
| Composition type compatibility | IMPLEMENTED | Phase 21 |
| Toda entry composition compatibility | IMPLEMENTED | Phase 21 |
| `GeneratorSymbol` | IMPLEMENTED | Phase 22 |
| generator family / index / decoration | IMPLEMENTED | Phase 22 |
| `HomotopyElement.generator` | IMPLEMENTED | Phase 22 |
| structured `{η₃,Eν′,ν₇}_1` | IMPLEMENTED | Phase 22 |
| indexed theorem fact preservation | IMPLEMENTED | Phase 23 |
| bracket-index theorem matching | IMPLEMENTED | Phase 23 |
| generator-structure theorem matching | IMPLEMENTED | Phase 23 |
| indexed theorem + definedness → membership | IMPLEMENTED | Phase 23 |
| canonical indexed structural / typing guards | IMPLEMENTED | Phase 23 |
| actual indexed ε₃ bridge | IMPLEMENTED | Phase 23 |
| indexed → unindexed collapse prevention | IMPLEMENTED | Phase 23 |
| `TheoremFactEntry` | IMPLEMENTED | Phase 24 |
| `TheoremFactRepository` | IMPLEMENTED | Phase 24 |
| LiteratureReference-backed repository entry | IMPLEMENTED | Phase 24 |
| registered ε₃ theorem fact | IMPLEMENTED | Phase 24 |
| structural theorem-fact lookup | IMPLEMENTED | Phase 24 |
| unknown / empty lookup boundary | IMPLEMENTED | Phase 24 |
| duplicate structural fact rejection | IMPLEMENTED | Phase 24 |
| theorem statement materialization | IMPLEMENTED | Phase 24 |
| repository theorem → `ProofStep.GIVEN` | IMPLEMENTED | Phase 24 |
| repository ε₃ end-to-end representative | IMPLEMENTED | Phase 24 |
| repository provenance / fixed-point regression | IMPLEMENTED | Phase 24 |
| external knowledge-table loader | PLANNED | actual file-loading need |
| fact key / stable ID | PLANNED | actual lookup need |
| multiple literature sources per fact | PLANNED | actual bibliography need |
| generator table lookup | NEXT CANDIDATE | Phase 25 |
| automatic generator typing | PLANNED | explicit fact layer first |
| ambient homotopy group validation | PLANNED | Phase 25+ |
| general theorem representation | PLANNED | quantified theorem need |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer required |
| stable degree / stem checking | PLANNED | convention to be fixed |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 21. Phase 24 completion boundary

Implemented:

```text
literature-backed Toda theorem repository
fact entry + LiteratureReference
actual ε₃ registered fact
structural lookup
unknown / empty lookup
duplicate statement rejection
provenance materialization
ProofStep.GIVEN connection
actual repository-to-membership representative
unrelated-fact provenance exclusion
fixed-point / duplicate-conclusion boundary
```

Actual chain:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
↓
THEOREM_FACT_REPOSITORY
↓
lookup
↓
materialized theorem
↓
ProofStep.GIVEN
+
matching definedness
↓
existing Toda theorem bridge
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
↓
FIXED_POINT
```

Boundary:

```text
repository fact
!=
membership
```

```text
lookup success
!=
theorem applicability
```

```text
structural statement
=
current lookup identity
```

```text
fact key
=
not implemented
```

```text
repository
!=
universal theorem prover
```

```text
repository
!=
external loader
```

```text
GeneratorSymbol
↛
automatic typing
```

Generic inference engine unchanged.

Verified:

```text
tests/test_theorem_facts.py
15 passed
```

```text
full suite
1190 passed in 61.30s
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
literature-backed theorem repository
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
literature provenance
repository provenance
stable Toda-bracket membership
```

を provenance 付き knowledge として保持する。
