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
group query
operation query
query-proof
generator show-proof
generator explore
generator explore-proof
generator explore-applicable
```

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

# 4. Phase 123 完了境界

```text
generator を browser から applicability exploration へ入力できる
existing applicability facade / presentation を使う
CLI Markdown を解析しない
source grouping を Web で再実装しない
rule-family relevance ordering を Web で再実装しない
candidate selection を追加しない
execute を追加しない
detailed toggle を追加しない
unknown indexed generator の 0 result を正常結果として扱う
full summary counts を保持する
HTML 生成量を bounded にする
group query を壊さない
operation query / query-proof を壊さない
generator proof を壊さない
generator direct explore を壊さない
generator proof-scope explore を壊さない
browser KaTeX path を維持する
focused regression が通る
repository-wide pytest が通る
```

Phase 123 は完了。

---

# 5. Phase 124: next-capability / Web usability audit

Phase 123 で read-only Web capability の優先接続は一通り完了した。

Phase 124 は、次に何を実装するかを先に監査する。

候補:

```text
A. execute Web integration
B. current single-page Web UI organization / usability cleanup
```

## A. execute Web integration の監査観点

現在の user execution workflow:

```text
generator
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ candidate selection
→ qualified execution
→ proof result
```

Web 化には少なくとも、

```text
candidate selection UI
ambiguity handling
execution status presentation
qualified target identity
proof result presentation
existing execution semantics の非変更
```

が必要。

したがって read-only `explore-applicable` の延長として自動的に接続しない。

## B. Web UI cleanup の監査観点

現在の単一ページには複数の独立フォームがある。

```text
group query
operation query
generator proof
generator exploration
generator proof-scope exploration
generator applicability exploration
```

Phase 124 では、

```text
navigation / section organization
default visibility
long result placement
form discoverability
read-only exploration と execution の視覚的分離
```

を監査し、UI cleanup が execute より先かを判断する。

Phase 124 は監査を先に行い、将来 Phase の機能を先取りしない。

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
