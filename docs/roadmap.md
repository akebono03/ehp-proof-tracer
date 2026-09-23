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
→ structured presentation
→ report
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

Phase 130 は standard query の未接続・境界 semantics を整理した。

完了内容:

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

Phase 130 は完了。

---

# 3. Phase 130 後の standard-query coverage

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

# 4. Phase 131: post-Phase 130 capability audit

Phase 131 は新機能実装から開始しない。

最初に次を監査する。

```text
1. current CLI / Web capability
2. standard query で残る実利用 pressure
3. operation query で残る実利用 pressure
4. proof support の有無
5. user-facing result semantics
6. provenance reuse の可否
7. smallest missing capability
```

候補選定順:

```text
actual usage pressure
→ existing mathematics reuse audit
→ result semantics
→ provenance shape
→ minimal capability
→ scope freeze
```

---

# 5. Phase 131 の候補

```text
k >= 8 の standard query pressure
H(nu_5)
Delta(nu_prime)
H(sigma_11)
Delta(sigma_11)
Web での foundational-domain 表示確認
standard query と generator exploration の接続 gap
```

これらを実装対象と決め打ちしない。

---

# 6. 先取りしないもの

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
```

---

# 7. 残存数学 pressure

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

# 8. test / backup 運用

Phase 完了時:

```powershell
python -m pytest tests -q
```

backup は repository 外へ保存する。

repo 内 backup に copied `test_*.py` を置かない。

---

# 9. 長期保留

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

# 10. 完了判断原則

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
