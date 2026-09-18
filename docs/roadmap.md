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
→ flat proof dependency extraction
→ dependency role classification
→ recursive proof-node / edge extraction
→ representative explanation integration
```

latest confirmed repository-wide regression:

```text
7313 passed in 36.98s
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
final proof ancestry から actually reachable な facts
```

を扱う。

---

# 5. Phase 93 COMPLETE：flat proof dependency / role / explanation integration

完成:

```text
TodaProofDependency
TodaProofDependencyResult
TodaProofDependencyRole
extract_toda_proof_dependencies()
classify_toda_proof_step_role()
TodaRepresentativeExplanationResult
build_toda_representative_explanation()
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

---

# 6. Phase 94 COMPLETE：recursive proof provenance

Phase 93 の flat dependency view から proof edge を first-class に拡張した。

## Phase 94-1 COMPLETE

current recursive provenance / DAG representation audit。

確定:

```text
node identity = ProofStep object identity
edge order = original premises order
premise_index = original unfiltered tuple index
shortest_depth = BFS shortest path
recursive edge structure と shortest depth は別概念
non-ProofStep premise は graph へ含めない
status taxonomy は actual need が出るまで追加しない
```

## Phase 94-2 COMPLETE

追加:

```text
TodaProofNode
TodaProofEdge
TodaRecursiveProofProvenanceResult
```

shared dependency を一つの node と複数 incoming edge で表現する。

## Phase 94-3 COMPLETE

追加:

```text
extract_toda_recursive_proof_provenance()
```

actual `π_9^5` で:

```text
actual Phase 68 final_step root identity
all reachable ProofStep nodes
all parent -> premise proof edges
original premise_index
Phase 93 shortest-depth compatibility
role compatibility
```

を確認。

## Phase 94-4 COMPLETE

regression-only。

固定:

```text
shared node
multiple incoming edges
BFS stable node order
stable edge order
original premise_index
cycle safety
self-cycle safety
cycle back-edge preservation
```

production code は変更しない。

## Phase 94-5 COMPLETE

`TodaRepresentativeExplanationResult` に:

```text
recursive_provenance
```

を統合。

identity invariant:

```text
dependency_result.root_step
is recursive_provenance.root_step
is group_result.proof_step
```

Phase 94 completion regression:

```text
Phase 94-5 related:
48 passed in 2.98s

repository-wide:
7313 passed in 36.98s

git diff --check:
clean
```

### 状態

COMPLETE

---

# 7. Phase 95：calculation orchestration

次の Phase。

Phase 90–94 の既存 capability を、user-facing calculation entry point へどう束ねるかを決める。

概念候補:

```text
(n,k)
↓
target π_{n+k}^n
↓
known-result lookup
↓
normalized group result
↓
EHP context
↓
flat dependencies
↓
recursive provenance
↓
structured calculation result
```

lookup miss 時に:

```text
authorized bounded proof search
```

を起動するかどうかは Phase 95-1 監査で決める。

Phase 95 前に top-level result class や fallback policy を固定しない。

---

# 8. Phase 95 推奨開始

まず:

```text
Phase 95-1
current calculation entry points / orchestration boundary audit
```

監査対象:

```text
TodaGroupQuery
find_known_toda_group_results()
find_normalized_toda_group_results()
TodaGroupResult
build_toda_representative_explanation()
ProofRepository
repository-assisted bounded proof search
```

確認する中心:

```text
1. 現在 user が (n,k) から辿る必要がある entry point は何個あるか

2. known-result lookup と explanation build を
   どの layer が束ねるべきか

3. lookup miss を
   "unknown" として返すか
   authorized proof search へ渡すか

4. multiple theorem-backed matches の扱いを
   orchestration が勝手に ranking してよいか

5. TodaGroupResult と TodaRepresentativeExplanationResult の
   identity / provenance をどう保持するか

6. orchestration result に最低限必要な field は何か

7. Phase 96 presentation を Phase 95 schema に混ぜないための境界
```

監査後にのみ Phase 95-2 以降を確定する。

---

# 9. Phase 96：human-readable explanation / proof report

structured calculation result から presentation を生成する。

目標候補:

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

Phase 94 の recursive provenance は structured graph であり、natural-language narrator ではない。

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
Phase 95-1
current calculation entry points / orchestration boundary audit
```

まず実装せず、Phase 90–94 の entry point と責務の重複・境界を監査する。
