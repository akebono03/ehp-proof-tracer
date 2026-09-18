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
flat proof dependency extraction
↓
dependency role classification
↓
recursive proof provenance extraction
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
= flat dependency representation / extraction
  dependency role classification
  recursive proof-node / edge representation
  recursive proof provenance extraction

toda_explanation.py
= Phase 91 / 92 / 93 / 94 representative result integration

probes/
= representative capability demonstrations

tests/
= semantic / regression / provenance verification
```

---

# 4. structural equality と proof identity

Python dataclass の equality は syntax tree の一致を表す。

```text
same syntax
→ structural equality
```

しかし proof provenance では:

```text
equal ProofStep
!=
same ProofStep identity
```

である。

そのため Phase 93 / 94 の dependency / node 重複判定は:

```text
id(ProofStep)
```

を使う。

equal-but-distinct `ProofStep` は別 provenance として保持する。

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

current query target は:

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

explanation / provenance extraction は repository 全体から「関係ありそうな fact」を集めない。

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

# 11. EHP structural / provenance layer

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

# 12. Phase 93 flat dependency representation

`TodaProofDependency`:

```text
proof_step
depth
role
```

`TodaProofDependencyResult`:

```text
root_step
dependencies
```

traversal:

```text
breadth-first
identity-based deduplication
premises-order stable
cycle-safe
```

`depth` は root からの shortest depth。

non-`ProofStep` premise は flat dependency に含めない。

---

# 13. dependency role classification

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

分類は主に:

```text
first-class conclusion type
+
RelationType
```

で行う。

未知 statement を theorem name や class-name substring から推測しない。

---

# 14. Phase 94 recursive proof representation

Phase 94 では proof edge を first-class にした。

`TodaProofNode`:

```text
proof_step
shortest_depth
role
```

semantics:

```text
root shortest_depth = 0
non-root shortest_depth > 0
one node per ProofStep identity
```

`TodaProofEdge`:

```text
parent_step
premise_step
premise_index
```

`premise_index` は:

```text
parent_step.premises[premise_index]
is premise_step
```

を identity で要求する。

ProofStep だけを filter した後の index へ付け替えない。

`TodaRecursiveProofProvenanceResult`:

```text
root_step
nodes
edges
```

invariants:

```text
root appears exactly once in nodes
node ProofStep identities are unique
all edge endpoints appear in nodes
duplicate identical proof edges are rejected
```

---

# 15. recursive provenance extraction semantics

入口:

```text
TodaGroupResult.proof_step
```

extractor:

```text
extract_toda_recursive_proof_provenance()
```

traversal:

```text
breadth-first search
```

node discovery:

```text
id(ProofStep)
```

で deduplicate する。

したがって shared dependency:

```text
root
├─ A
│  └─ shared
└─ B
   └─ shared
```

は:

```text
nodes:
root
A
B
shared
```

であり、`shared` を複製しない。

一方 edge は:

```text
A -> shared
B -> shared
```

の両方を保持する。

---

# 16. shortest depth と edge structure の分離

Phase 93 / 94 の `shortest_depth` は graph の summary metadata。

```text
shortest_depth
= root からの BFS 最短距離
```

recursive structure の truth は:

```text
edges
```

である。

shared dependency が複数 depth から到達可能でも node は最短 depth を保持し、全 incoming edge は失わない。

---

# 17. stable ordering

node order:

```text
breadth-first
+
ProofStep.premises tuple order
```

edge order:

```text
parent node traversal order
+
original premise_index order
```

同じ proof graph に対し deterministic な出力順を維持する。

---

# 18. non-ProofStep premise semantics

`ProofStep.premises` は `Any` を許す。

Phase 94 graph では:

```text
ProofStep premise
→ node / edge

non-ProofStep premise
→ node / edge にしない
```

ただし edge の `premise_index` は元の unfiltered tuple index を保持する。

例:

```text
premises = (
  "metadata-like premise",
  proof_step,
)

edge.premise_index = 1
```

---

# 19. cycle semantics

recursive extractor は `seen_step_ids` により無限 traversal を防ぐ。

cycle がある場合でも back-edge 自体は保持する。

```text
A -> B
B -> A
```

なら node は `A`, `B` の2個で、edge は両方向を保持する。

self-cycle:

```text
A -> A
```

も node 1個 / self-edge 1個として表現できる。

Phase 94-4 の cycle fixture は synthetic regression のためのものであり、actual representative Toda proof が cyclic だと主張するものではない。

shared revisit と cycle revisit のために新しい status enum は追加していない。現時点では graph structure 自体で区別する。

---

# 20. representative explanation integration

`TodaRepresentativeExplanationResult` fields:

```text
group_result
ehp_result
exactness_provenance
dependency_result
recursive_provenance
```

identity invariants:

```text
dependency_result.root_step
is group_result.proof_step

recursive_provenance.root_step
is group_result.proof_step
```

したがって:

```text
dependency_result.root_step
is recursive_provenance.root_step
is group_result.proof_step
```

となる。

`dependencies_for_role()` は Phase 93 API のまま維持する。

---

# 21. actual π_9^5 representative integration

代表 theorem-backed result:

```text
π_9^5=Z/2{ν₅η₈}
```

EHP context:

```text
π_10^9 --Δ--> π_8^4 --E--> π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

recursive provenance では actual Phase 68 `final_step` を root とし、その reachable ancestry を node / edge として保持する。

代表 edge:

```text
hopf_zero_step
→ delta_injective_step

hopf_zero_step
→ h_delta_exactness_step
```

さらに exactness step から structural EHP window step への edge も保持する。

flat dependency node set と recursive node set は:

```text
recursive nodes
=
root
+
flat dependencies
```

として identity ベースで整合する。

各 flat dependency の `depth` は対応 node の `shortest_depth` と一致する。

---

# 22. non-destructive extraction principle

Phase 90–94 の calculation / extraction / explanation layer は既存 proof graph を mutate しない。

保持する identity:

```text
ProofRepositoryEntry
ProofStep
group structure object
TodaEHPExactnessWindow
actual exactness ProofStep
actual dependency ProofStep
recursive graph node ProofStep
recursive graph edge endpoint ProofSteps
```

normalization / extraction / explanation は read-only view を構築する。

---

# 23. Phase 95 への境界

Phase 94 までで:

```text
theorem-backed group result
+
EHP context
+
exactness provenance
+
flat dependency view
+
recursive proof DAG
```

が structured data として揃った。

次の Phase 95 は:

```text
calculation orchestration
```

を扱う。

最初は実装ではなく:

```text
Phase 95-1
current calculation entry points / orchestration boundary audit
```

を行う。

監査対象:

```text
TodaGroupQuery
known-result lookup
TodaGroupResult
build_toda_representative_explanation()
ProofRepository
bounded proof search
```

監査前に top-level result class、lookup miss 時の proof-search fallback、ranking policy を固定しない。

---

# 24. Phase 96 との境界

Phase 96 は human-readable explanation / proof report layer。

Phase 94 の recursive provenance は machine-readable graph であって natural-language narrator ではない。

```text
structured proof truth
!=
presentation
```

を維持する。

Phase 96 まで先取りしない:

```text
automatic prose generation
automatic Markdown proof
automatic LaTeX proof
citation placement policy
proof summarization / compression
```

---

# 25. verification policy

Phase completion は最低限:

```text
focused tests
related regression
repository-wide pytest
git diff --check
```

で確認する。

Phase 94 completion の最新確認:

```text
Phase 94-5 related:
48 passed in 2.98s

repository-wide:
7313 passed in 36.98s

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

# 26. 文書運用

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
