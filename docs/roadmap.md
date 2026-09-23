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
```

`query-proof` は operation query の selected fact から利用できる。

generator explore-applicable:

```text
generator input
→ thin Web generator-applicability adapter
→ existing applicability facade
→ existing RepositoryGeneratorApplicabilityPresentation
→ compact source / rule-family Web view
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
explore-applicable != execute
Web truncation != applicability-result truncation
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
web_generator_applicability thin adapter
existing applicability facade / presentation reuse
source category + rule-family display
normal zero-result handling
browser-scale display-volume audit
source / rule-family output limits
browser/manual re-audit
```

Phase 123 focused implementation:

```text
13 passed in 61.24s
```

Phase 123 compact-volume focused regression:

```text
17 passed in 69.57s
```

Phase 123 final regression:

```text
9229 passed in 509.16s (0:08:29)
```

Phase 124:

```text
execute Web integration readiness vs Web UI usability audit
Web UI organization を先に選定
single-page structure を維持
workflow navigation を追加
既存 six form section へ anchor target を追加
web_app.py は変更しない
execute / candidate selection は追加しない
browser/manual integration audit
```

Phase 124 focused:

```text
5 passed in 3.83s
38 passed in 44.51s
```

Phase 124 final regression:

```text
9234 passed in 522.10s (0:08:42)
```

---

# 3. 現在の Web UI

起動:

```text
python -m flask --app web_app run --debug
```

read-only capability:

```text
group query
operation query
query-proof
generator show-proof
generator explore
generator explore-proof
generator explore-applicable
```

`explore-applicable` Web summary:

```text
generator
proof-scope occurrences
applicability candidates
source statements with candidates
rule groups
rule families
```

source category:

```text
Toda memberships
Map relations
Other statements
```

displayed source metadata:

```text
statement LaTeX or safe type fallback
root
depth
source statement type
raw candidates
rule-family count
```

displayed rule-family metadata:

```text
rule name
catalog-entry count
raw-candidate count
```

browser-volume boundary:

```text
max 5 sources per category
max 10 rule families per displayed source
rule-family details collapsed by default
full aggregate counts preserved
omitted counts displayed
```

代表例:

```text
nu_prime
→ 626 proof-scope occurrences
→ 176616 applicability candidates
→ 542 source statements
→ 123300 rule groups
→ 29308 rule families

sigma_11
→ 1 proof-scope occurrence
→ 686 applicability candidates
→ 1 source
→ 472 rule groups
→ 112 rule families

eta_999
→ 0 / 0 / 0 / 0 / 0
```

---

# 4. Phase 124 完了境界

```text
Phase 123 の read-only Web capability を維持する
current single-page Web UI を維持する
existing six forms を削除・統合しない
上部 workflow navigation を追加する
既存 section へ anchor link する
route を増やさない
web_app.py を変更しない
Web adapter を増やさない
candidate selection を追加しない
execute を追加しない
qualified execution semantics を変更しない
applicability semantics を変更しない
compact Web output limits を維持する
KaTeX path を維持する
focused regression が通る
browser/manual integration audit が通る
repository-wide pytest が通る
```

Phase 124 は完了。

---

# 5. Phase 125: execute Web integration

Phase 124 で UI organization を先に済ませたため、Phase 125 では既存 `execute` workflow の Web 接続に進む。

現在の user execution workflow:

```text
generator
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ candidate selection
→ qualified execution
→ proof result
→ result + proof presentation
```

Phase 125 で再利用する既存基盤:

```text
repository_generator_user_execution_facade.py
repository_generator_user_execution_candidate_presentation.py
repository_generator_user_execution_presentation.py
repository_generator_user_execution_handoff.py
repository_generator_user_execution_proof_step.py
```

実装方針:

```text
thin Web adapter を追加する
existing execution facade を呼ぶ
NONE を no executable target として表示する
AMBIGUOUS は候補一覧を表示し利用者選択を待つ
EXECUTED は result + proof を表示する
candidate number を theorem ranking と解釈しない
CLI Markdown を解析しない
existing candidate / execution presentation を最大限再利用する
new qualified family を追加しない
new proof-search semantics を追加しない
```

最初に監査する事項:

```text
Web view model に必要な最小 field
candidate selection form の round-trip
candidate number validation
generator input の保持
NONE / AMBIGUOUS / EXECUTED の表示境界
result / proof の KaTeX rendering
既存 Group / Query / Proof / Explore / Applicability との共存
```

Phase 125 では execute の Web 接続だけを扱い、UI 全体の追加 redesign は行わない。

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
general operation-query grammar
general E/H/Delta evaluator
general Toda bracket solver
coset / indeterminacy computation
semantic theorem ranking
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
browser-scale result volume を実測する
focused regression で境界を固定する
browser/manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
