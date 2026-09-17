# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。

過去の詳細な実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明・infrastructure trace は `docs/proof_records.md` を参照する。

---

# 1. 現在地

数学面:

```text
Toda Lemma 5.16 までの concrete proof spine
stable G_0 through G_7
0-stem から 7-stem までの主要 2-primary / Toda π_i^n 計算材料
```

proof-search infrastructure:

```text
Proof Repository
→ automatic final-rule selection
→ missing-premise producer analysis
→ concrete theorem-instance compatibility filtering
→ bounded dependency search
→ explicit max_depth
→ finite producer retry
→ search / execution diagnostics
→ exact selected-path execution
→ goal ProofStep
```

calculation / explanation infrastructure:

```text
TodaGroupQuery
→ theorem-backed group lookup
→ TodaGroupResult
→ actual EHP extraction
→ EHP term group enrichment
→ exactness-use provenance
→ proof dependency extraction
→ dependency role classification
→ representative explanation integration
```

latest confirmed repository-wide regression:

```text
7269 passed in 102.15s
```

`git diff --check`:

```text
clean
```

---

# 2. Phase 90 COMPLETE：Toda group query / known-result lookup

完成:

```text
TodaGroupQuery(n,k)
↓
TodaPrimaryGroup(n+k,n)
↓
ProofRepository
↓
theorem-backed group result
↓
original ProofStep
```

lookup miss:

```text
()
```

proof search on miss は行わない。

---

# 3. Phase 91 COMPLETE：normalized group result

完成:

```text
TodaGroupResult

target
group_structure
generators
generator_orders
source_entry
proof_step
```

保持:

```text
source_entry identity
ProofStep identity
premise provenance
group-structure object identity
repository non-mutation
```

---

# 4. Phase 92 COMPLETE：EHP extraction / enrichment / exactness provenance

完成:

```text
TodaEHPSequenceResult
TodaEHPGroupEnrichmentResult
TodaEHPExactnessUseProvenanceResult
```

actual `π_9^5`:

```text
π_10^9 --Δ--> π_8^4 --E--> π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

原則:

```text
repository 内の potentially relevant facts
```

ではなく:

```text
final proof ancestry から actually reachable な facts
```

を扱う。

---

# 5. Phase 93 COMPLETE：proof dependency extraction / explanation integration

## Phase 93-1

current dependency representation / traversal audit。

確定:

```text
direct vs transitive dependency
shared ProofStep identity
actual proof ancestry as truth source
Phase 92 EHP traversal と generic dependency layer の境界
Phase 94 recursive provenance との境界
```

## Phase 93-2

追加:

```text
TodaProofDependency
TodaProofDependencyResult
```

最低限:

```text
proof_step
depth
is_direct
```

を表現。

## Phase 93-3

追加:

```text
extract_toda_proof_dependencies()
```

semantics:

```text
breadth-first traversal
shortest depth
premises-order stable traversal
identity-based deduplication
cycle-safe
non-ProofStep premise exclusion
```

actual `π_9^5` で theorem-backed dependency extraction を確認。

## Phase 93-4

追加:

```text
TodaProofDependencyRole
classify_toda_proof_step_role()
```

roles:

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

未知 statement を文字列推測で分類しない。

## Phase 93-5

追加:

```text
TodaRepresentativeExplanationResult
build_toda_representative_explanation()
```

統合:

```text
TodaGroupResult
+
TodaEHPSequenceResult
+
TodaEHPExactnessUseProvenanceResult
+
TodaProofDependencyResult
```

Phase 93 completion regression:

```text
Phase 93 focused:
66 passed in 7.61s

Phase 92 -> 93:
88 passed in 5.05s

repository-wide:
7269 passed in 102.15s
```

### 状態

COMPLETE

---

# 6. Phase 94：recursive proof provenance

次の Phase。

Phase 93 の flat dependency view:

```text
dependency
proof_step
depth
role
```

から、proof edge を first-class にする。

目標イメージ:

```text
final result
├─ dependency A
│  ├─ premise A1
│  └─ premise A2
├─ dependency B
│  └─ shared dependency
└─ dependency C
```

重要:

```text
proof structure is generally a DAG
not necessarily a tree
```

shared dependency を複製しない representation が必要。

---

# 7. Phase 94 推奨分割

```text
Phase 94-1
current recursive provenance / DAG representation audit

Phase 94-2
minimal proof-node / edge representation

Phase 94-3
actual theorem-backed recursive provenance extraction

Phase 94-4
shared-node / cycle / stable-order regression

Phase 94-5
representative Phase 93 explanation integration
```

Phase 94-1 で確認する中心:

```text
ProofStep.premises
object identity
shared ProofStep
edge order
cycle handling
root inclusion
Phase 93 shortest-depth semantics との整合
```

status 候補:

```text
derived
proved
imported
assumed
```

は、actual need が確認できるまで schema に入れない。

---

# 8. Phase 95：calculation orchestration

Phase 90–94 layer を user-facing calculation API に束ねる。

概念:

```text
(n,k)
↓
target π_{n+k}^n
↓
known-result lookup
or
authorized bounded proof search
↓
normalized group result
↓
EHP context
↓
dependencies / recursive provenance
↓
structured calculation result
```

Phase 95 前に orchestration class を固定しない。

---

# 9. Phase 96：human-readable explanation / proof report

structured calculation result から presentation を生成する。

目標:

```text
target
group structure
generators
orders
EHP sequence
known groups on EHP terms
exactness uses
required lemmas / propositions / relations
recursive proof provenance
literature references
```

出力候補:

```text
Markdown
console
LaTeX
JSON-like structured report
```

重要:

```text
presentation != proof truth
```

を維持する。

Phase 93 の `TodaRepresentativeExplanationResult` は structured integration であり、Phase 96 の natural-language narrator ではない。

---

# 10. deferred capabilities

actual theorem-backed need が出るまで実装しない:

```text
unbounded proof search
general backtracking
producer ranking
proof-cost optimization
best-proof selection
persistent global proof cache
persistent Proof Repository
general CAS normalization
generic sign algebra
generic theorem proving
odd-primary full integration
ordinary π_{n+k}(S^n) all-primary calculator
```

---

# 11. completion policy

各 Phase は最低限:

```text
focused pytest
related regression
repository-wide pytest
git diff --check
```

を確認して COMPLETE とする。

実装前:

```text
current GitHub code
related tests
actual theorem-backed need
```

を確認する。

将来 Phase の capability を先取りしない。

---

# 12. 直近の次作業

次:

```text
Phase 94-1
current recursive provenance / DAG representation audit
```

監査対象:

```text
ProofStep.premises
TodaProofDependencyResult
extract_toda_proof_dependencies()
TodaRepresentativeExplanationResult
Phase 92 exactness provenance traversal
actual π_9^5 proof graph
```

確認する中心:

```text
flat dependency list から何を追加すれば DAG を lossless に表現できるか
shared node を identity でどう保持するか
edge order をどう保持するか
shortest depth と recursive edge structure をどう分離するか
cycle guard を representation と extraction のどちらに置くか
Phase 96 narrative layer と何を分離するか
```
