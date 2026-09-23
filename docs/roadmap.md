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

現在の Web UI:

```text
Workflow navigation

Calculation and queries
→ group query
→ operation query

Proof and exploration
→ generator show-proof
→ generator explore
→ generator explore-proof

Applicability
→ generator explore-applicable
→ generator execute
```

`query-proof` は operation query の selected fact から利用できる。

generator execute:

```text
generator input
→ existing applicability exploration
→ qualified execution families
→ executable relevance guard
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ candidate selection when required
→ existing qualified execution
→ Result + Proof
→ CLI / Web
```

現在利用できる限定 handoff:

\[
E(\nu_5)=\nu_6,
\]

\[
E(\sigma_{11})=\sigma_{12},
\]

\[
E(\nu_5\eta_8)=0.
\]

基本境界:

```text
direct lookup first
limited theorem-specific handoff != general query inference
query != general evaluator
LOOKUP_MISS != evaluator required
target-zero theorem-specific handoff != general target-zero evaluator
Web UI != new mathematical engine
depth control != new proof search
show-proof != execute
explore != explore-proof
explore-proof != explore-applicable
explore-applicable != candidate selection
proof-scope relevance != executable relevance
applicability relevance != executable relevance
candidate selection != theorem ranking
executable relevance filtering != theorem ranking
Web execution != second execution engine
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
E(nu_5)=nu_6 existing-proof handoff
E(sigma_11)=sigma_12 existing-proof handoff
```

Phase 116–122:

```text
Web readiness audit
Flask / KaTeX
group query
operation query / query-proof
generator show-proof
generator direct explore
generator recursive explore-proof
```

Phase 123:

```text
explore-applicable Web audit
read-only compact Web exposure
existing applicability facade / presentation reuse
browser-scale display-volume audit
source / rule-family output limits
```

Phase 123 final regression:

```text
9229 passed in 509.16s (0:08:29)
```

Phase 124:

```text
execute Web readiness vs UI organization audit
single-page workflow navigation
existing section anchors
execute / candidate selection deferred
```

Phase 124 final regression:

```text
9234 passed in 522.10s (0:08:42)
```

Phase 125:

```text
existing execute workflow audit
NONE / AMBIGUOUS / EXECUTED Web boundary
thin Web execution adapter
explicit candidate selection
Result + Proof + provenance display
KaTeX integration
browser/manual audit
CLI/Web consistency audit
```

Phase 125 focused regression:

```text
14 passed in 29.80s
```

Phase 125 final regression:

```text
9243 passed in 555.37s (0:09:15)
```

Phase 126:

```text
executable-target resolution audit
proof-scope / applicability / executable relevance separation
aggregate Prop.5.6 branch audit
nu_prime / nu_5 / sigma_11 comparison
minimal executable relevance guard
nu_prime 2 targets preserved
nu_5 unrelated pi6_2 target removed
sigma_11 NONE preserved
```

Phase 126 focused regression:

```text
13 passed in 14.86s
```

Phase 126 final regression:

```text
9246 passed in 556.62s (0:09:16)
```

Phase 127:

```text
post-Phase 126 capability priority audit
remaining operation-query pressure comparison
H(nu_5) / H(sigma_11) / Delta(sigma_11) deferred
Delta(nu_prime) deferred
E(nu_prime) kept for semantics audit
E(nu_5 o eta_8) selected as the next minimum capability
```

Phase 128:

```text
E(nu_5 o eta_8) theorem-specific handoff
direct lookup first
exact two-generator composition guard
Toda Proposition 5.8 provenance reuse
standard.toda.prop58 root restriction
duplicate specialized match elimination
query-proof replay
repository non-mutation
```

Phase 128 focused regression:

```text
40 passed in 15.43s
```

Phase 128 final regression:

```text
9256 passed in 570.10s (0:09:30)
```

---

# 3. 現在の Web / CLI execution semantics

`explore-applicable` は read-only。

`execute` は既存 qualified execution workflow を利用する。

状態:

```text
NONE
→ no executable target

AMBIGUOUS
→ candidate list
→ explicit user selection

EXECUTED
→ Result + Proof
```

現在の executable-target inclusion:

```text
generator occurrence
→ proof-scope relevance

source-step rule match
→ applicability relevance

qualified family が実際に利用する source component と
generator occurrence が対応
→ executable relevance
```

代表例:

```text
nu_prime
→ 2 executable targets

nu_5
→ NONE

sigma_11
→ NONE

eta_999
→ NONE
```

`NONE` は現在 admitted された qualified execution path に executable target がないことを表し、数学的 impossibility を意味しない。

---

# 4. 現在の operation-query handoff semantics

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
→ Toda Proposition 5.6 symbolic stable bridge

E(sigma_11)
→ E(sigma_11)=sigma_12
→ Toda sigma-family definition

E(nu_5 o eta_8)
→ E(nu_5 eta_8)=0
→ Toda Proposition 5.8 derived pi_10^6=0 provenance
```

Phase 128 の `E(nu_5 o eta_8)` は、

```text
query operand exactly nu_5 o eta_8
root exactly standard.toda.prop58
derived pi_10^6=0
direct premise includes pi_9^5=Z/2{nu_5 eta_8}
```

を要求する。

```text
theorem-specific zero handoff
!= general E evaluator
!= general target-zero evaluator
```

---

# 5. Phase 128 完了境界

```text
direct lookup first を維持
repository 非破壊
Prop.5.8 provenance を維持
query-proof replay を維持
E(nu_5) / E(sigma_11) handoff を維持
parser を変更しない
Web に別 semantics を作らない
general E evaluator を追加しない
general target-zero rule を追加しない
new theorem root を追加しない
qualified family を追加しない
ranking を追加しない
```

Phase 128 は完了。

---

# 6. Phase 129: `E(nu_prime)` operation-result semantics audit

Phase 127 で `E(nu_prime)` は implementation candidate として KEEP したが、Phase 128 より先には実装しなかった。

既存 repository には

\[
E\nu'
\]

が

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}
\]

の generator として既に存在する。

一方、現行 operation query が通常返すのは、

```text
E(alpha)=beta
E(alpha)=0
```

のような element-level `Relation` である。

Phase 129 はまず次を監査する。

```text
1. E nu' の current proof-scope representation
2. E(nu_prime) に対する user-facing result の自然な形
3. membership / group decomposition を operation result とみなすべきか
4. element-level Relation を作るなら既存 provenance だけで十分か
5. containment semantics の一般化なしに exact handoff できるか
```

Phase 129 で先取りしないもの:

```text
general E evaluator
arbitrary expression containment → operation result
general membership evaluator
general target-zero evaluator
parser expansion
new theorem root
new qualified execution family
ranking
```

Phase 129 の判断順:

```text
current representation
→ desired result semantics
→ provenance audit
→ minimum missing capability
→ implementation scope freeze or DEFER
```

---

# 7. 残存数学 pressure

Phase 127 の監査結果を維持する。

```text
H(nu_5)
→ DEFER
→ element-level H proof が不足

Delta(nu_prime)
→ DEFER
→ element-level Delta proof が不足

H(sigma_11)
→ DEFER
→ sigma_11 への Hopf transport が不足

Delta(sigma_11)
→ DEFER
→ element-level Delta proof / concrete window が不足

E(nu_prime)
→ KEEP
→ Phase 129 semantics audit

E(nu_5 o eta_8)
→ Phase 128 で完了
```

今後も

```text
実利用
→ pressure
→ existing mathematics reuse audit
→ minimum missing capability
```

の順で扱う。

---

# 8. 長期保留

```text
semantic theorem ranking
semantic executable-target ranking
automatic best-target selection
general premise-component dependency engine
general operation-query grammar
general E/H/Delta evaluator
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

# 9. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
Web UI から数学 semantics を変更しない
CLI と Web の数学結果を分岐させない
read-only と execution の境界を明示する
proof-scope relevance と executable relevance を混同しない
aggregate statement の同居だけで executable source とみなさない
candidate number を theorem priority と解釈しない
theorem-specific handoff を general evaluator に拡張しない
focused regression で境界を固定する
CLI / browser manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
