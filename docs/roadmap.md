# EHP Proof Tracer ロードマップ

この文書は**今後の機能依存関係と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

標準 group query:

```text
n,k
→ query-domain classification
→ foundational specialization
→ standard production repository
→ TodaGroupQuery
→ direct known-group lookup
→ concrete proof recovery
→ 必要なら theorem-specific stable specialization
→ TodaGroupResult
→ structured presentation
→ report
```

group-result proof:

```text
TodaGroupResult
→ existing proof_step / source_entry
→ recursive provenance
→ depth-limited replay
→ TodaGroupProofPresentation
→ Trace / Outline / Narrative
→ CLI / Web
```

operation query:

```text
query
→ direct lookup
→ direct miss
→ exact theorem-specific handoff
→ presentation
→ query-proof
```

基本境界:

```text
direct lookup first
limited theorem-specific handoff != general query inference
query != general evaluator
GROUP_MEMBERSHIP != general membership evaluator
group containment != operation result
LOOKUP_MISS != evaluator required
stable specialization != general AST substitution
concrete proof recovery != arbitrary theorem mining
negative stem input != negative homotopy group definition
pi_0 information != ordinary group result
Web UI != new mathematical engine
depth control != new proof search
candidate selection != theorem ranking
group-result replay != generator lookup
group-result replay != theorem search
proof narrative != new proof
Narrative deduplication != proof graph deletion
```

---

# 2. 完了済み機能

## Phase 90–111

```text
Toda group query / normalization
EHP / proof provenance
reporting
generator exploration
recursive proof scope
applicability discovery
qualified execution
known-group identity
indexed sigma specialization
show-proof
operation query / query-proof
3-term top-level composition query
replay --depth
```

## Phase 112–115

```text
real workflow pressure audit
symbolic sigma_n → TodaGroupQuery integration
E(nu_5)=nu_6 handoff
E(sigma_11)=sigma_12 handoff
```

## Phase 116–125

```text
Flask / KaTeX Web UI
group query
operation query / query-proof
generator show-proof
generator explore
generator explore-proof
generator explore-applicable
generator execute
workflow navigation
```

## Phase 126–129

```text
proof-scope / applicability / executable relevance separation
operation-query capability pressure audit
E(nu_5 o eta_8)=0 handoff
E(nu_prime) membership semantics
E nu' in pi_7^4 handoff
GROUP_MEMBERSHIP result classification
```

Phase 129 final:

```text
9268 passed in 569.71s (0:09:29)
```

## Phase 130

```text
low-dimensional query recovery
stem 1 eta specialization
stem 2 eta^2 specialization
stem 3 nu specialization
stem 4 Prop.5.8 zero specialization
stem 5 Prop.5.9 concrete + zero specialization
stem 6 Prop.5.11 nu^2 specialization
k=0 diagonal Z{iota_n}
n=1 higher groups zero
negative stem acceptance
positive below-diagonal connectivity zero
pi_0 boundary information
negative dimension out-of-domain information
pi16_9 = Z/16{sigma_9} concrete standard-query connection
stale CLI negative-k test correction
```

final:

```text
9308 passed in 577.02s (0:09:37)
```

Phase 130 完了。

## Phase 131

```text
group-result → ProofStep path audit
TodaGroupResultProofReplayStep
TodaGroupResultProofReplayResult
build_toda_group_result_proof_replay()
existing recursive provenance reuse
depth 0 / 1 / 2
ProofStep identity preservation
source_entry identity preservation
zero-group replay
connectivity-zero replay
CLI group-proof n k
CLI group-proof n k --depth N
Web group result → Show proof
Web proof depth 0 / 1 / 2
pi_0 / negative-dimensional domain-only result exclusion
existing generator show-proof semantics preservation
```

final:

```text
9333 passed in 583.64s (0:09:43)
```

Phase 131 完了。

## Phase 132

Phase 132 は group-result proof replay の presentation layer を拡張した。

完了内容:

```text
proof narrative capability audit
ProofStep.premises edge semantics confirmation
TodaGroupProofPresentation
deterministic Outline
deterministic Narrative
safe statement / rule / type fallback
shared dependency Narrative deduplication
CLI group-proof --mode trace|outline|narrative
Trace default preservation
shared --depth semantics
Web Trace / Outline / Narrative selector
Web KaTeX preservation
proof graph non-mutation
repository non-mutation
```

final:

```text
9392 passed in 587.98s (0:09:47)
```

Phase 132 完了。

---

# 3. standard-query coverage through stem 7

```text
k < 0
→ target dimension に応じて connectivity zero / pi_0 info / out-of-domain

k = 0
→ Z{iota_n}

k = 1
→ eta family

k = 2
→ eta^2 family

k = 3
→ nu family

k = 4
→ Prop.5.8 family / zero branch

k = 5
→ Prop.5.9 family / zero branch

k = 6
→ nu^2 family

k = 7
→ sigma family
```

具体的定理 branch がある場合は generic specialization より既存 concrete proof を優先する。

---

# 4. 現在の proof access

generator 起点:

```text
generator
→ known-group identity
→ show-proof
```

group query 起点:

```text
n,k
→ TodaGroupResult
→ replay
→ Trace / Outline / Narrative
→ CLI / Web
```

operation fact 起点:

```text
query
→ selected operation fact
→ query-proof
```

これらは同じ `ProofStep` / provenance infrastructure を利用する。

---

# 5. Phase 133: post-Phase-132 capability / workflow pressure audit

Phase 133 では新機能を先に決めず、Phase 132 までの機能を実利用して次の不足を選ぶ。

監査対象:

```text
1. standard group query の実利用
2. Trace / Outline / Narrative の読みやすさと不足
3. operation query / query-proof の残件
4. generator explore / applicability / execute の利用 pressure
5. Web workflow の実利用上の不足
6. stem 7 より先の standard-query demand
```

判断原則:

```text
既存 proof にある事実を先に再利用
direct fact を上書きしない
実利用上の不足を1つ選ぶ
最小の representation / orchestration を追加
future Phase を先取りしない
```

Phase 133 の時点では次のどれも自動的な実装対象とはしない。

```text
k >= 8
H(nu_5)
Delta(nu_prime)
H(sigma_11)
Delta(sigma_11)
Narrative wording polish
rich proof graph visualization
```

---

# 6. 残存数学 pressure

```text
H(nu_5)
→ DEFER
→ element-level H proof support の再監査が必要

Delta(nu_prime)
→ DEFER
→ element-level Delta proof support の再監査が必要

H(sigma_11)
→ DEFER
→ sigma_11 Hopf transport / proof support の再監査が必要

Delta(sigma_11)
→ DEFER
→ concrete Delta proof / EHP window support の再監査が必要
```

---

# 7. proof presentation の今後の候補

Phase 132 で以下は実装済み。

```text
Trace
Outline
Narrative
shared-dependency Narrative dedup
CLI mode selection
Web mode selection
KaTeX rendering
```

今後の改善候補:

```text
Narrative の局所的な冗長表現の圧縮
role-specific deterministic templates
unsupported aggregate statement の追加 safe rendering
rich graph visualization
```

ただし実利用 pressure が確認されるまで実装しない。

---

# 8. 先取りしないもの

```text
general E evaluator
general H evaluator
general Delta evaluator
general membership evaluator
arbitrary recursive containment → operation result
general target-zero evaluator
general operation-query grammar
general symbolic AST substitution
arbitrary theorem mining from proof scope
new theorem ranking
automatic best-target selection
general premise-component dependency engine
unbounded proof search
free-form provenance-free proof generation
```

---

# 9. test / backup 運用

Phase 完了時:

```powershell
python -m pytest tests -q
```

backup は repository 外へ保存する。

repo 内 backup に copied `test_*.py` を置かない。

最新 full regression:

```text
9392 passed in 587.98s (0:09:47)
```

---

# 10. 長期保留

```text
semantic theorem ranking
semantic executable-target ranking
automatic best-target selection
general premise-component dependency engine
general operation-query grammar
general E/H/Delta evaluator
general membership evaluator
general target-zero evaluator
general Toda bracket solver
coset / indeterminacy computation
proof-cost optimization
producer ranking
unbounded backtracking
persistent cache / parallelization
repository snapshot / versioning
rich graph proof visualization
odd-primary integration
all-primary ordinary sphere-homotopy calculation
authentication
database persistence
deployment automation
rich SPA architecture
```

---

# 11. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
generic specialization より concrete proof を優先する
focused regression で境界を固定する
CLI / Web manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
