# EHP Proof Tracer 設計

この文書は、EHP Proof Tracer の現在のアーキテクチャ、意味論、設計境界を記録する。

過去の実装経緯は `docs/development_log.md`、今後の Phase 順序は `docs/roadmap.md`、主要コードの探索は `docs/code_reference.md`、代表的な証明・infrastructure trace は `docs/proof_records.md` に分離する。

---

# 1. 基本設計原則

```text
実際の数学的・proof-search 上の必要
↓
不足している最小表現
↓
必要な explicit fact / domain rule / orchestration
↓
既存 generic inference engine
```

数学固有の theorem knowledge を generic inference engine に埋め込まない。

```text
representation != typing != theorem knowledge
structural equality != mathematical equality
catalog metadata != proof truth
search plan != proof result
calculation result != proof truth
presentation != mathematical data
```

既存 API と既存 proof provenance を保ち、将来 Phase の一般化を先取りしない。

---

# 2. 現在のレイヤー構造

基礎 layer:

```text
文献由来 theorem / explicit facts
↓
domain-specific inference rules
↓
InferenceRuleCatalog
↓
repository-assisted bounded proof search
↓
ProofStep / InferenceRule
↓
expression / statement structures
↓
homotopy / EHP data
↓
abelian-group algebra
```

Phase 90 以降の calculation / explanation layer:

```text
TodaGroupQuery
↓
theorem-backed result lookup
↓
TodaGroupResult
↓
EHP extraction
↓
EHP term group enrichment
↓
exactness-use provenance
↓
proof dependency extraction
↓
dependency role classification
↓
representative explanation integration
```

この上位 layer は、既存 theorem-backed proof object を read-only に束ねる。

Toda theorem 自体を新たに知る layer にはしない。

---

# 3. 主要モジュールの責務

```text
expression.py
= 式の structural representation

proof.py
= generic proof / inference mechanics

proof_repository.py
= in-memory ProofStep catalog

rule_catalog.py
= rule registration and search metadata

repository_inference.py
= repository-assisted bounded producer search
  diagnostics
  selected-path execution

relation_rules.py
= generic relation propagation

homotopy_groups.py
= homotopy / Toda group / EHP structural data

toda_rules.py
= Toda-specific theorem knowledge

toda_group_query.py
= Toda query validation / target construction

toda_group_lookup.py
= Toda-specific known-result lookup

toda_group_result.py
= normalized theorem-backed group result

toda_ehp_result.py
= minimal EHP sequence / window result representation

toda_ehp_extraction.py
= actual theorem-backed EHP extraction

toda_ehp_group_enrichment.py
= EHP term -> known TodaGroupResult connection

toda_ehp_exactness_provenance.py
= exactness ProofStep / direct-consumer provenance

toda_proof_dependency.py
= proof dependency representation
  breadth-first dependency extraction
  dependency role classification

toda_explanation.py
= Phase 91 / 92 / 93 representative result integration

probes/
= representative capability demonstrations

tests/
= semantic / regression / provenance verification
```

---

# 4. structural equality と mathematical equality

Python dataclass の equality は syntax tree の一致を表す。

```text
same syntax
→ structural equality
```

数学的に同値だが syntax が異なる場合は、必要な concrete theorem branch に限定して explicit relation / inference rule で接続する。

global normalization や一般 CAS 化は行わない。

proof dependency の重複判定では structural equality ではなく `ProofStep` object identity を使う。

理由:

```text
equal conclusion
!=
same provenance
```

であるため。

---

# 5. ordinary homotopy group と Toda π_i^n

`HomotopyGroup(i,n)` は ordinary `π_i(S^n)` を表す。

`TodaPrimaryGroup(i,n)` は historical class name であり、Toda (4.3) の `π_i^n` を表す。

```text
i=n
  π_n^n = π_n(S^n)

i=2n-1
  π_(2n-1)^n = E^(-1)(π_(2n)(S^(n+1);2))

otherwise
  π_i^n = π_i(S^n;2)
```

したがって:

```text
HomotopyGroup
!= structurally
TodaPrimaryGroup
```

current user-facing query target は:

```text
π_{n+k}^n
```

であり、一般の all-primary ordinary `π_{n+k}(S^n)` calculator ではない。

---

# 6. generic inference engine と proof truth

中心 object:

```text
Relation
ProofStep
PremisePattern
PatternVariable
VariableBinding
InferenceRule
InferenceMatch
InferenceRunResult
```

provenance truth source:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry` metadata:

```text
key
phase
theorem
```

は provenance metadata であり、mathematical truth 判定には使わない。

---

# 7. Proof Repository

`ProofRepository` の責務:

```text
registration
metadata
lookup
direct dependency access
```

責務ではない:

```text
proof construction
theorem truth
inference
graph rewriting
persistent storage
presentation
```

Phase 93 dependency extraction は repository 全体から「関係ありそうな fact」を集めない。

必ず:

```text
TodaGroupResult.proof_step
↓
actual reachable ProofStep ancestry
```

を truth source とする。

---

# 8. bounded proof-search の安全境界

現在維持する invariant:

```text
finite depth bound
finite retry bound
fixed-point-safe opt-in
concrete theorem-instance compatibility
cycle detection
shared dependency reuse
dependency-first execution
failed retry rollback
selected path = executed path
concrete producer-output validation
ProofStep provenance
repository non-mutation
```

defaults:

```text
max_depth=2
retry_policy=None
```

formal regression:

```text
max_depth=2
max_depth=3
max_depth=4
```

general backtracking / ranking / proof-cost model は deferred。

---

# 9. Toda group query semantics

`TodaGroupQuery(n,k)`:

```text
n is int and not bool
n >= 1

k is int and not bool
k >= 0
```

target:

```text
TodaPrimaryGroup(
  group_dimension=n+k,
  sphere_dimension=n,
)
```

query object の責務:

```text
input validation
target construction
```

責務ではない:

```text
proof truth
proof search
group computation
presentation
```

---

# 10. normalized theorem-backed group result

`TodaGroupResult`:

```text
target
group_structure
generators
generator_orders
source_entry
proof_step
```

order semantics:

```text
None
= infinite order

positive int
= finite order
```

zero group:

```text
group_structure=None
generators=()
generator_orders=()
```

identity preservation:

```text
result.source_entry is original ProofRepositoryEntry
result.proof_step is original ProofStep
result.group_structure is original RHS object when nonzero
```

---

# 11. EHP structural representation

既存 structural layer:

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
```

区別:

```text
TodaEHPExactnessWindow
= sequence structure

TodaProp42ExactnessStatement
= exactness theorem conclusion
```

この区別は Phase 92 / 93 でも維持する。

---

# 12. Phase 92 EHP result layer

主要 result:

```text
TodaEHPExactnessWindowResult
TodaEHPSequenceResult
TodaEHPGroupTermResult
TodaEHPGroupEnrichmentResult
TodaEHPExactnessUseResult
TodaEHPExactnessUseProvenanceResult
```

actual extraction:

```text
TodaGroupResult.proof_step
↓
reachable ProofStep ancestry
↓
TodaProp42ExactnessStatement
↓
relevant exactness windows
↓
contiguous EHP chain
```

代表:

```text
π_10^9 --Δ--> π_8^4 --E--> π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

exactness-use provenance:

```text
window_result
↓
actual exactness ProofStep
↓
direct reachable consumer ProofSteps
```

---

# 13. Phase 93 dependency representation

追加:

```text
TodaProofDependency
TodaProofDependencyResult
```

`TodaProofDependency`:

```text
proof_step
depth
role
```

`is_direct`:

```text
depth == 1
```

`TodaProofDependencyResult`:

```text
root_step
dependencies
```

invariants:

```text
root_step is ProofStep
root_step does not appear in dependencies
dependencies is ordered tuple
same ProofStep identity appears at most once
equal-but-distinct ProofStep objects remain distinct
```

role 未指定での既存 API compatibility のため:

```text
role = OTHER
```

を default とする。

---

# 14. Phase 93 dependency traversal semantics

入口:

```text
TodaGroupResult.proof_step
```

traversal:

```text
breadth-first search
```

理由:

```text
shared dependency
→ first reached depth is shortest depth
```

例:

```text
root
├─ A
│  └─ shared
└─ B
   └─ C
      └─ shared
```

`shared` は:

```text
depth=2
```

を保持する。

queue への追加順は各 `ProofStep.premises` tuple order を維持する。

したがって同じ proof graph に対して traversal order は deterministic。

visited 判定:

```text
id(ProofStep)
```

root identity も visited に最初から含めるため cycle が存在しても root は dependency として戻らない。

non-`ProofStep` premise は dependency graph へ含めない。

---

# 15. dependency role classification

`TodaProofDependencyRole`:

```text
EHP_EXACTNESS
EHP_WINDOW
GROUP_STRUCTURE
RELATION
ORDER
MAP_PROPERTY
DEFINITION
LITERATURE
OTHER
```

分類原則:

```text
first-class conclusion type
+
RelationType
```

を優先する。

例:

```text
TodaProp42ExactnessStatement
→ EHP_EXACTNESS

TodaEHPExactnessWindow
→ EHP_WINDOW

TodaPrimaryGroup = supported group structure
→ GROUP_STRUCTURE

RelationType.ORDER
→ ORDER

generic Relation
→ RELATION

TodaDeltaInjectiveStatement
TodaHopfInvariantZeroStatement
TodaSuspensionSurjectiveStatement
TodaDeltaImageUpToSignStatement
→ MAP_PROPERTY

TodaNuFamilyDefinitionStatement
→ DEFINITION

LiteratureStatement
→ LITERATURE
```

未知の Toda-specific statement を class-name string から推測しない。

未監査:

```text
→ OTHER
```

とする。

---

# 16. representative explanation integration

追加:

```text
TodaRepresentativeExplanationResult
build_toda_representative_explanation()
```

fields:

```text
group_result
ehp_result
exactness_provenance
dependency_result
```

target は:

```text
group_result.target
```

から取得する。

EHP が存在する場合:

```text
ehp_result
+
exactness_provenance
```

を両方要求する。

EHP が存在しない場合:

```text
ehp_result=None
exactness_provenance=None
```

を許容する。

dependency root:

```text
dependency_result.root_step
is
group_result.proof_step
```

を identity で要求する。

---

# 17. role-based explanation access

`TodaRepresentativeExplanationResult.dependencies_for_role()`:

```text
role
↓
dependency_result.dependencies
↓
same order の subset
```

filter は view operation であり、dependency graph を作り直さない。

代表:

```text
dependencies_for_role(MAP_PROPERTY)
```

により actual proof で使われた map property dependencies を取得できる。

---

# 18. actual π_9^5 representative integration

代表 theorem-backed result:

```text
π_9^5=Z/2{ν₅η₈}
```

EHP context:

```text
π_10^9 --Δ--> π_8^4 --E--> π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

actual dependency examples:

```text
delta_e_exactness_step
e_h_exactness_step
h_delta_exactness_step
→ EHP_EXACTNESS

delta/e/h structural windows
→ EHP_WINDOW

π_8^4 group result
→ GROUP_STRUCTURE

Δ injectivity
Hopf zero
E surjectivity
→ MAP_PROPERTY

Δη₉ relation
generator bridge
→ RELATION

ν₅ definition
→ DEFINITION
```

これらは repository metadata から推測したものではなく、final proof ancestry から抽出した actual `ProofStep` である。

---

# 19. non-destructive extraction principle

Phase 90–93 の calculation / extraction / explanation layer は既存 proof graph を mutate しない。

保持する identity:

```text
ProofRepositoryEntry
ProofStep
group structure object
TodaEHPExactnessWindow
actual exactness ProofStep
actual dependency ProofStep
```

normalization / extraction / explanation は read-only view を構築する。

---

# 20. direct dependency と recursive provenance の境界

Phase 93 が扱うもの:

```text
どの ProofStep が dependency か
root からの shortest depth
direct / transitive
role
stable order
```

Phase 93 がまだ first-class に表現しないもの:

```text
dependency A
├─ premise A1
└─ premise A2
```

という recursive dependency edge result。

`ProofStep.premises` 自体にはその情報が存在するが、Phase 93 result は flat dependency view である。

これを machine-readable DAG として first-class にするのが Phase 94 の責務。

---

# 21. Phase 94 への境界

次:

```text
Phase 94
recursive proof provenance
```

最初:

```text
Phase 94-1
current recursive provenance / DAG representation audit
```

検討事項:

```text
tree ではなく DAG として shared dependency をどう保持するか
node identity を何にするか
edge order をどう保持するか
cycle guard をどこに置くか
Phase 93 flat view とどう整合させるか
derived / imported / assumed 等の status が本当に必要か
```

Phase 94 で先取りしないもの:

```text
natural-language proof generation
best-proof selection
proof ranking
generic theorem proving
persistent graph database
```

---

# 22. verification policy

Phase completion は最低限:

```text
focused tests
related regression
repository-wide pytest
git diff --check
```

で確認する。

Phase 93 completion:

```text
Phase 93 focused:
66 passed in 7.61s

Phase 92 -> 93 integration:
88 passed in 5.05s

repository-wide:
7269 passed in 102.15s

git diff --check:
clean
```

wall-clock time は machine-dependent。

cross-machine signal:

```text
test count
semantic coverage
provenance coverage
focused regression
repository-wide regression
```

---

# 23. 文書運用

```text
README.md
= current status / capabilities

docs/design.md
= current architecture / semantics / boundaries

docs/development_log.md
= chronological implementation history

docs/roadmap.md
= future-oriented plan

docs/code_reference.md
= code navigation

docs/proof_records.md
= representative mathematical / infrastructure records
```

`development_log.md` と `proof_records.md` は原則追記型。

`design.md` と `roadmap.md` は current state に合わせて古い計画を訂正・削除してよい。
