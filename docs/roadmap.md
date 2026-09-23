# EHP Proof Tracer ロードマップ

この文書は**今後の機能依存関係と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

標準 group query:

```text
n,k
→ standard production repository
→ TodaGroupQuery
→ direct known-group lookup
→ 必要なら theorem-specific specialization
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

現在利用できる限定 handoff:

\[
E(\nu_5)=\nu_6,
\]

\[
E(\sigma_{11})=\sigma_{12},
\]

\[
E(\nu_5\eta_8)=0,
\]

\[
E\nu' \in \pi_7^4.
\]

基本境界:

```text
direct lookup first
limited theorem-specific handoff != general query inference
query != general evaluator
GROUP_MEMBERSHIP != general membership evaluator
group containment != operation result
LOOKUP_MISS != evaluator required
Web UI != new mathematical engine
depth control != new proof search
show-proof != execute
explore != explore-proof
explore-proof != explore-applicable
explore-applicable != execute
proof-scope relevance != executable relevance
applicability relevance != executable relevance
candidate selection != theorem ranking
```

---

# 2. 完了済み機能

Phase 90–111:

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

Phase 112–115:

```text
real workflow pressure audit
symbolic sigma_n → TodaGroupQuery integration
E(nu_5)=nu_6 handoff
E(sigma_11)=sigma_12 handoff
```

Phase 116–125:

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

Phase 126:

```text
proof-scope / applicability / executable relevance separation
nu_prime 2 executable targets preserved
nu_5 unrelated pi6_2 executable target removed
```

Phase 127:

```text
operation-query capability pressure audit
E(nu_prime) retained for semantics audit
E(nu_5 o eta_8) selected for the next minimum capability
```

Phase 128:

```text
E(nu_5 o eta_8)=0 theorem-specific handoff
Proposition 5.8 provenance reuse
query-proof replay
repository non-mutation
```

final:

```text
9256 passed in 570.10s (0:09:30)
```

Phase 129:

```text
E(nu_prime) representation audit
operation-result semantics decision
membership result selected
E nu' in pi_7^4 theorem-specific handoff
Proposition 5.6 provenance reuse
GROUP_MEMBERSHIP result classification
direct lookup unchanged
arbitrary containment not generalized
```

focused:

```text
12 passed in 6.28s
63 passed in 12.54s
```

final:

```text
9268 passed in 569.71s (0:09:29)
```

Phase 129 は完了。

---

# 3. Phase 129 完了後の operation-query semantics

lookup-first:

```text
query
→ direct repository / proof-scope lookup
→ direct hit はそのまま返す
→ direct miss の場合だけ exact handoff guard
```

限定 handoff:

```text
E(nu_5)
→ E(nu_5)=nu_6

E(sigma_11)
→ E(sigma_11)=sigma_12

E(nu_5 o eta_8)
→ E(nu_5 eta_8)=0

E(nu_prime)
→ E nu' in pi_7^4
```

`E(nu_prime)` は Proposition 5.6 の

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}
\]

から theorem-specific に membership を具体化する。

```text
theorem-specific membership handoff
!= general E evaluator
!= general membership evaluator
!= arbitrary containment rule
```

---

# 4. Phase 130: post-Phase 129 capability re-audit

Phase 130 は general evaluator 実装から開始しない。

まず次を再監査する。

```text
1. current CLI / Web capability
2. remaining operation-query pressure
3. proof support の有無
4. user-facing result semantics
5. smallest missing capability
```

既存の deferred pressure:

```text
H(nu_5)
Delta(nu_prime)
H(sigma_11)
Delta(sigma_11)
```

Phase 127 時点では、これらは small handoff ではなく element-level proof support の不足として分類された。

したがって Phase 130 では、その分類が現行 repository でも妥当かを再確認してから次の Phase を決める。

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

# 5. Phase 130 で先取りしないもの

```text
general E evaluator
general H evaluator
general Delta evaluator
general membership evaluator
arbitrary recursive containment → operation result
general target-zero evaluator
general operation-query grammar
new theorem ranking
automatic best-target selection
general premise-component dependency engine
unbounded proof search
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

`E(nu_prime)` と `E(nu_5 o eta_8)` は完了済み。

---

# 7. 長期保留

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

# 8. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
containment と operation result を混同しない
theorem-specific handoff を general evaluator に拡張しない
focused regression で境界を固定する
CLI / Web manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
