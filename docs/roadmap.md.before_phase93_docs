# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。

過去の詳細な実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明・infrastructure trace は `docs/proof_records.md` を参照する。

---

# 1. 現在地

数学面:

```text
Toda Lemma 5.16 までの concrete proof spine
stable G_0 through G_7
0-stem から 7-stem までの主要な 2-primary / Toda π_i^n 計算材料
```

proof infrastructure:

```text
Proof Repository
→ automatic final-rule selection
→ missing-premise producer analysis
→ bounded dependency search
→ max_depth parameterization
→ diagnostics
→ finite explicit producer retry
→ concrete theorem-instance compatibility filtering
→ exact selected-path execution
→ goal ProofStep
```

calculation / extraction infrastructure:

```text
TodaGroupQuery
→ theorem-backed group lookup
→ TodaGroupResult
→ actual EHP extraction
→ EHP term group enrichment
→ exactness-use provenance
```

latest confirmed repository-wide regression:

```text
7203 passed in 109.03s
```

`git diff --check`:

```text
clean
```

---

# 2. completed infrastructure boundary: Phase 86–89

## Phase 86

explicit bounded-search depth parameterization:

```text
max_depth=2
max_depth=3
max_depth=4
```

default:

```text
max_depth=2
```

## Phase 87

finite explicit producer retry:

```text
FiniteProducerRetryPolicy(max_attempts=N)
```

default:

```text
retry_policy=None
→ ambiguity stops
```

general backtracking は導入しない。

## Phase 88

concrete theorem-instance producer compatibility:

```text
bindings
→ requested_statement
→ concrete-compatible producers
```

same conclusion type collision と same concrete theorem ambiguity を区別する。

## Phase 89

post-Phase88 audit:

```text
general backtracking の actual theorem-backed need
→ 未確認

producer ranking / proof-cost model
→ concrete need 未確認

max_depth > 4
→ actual need 未確認
```

したがって proof-search algorithm の抽象的一般化は deferred。

---

# 3. Phase 90 COMPLETE：Toda group query / known-result lookup

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

actual verification:

```text
π_7^4
π_10^4
π_9^2=0
```

lookup miss:

```text
()
```

proof search on miss は行わない。

---

# 4. Phase 91 COMPLETE：normalized group result

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

zero:

```text
group_structure=None
generators=()
generator_orders=()
```

---

# 5. Phase 92 COMPLETE：EHP extraction / enrichment / exactness provenance

Phase 92 は旧3分割計画ではなく、実装結果に合わせて次の5段階で確定する。

## Phase 92-1：current EHP representation audit

確認:

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
ProofStep provenance
TodaGroupResult
```

は既存。

不足:

```text
result aggregation
actual theorem-backed extraction
group enrichment
exactness-use connection
```

### 状態

COMPLETE

## Phase 92-2：minimal EHP sequence / window result representation

追加:

```text
TodaEHPExactnessWindowResult
TodaEHPSequenceResult
```

保持:

```text
existing sequence/window identity
target
window order
contiguous-window validation
subset-window support
```

### 状態

COMPLETE

## Phase 92-3：actual theorem-backed EHP extraction integration

入口:

```text
TodaGroupResult.proof_step
```

actual proof ancestry から `TodaProp42ExactnessStatement` を抽出し、contiguous EHP chain を構成する。

actual `π_9^5`:

```text
π_10^9 --Δ--> π_8^4 --E--> π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

重要:

```text
repository 内の全 EHP facts
```

ではなく:

```text
final proof ancestry から到達可能な EHP facts
```

を取得する。

### 状態

COMPLETE

## Phase 92-4：connect known group structures to EHP terms

追加:

```text
TodaEHPGroupTermResult
TodaEHPGroupEnrichmentResult
connect_known_toda_group_results()
```

actual integration:

```text
π_10^9 -> unknown
π_8^4  -> known
π_9^5  -> known
π_9^9  -> unknown
π_7^4  -> known
```

区別:

```text
unknown
→ group_results=()

known zero
→ TodaGroupResult(group_structure=None)
```

### 状態

COMPLETE

## Phase 92-5：exactness-use provenance integration

追加:

```text
TodaEHPExactnessUseResult
TodaEHPExactnessUseProvenanceResult
extract_toda_ehp_exactness_use_provenance()
```

各 window:

```text
window_result
↓
actual exactness ProofStep
↓
direct consumer ProofSteps
```

まで接続する。

例:

```text
H-Δ exactness
→ actual TodaProp42ExactnessStatement
→ hopf-zero derivation consumer
```

Phase 92-5 latest regression:

```text
68 passed in 8.90s
repository-wide:
7203 passed in 109.03s
```

### 状態

COMPLETE

---

# 6. Phase 93：proof dependency extraction / explanation layer

次の Phase。

目的:

```text
final theorem-backed result
↓
actually used intermediate mathematical facts
↓
machine-readable dependency structure
```

対象候補:

```text
propositions
lemmas
relations
known groups
EHP exactness facts
map properties
generator / order facts
```

最初は audit から開始する。

推奨分割:

```text
Phase 93-1
current proof-dependency representation / traversal audit

Phase 93-2
minimal dependency-result representation

Phase 93-3
actual theorem-backed dependency extraction

Phase 93-4
dependency role classification

Phase 93-5
representative explanation integration
```

Phase 93 の重要原則:

```text
potentially relevant facts
```

ではなく:

```text
actually reachable / actually used facts
```

を扱う。

Phase 92 の EHP-specific traversal をそのまま generic 化せず、actual need を確認してから最小設計する。

---

# 7. Phase 94：recursive proof provenance

Phase 93 で dependency node / role が安定した後に進む。

目的:

```text
final result
├─ dependency A
│  ├─ premise A1
│  ├─ premise A2
│  └─ proof of A
├─ dependency B
│  └─ proof of B
└─ dependency C
   └─ imported / assumed
```

status 候補:

```text
derived
proved
imported
assumed
```

これらの正式 semantics は Phase 94 audit で確定する。

---

# 8. Phase 95：calculation orchestration

Phase 90–94 の layer を user-facing calculation API に束ねる。

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
dependencies / provenance
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
proof dependencies
literature references
```

出力候補:

```text
Markdown
console
LaTeX
JSON-like structured report
```

automatic narrative は proof data と分離する。

```text
presentation != proof truth
```

を維持する。

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
current code
related tests
actual theorem-backed need
```

を確認する。

将来 Phase の capability を先取りしない。

---

# 12. 直近の次作業

次:

```text
Phase 93-1
current proof-dependency representation / traversal audit
```

監査対象:

```text
ProofStep.premises
ProofStep.inference_rule
LiteratureStatement
ProofRepositoryEntry metadata
TodaGroupResult
Phase 92 EHP-specific traversal
existing probe presentation helpers
```

確認する中心:

```text
どこまで既存 provenance だけで dependency を分類できるか
同一 ProofStep 再訪をどう扱うか
shared dependency をどう表現するか
direct dependency と transitive dependency をどう区別するか
role classification をどこまで Phase 93 で必要とするか
Phase 94 recursive proof presentation と何を分離するか
```
