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
→ thin Web execution adapter
→ existing execution facade
→ NONE / AMBIGUOUS / EXECUTED
→ candidate selection when required
→ existing qualified execution
→ Result + Proof
→ KaTeX
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
candidate selection != theorem ranking
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

---

# 3. 現在の Web UI

起動:

```text
python -m flask --app web_app:create_app run
```

capability:

```text
group query
operation query
query-proof
generator show-proof
generator explore
generator explore-proof
generator explore-applicable
generator execute
```

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

代表例:

```text
nu_prime
→ 2 executable targets

eta_999
→ NONE
```

Phase 125 browser/manual audit では `nu_5` の Web 実行結果が既存 CLI と一致することを確認した。

---

# 4. Phase 125 完了境界

```text
existing execution facade を再利用する
existing candidate presentation を再利用する
existing execution presentation を再利用する
CLI Markdown を解析しない
NONE を normal no-target state とする
AMBIGUOUS を自動選択しない
candidate number は 1-based addressing
candidate number != theorem priority
EXECUTED では Result + Proof + provenance を表示する
new qualified family を追加しない
new proof-search semantics を追加しない
generator-to-target resolution semantics を変更しない
existing single-page Web UI を維持する
KaTeX path を維持する
focused regression が通る
browser/manual integration audit が通る
repository-wide pytest が通る
```

Phase 125 は完了。

---

# 5. Phase 126: executable-target resolution semantics audit

Phase 125 で Web execution が利用可能になったことで、既存 target-resolution semantics が利用者から直接見えるようになった。

最初の pressure:

```text
python main.py execute nu_5
```

と Web `nu_5` execution がともに、

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
\]

の既存 qualified execution path へ到達する。

Phase 125 の Web adapter mismatch ではないことは確認済みである。

Phase 126 はこの挙動を**変更する Phase ではなく、まず監査する Phase**とする。

監査対象:

```text
generator occurrence semantics
proof-scope relation
applicability relation
qualified executable target inclusion
target tuple ordering
generator-specific user expectation
CLI / Web consistency
```

確認したい問い:

```text
なぜ nu_5 がこの executable target に含まれるのか
既存 resolver の intended semantics か
generator relation の広さが user-facing execute に適切か
target order は単なる deterministic order か
candidate list に必要な説明 metadata はあるか
```

Phase 126 で先取りしないもの:

```text
semantic target ranking
best-target selection
automatic filtering
new qualified family
new proof-search rule
general evaluator
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
candidate number を theorem priority と解釈しない
利用者違和感はまず resolver semantics を監査する
focused regression で境界を固定する
browser/manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
