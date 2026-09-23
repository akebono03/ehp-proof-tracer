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
E(\sigma_{11})=\sigma_{12}.
\]

基本境界:

```text
direct lookup first
limited theorem-specific handoff != general query inference
query != general evaluator
LOOKUP_MISS != evaluator required
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

# 4. Phase 126 完了境界

```text
proof-scope exploration semantics を維持する
applicability exploration semantics を維持する
qualified execution family admission を維持する
executable target inclusion だけを必要最小限に狭める

nu_prime
→ 2 executable targets を維持

nu_5
→ unrelated pi6_2 target を除外
→ NONE

sigma_11
→ NONE を維持

candidate number
→ 1-based addressing
→ theorem priority ではない

target ranking
→ 追加しない

automatic best-target selection
→ 追加しない

general premise-component dependency engine
→ 追加しない
```

Phase 126 は完了。

---

# 5. Phase 127: post-Phase 126 capability priority audit

Phase 126 で user-facing execute の semantic leak を修正した。

次 Phase は新機能を直ちに追加せず、現在の実利用フローで次に不足する capability を再監査する。

監査候補:

```text
operation query / query-proof の残存 pressure
generator execute の実利用 pressure
Web / CLI workflow の不整合
現在の2 qualified family で不足する具体例
executable relevance guard を別 family / aggregate statement へ一般化する実需要
```

判断順:

```text
actual user workflow
→ concrete pressure
→ existing mathematics / infrastructure reuse audit
→ minimum missing capability
→ Phase scope freeze
```

Phase 127 で先取りしないもの:

```text
general premise-component dependency engine
semantic theorem ranking
semantic executable-target ranking
automatic best-target selection
general evaluator
new qualified family without concrete pressure
```

---

# 6. 数学的 capability pressure

Web UI の発展とは別に、残存数学 pressure を保持する。

```text
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
E(nu_5 o eta_8)
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

# 7. 長期保留

```text
semantic theorem ranking
semantic executable-target ranking
automatic best-target selection
general premise-component dependency engine
general operation-query grammar
general E/H/Delta evaluator
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
Web UI から数学 semantics を変更しない
CLI と Web の数学結果を分岐させない
read-only と execution の境界を明示する
proof-scope relevance と executable relevance を混同しない
aggregate statement の同居だけで executable source とみなさない
candidate number を theorem priority と解釈しない
利用者違和感はまず resolver semantics を監査する
focused regression で境界を固定する
CLI / browser manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
