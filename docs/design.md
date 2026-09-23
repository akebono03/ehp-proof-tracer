# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の**現在有効なアーキテクチャ、意味論、不変条件、設計境界**を記録する。

過去の実装経緯は `docs/development_log.md`、証明記録は `docs/proof_records.md`、今後の計画は `docs/roadmap.md`、コード探索は `docs/code_reference.md` を参照する。

---

# 1. 基本設計原則

```text
実際の数学的・証明探索上の必要
↓
不足している最小表現
↓
必要な領域固有規則 / オーケストレーション
↓
既存の汎用基盤
```

次を混同しない。

```text
表現 != 型付け != 定理知識
構造的等値 != 数学的等値
探索計画 != 証明結果
表示層 != 証明事実
proof-scope 走査 != 定理探索
既知関係の発見 != 写像評価
適用可能候補 != 証明成功
候補番号 != 数学的優先度
operation query != general evaluator
limited theorem-specific handoff != general query inference
Web UI != 新しい数学エンジン
TeX rendering != 数学的 normalization
proof depth control != 新しい proof search
safe fallback != 推測した数学的説明
generator exploration Web adapter != 新しい repository semantics
generator proof-scope Web adapter != 新しい proof-scope semantics
generator applicability Web adapter != 新しい applicability semantics
generator execution Web adapter != 新しい execution semantics
Web grouping != 新しい occurrence classification
Web 表示制限 != applicability result の切り捨て
Workflow navigation != 新しい capability
Workflow anchor != 新しい route
UI organization != execution semantics
show-proof != execute
explore != explore-proof
explore-proof != explore-applicable
explore-applicable != candidate selection
explore-applicable != execute
candidate selection != theorem ranking
Web execution != second execution engine
```

---

# 2. 現在の主要経路

## Toda group calculation

```text
ProofRepository
→ TodaGroupQuery
→ direct group lookup
→ 必要なら限定的 theorem-specific specialization
→ group result
→ proof / EHP provenance
→ structured presentation
→ report
```

## operation query

```text
query string
→ minimal parser
→ direct repository / proof-scope lookup
→ direct hit はそのまま返す
→ direct miss のうち許可された exact handoff のみ具体化
→ structured presentation
→ CLI / Web
```

現在許可される exact handoff:

```text
E(nu_5)
E(sigma_11)
```

## query-proof / generator show-proof

```text
selected existing fact / known-group identity
→ existing ProofStep
→ bounded ancestry
→ replay presentation
→ CLI / Web
```

Web の depth 0 / 1 / 2 は表示範囲であり、新しい proof search ではない。

## generator explore

```text
generator input
→ standard production repository
→ existing direct generator exploration
→ RepositoryGeneratorExplorationPresentation
→ thin Web adapter
→ Jinja
→ KaTeX
```

## generator explore-proof

```text
generator input
→ standard production repository
→ recursive proof scope
→ existing generator specialization
→ RepositoryProofScopeExplorationResult
→ thin Web adapter
→ Jinja
→ KaTeX
```

## generator explore-applicable

```text
generator input
→ existing applicability facade
→ RepositoryGeneratorApplicabilityExplorationResult
→ RepositoryGeneratorApplicabilityPresentation
→ thin Web applicability adapter
→ compact Web view
→ Jinja
→ KaTeX
```

## generator execute

```text
generator input
→ thin Web execution adapter
→ run_standard_repository_generator_user_execution_workflow(...)
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ candidate number selection when required
→ existing qualified execution
→ executed ProofStep
→ existing structured execution presentation
→ Web view
→ Jinja
→ KaTeX
```

重要:

```text
Web adapter は候補探索を再実装しない
Web adapter は source classification を再実装しない
Web adapter は relevance ordering を再実装しない
Web adapter は qualified execution を再実装しない
Web adapter は candidate number を theorem priority と解釈しない
Web adapter は CLI Markdown を解析しない
```

---

# 3. 主要モジュール

Web:

```text
web_app.py
web_group_query.py
web_operation_query.py
web_operation_query_proof.py
web_generator_proof.py
web_generator_exploration.py
web_generator_proof_scope.py
web_generator_applicability.py
web_generator_execution.py
templates/index.html
static/web_math.js
```

generator applicability:

```text
repository_generator_applicability_facade.py
repository_generator_applicability_presentation.py
repository_generator_applicability_renderer.py
repository_proof_scope_applicability.py
standard_production_applicability_catalog.py
web_generator_applicability.py
```

generator execution:

```text
repository_generator_user_execution_resolver.py
repository_generator_user_execution_candidate_presentation.py
repository_generator_user_execution_handoff.py
repository_generator_user_execution_proof_step.py
repository_generator_user_execution_presentation.py
repository_generator_user_execution_facade.py
web_generator_execution.py
```

known-group replay:

```text
repository_generator_known_group_proof_replay.py
repository_generator_known_group_proof_replay_presentation.py
repository_generator_known_group_proof_replay_renderer.py
```

operation query / replay:

```text
repository_operation_query.py
repository_operation_query_lookup.py
repository_operation_query_facade.py
repository_operation_query_presentation.py
repository_operation_query_proof_replay.py
repository_operation_query_proof_replay_presentation.py
repository_operation_query_proof_replay_statement_presentation.py
repository_operation_query_proof_replay_renderer.py
```

CLI:

```text
main.py
```

---

# 4. 証明事実と provenance

証明事実の中心は

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

である。

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata である。

renderer、facade、CLI、Web adapter、Flask route、表示 grouping、表示件数制限、candidate selection form は独立した定理事実を追加しない。

```text
applicability candidate
!= proof
!= selected theorem application
!= executed result

execution candidate number
!= theorem priority

Web execution result
= existing execution workflow が返した既存の executed ProofStep の presentation
```

---

# 5. Repository 非破壊

Phase 113 の TodaGroupQuery specialization、Phase 114 の `E(nu_5)` handoff、Phase 115 の `E(sigma_11)` handoff は元 repository に独立 root を追加しない。

Phase 117–125 の Web UI 接続も repository を変更しない。

read-only:

```text
explore
explore-proof
explore-applicable
```

execution:

```text
execute
```

Phase 125 の Web execution は既存 qualified execution path を利用するが、Web adapter 自体が repository semantics を変更するわけではない。

---

# 6. operation query の意味論

operation query は lookup-first である。

```text
operation query
→ direct existing-fact lookup
→ hit ならそのまま返す
→ miss なら exact handoff guard
→ 許可された場合だけ theorem-specific specialization
```

現在の限定 handoff:

\[
E(\nu_5)=\nu_6,
\]

\[
E(\sigma_{11})=\sigma_{12}.
\]

```text
LOOKUP_MISS
!= mathematical unknown
!= evaluator required

limited handoff
!= arbitrary inference fallback
!= general E evaluator
```

---

# 7. Operation-query parser の境界

現在対応:

```text
二項 top-level composition
三項 top-level composition
E / H の generator operand
E / H の二項 composition operand
Delta の generator operand
```

意図的に未対応:

```text
四項以上
E(a o b o c)
H(a o b o c)
Delta(a o b o c)
Unicode ∘
一般再帰 parser
```

Web UI は既存 parser を再利用し、別 grammar を持たない。

---

# 8. 証明再生

default:

```text
max_depth = 1
```

Web は現在

```text
0
1
2
```

のみを選択可能にする。

```text
depth 0 → root のみ
depth 1 → direct premise まで
depth 2 → さらに1段 ancestry
```

depth は表示範囲であり、新しい proof search ではない。

generator exploration、generator proof-scope exploration、generator applicability exploration は proof replay ではない。

---

# 9. Applicability の表示境界

Phase 123 では underlying applicability result を変更せず、HTML へ射影する件数だけを制限する。

```text
full summary counts
→ 常に保持

各 source category
→ Web では先頭 5 source を描画

各 displayed source
→ Web では先頭 10 rule family を描画

rule-family detail
→ <details> で初期折りたたみ

omitted count
→ 明示表示
```

したがって、

```text
Web 表示件数
!= source_count
!= candidate_count
!= rule_group_count
!= rule_family_count
```

である。

---

# 10. Generator exploration の意味論

`explore` は standard production repository の direct occurrence を調べる。

代表例:

```text
nu_prime
→ 6 direct occurrences

eta_999
→ Occurrences: 0

sigma_11
→ 0 direct standard-repository occurrences
```

zero result は normal result である。

---

# 11. Generator proof-scope exploration の意味論

`explore-proof` は recursive proof scope を構築し、その scope に対して既存の generator specialization を適用する。

代表例:

```text
sigma_11
→ direct explore: 0
→ proof-scope explore: 1

eta_999
→ proof-scope occurrences: 0
→ Toda memberships: 0
→ map relations: 0
```

---

# 12. Generator applicability exploration の意味論

`explore-applicable` は既存 proof-scope 内の source statement に対して、既存 applicability catalog から候補を列挙する read-only capability である。

### `nu_prime`

```text
Proof-scope occurrences: 626
Applicability candidates: 176616
Source statements with candidates: 542
Rule groups: 123300
Rule families: 29308
```

### `sigma_11`

```text
Proof-scope occurrences: 1
Applicability candidates: 686
Source statements with candidates: 1
Rule groups: 472
Rule families: 112
```

### `eta_999`

```text
Proof-scope occurrences: 0
Applicability candidates: 0
Source statements with candidates: 0
Rule groups: 0
Rule families: 0
```

重要な境界:

```text
explore-applicable
!= candidate selection
!= qualified execution
!= execute
```

---

# 13. Generator execution の意味論

Phase 125 は既存の利用者向け execution workflow を Web に接続した。

既存 status:

```text
NONE
AMBIGUOUS
EXECUTED
```

`NONE`:

```text
executable target = 0
→ 正常な no-target state
→ Web はエラーではなく結果として表示
```

`AMBIGUOUS`:

```text
executable target > 1
→ Web は既存 candidate list presentation から候補番号と conclusion を表示
→ candidate を自動選択しない
→ 利用者が 1-based candidate number を選択
```

`EXECUTED`:

```text
selected target
→ existing qualified execution
→ RepositoryGeneratorExecutedProofStepResult
→ RepositoryGeneratorUserExecutionPresentation
→ conclusion / premises / rule
→ root_entry provenance
→ Web 表示
```

Phase 125 の Web adapter は execution workflow の**利用者**であり execution engine ではない。

```text
web_generator_execution.py
!= resolver
!= ranking engine
!= proof-search engine
!= qualified execution engine
```

---

# 14. Candidate selection の境界

candidate number は既存 target tuple の 1-based selection である。

```text
candidate 1
candidate 2
...
```

は UI / workflow 上の addressing であり、

```text
candidate number
!= theorem priority
!= relevance score
!= mathematical preference
!= recommended result
```

である。

`AMBIGUOUS` 時に Web は自動選択しない。

1 target の場合は既存 facade が従来どおり自動実行する。

---

# 15. `nu_5` manual audit の扱い

Phase 125 browser/manual audit では `nu_5` の Web execution が

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
\]

へ到達することを確認した。

CLI の

```text
python main.py execute nu_5
```

も同じ結果を返した。

したがって Phase 125 では、

```text
Web adapter mismatch
```

ではなく、

```text
existing generator → executable target resolution semantics
```

の結果として扱う。

Phase 125 はこの意味論を変更しない。

この挙動が利用者期待に合うかは次 Phase の監査対象である。

---

# 16. Safe statement presentation

既存 renderer で数式化できる statement は LaTeX を使う。

未対応 aggregate statement は type-name fallback へ落とす。

```text
safe fallback
!= raw dataclass repr
!= 推測した定理説明
```

Phase 125 の executed premise 表示もこの境界を維持する。

---

# 17. Web UI の設計境界

framework:

```text
Flask
```

browser TeX renderer:

```text
KaTeX 0.18.7
```

Web は CLI output / Markdown を再解析しない。

```text
existing structured object
→ thin Web adapter
→ Jinja
→ KaTeX
```

現在接続済み:

```text
group query
operation query
operation query-proof
generator show-proof
generator explore
generator explore-proof
generator explore-applicable
generator execute
```

navigation:

```text
Calculation and queries
→ Group query
→ Operation query

Proof and exploration
→ Generator proof
→ Generator exploration
→ Generator proof-scope exploration

Applicability
→ Applicable theorem / lemma candidates
→ Execute theorem / lemma candidate
```

---

# 18. Web execution view model

概念上の最小 field:

```text
generator_input
generator_latex
status
candidates[]
selected_candidate_number
conclusion_latex
premises[]
rule_name
provenance
```

candidate:

```text
candidate_number
conclusion_latex
```

premise:

```text
premise_number
statement_latex | fallback_type_name
```

provenance:

```text
key
theorem
phase
```

Web view model は presentation 用であり、proof truth の保存場所ではない。

---

# 19. TeX / HTML boundary

Python renderer は LaTeX string を返す。

Jinja が `data-latex` へ渡し、`static/web_math.js` が `[data-latex]` 要素を取得して `katex.render(...)` を呼ぶ。

設定:

```text
displayMode = true
throwOnError = false
```

execution candidate / result / conclusion も同じ境界を使う。

---

# 20. Phase 125 regression boundary

Phase 125 で固定した境界:

```text
current single-page Web UI を維持する
既存 Flask route を維持する
既存 execution facade を再利用する
existing candidate / execution presentation を再利用する
CLI Markdown を解析しない
NONE を正常な no-target state とする
AMBIGUOUS を自動選択しない
candidate number を theorem ranking と解釈しない
EXECUTED の result / proof / provenance を表示する
new qualified family を追加しない
new proof-search rule を追加しない
generator-to-target resolution semantics を変更しない
KaTeX path を維持する
```

Phase 125-4 focused tests:

```text
14 passed in 29.80s
```

browser/manual integration:

```text
nu_prime
→ 2 executable candidates
→ candidate 1 / 2 の既存 CLI 対応を確認

eta_999
→ NONE
→ No executable target found for this generator.

nu_5
→ Web と CLI の execution result が一致

KaTeX
→ candidate / result の数式表示を確認

既存 Web capability
→ 共存を確認
```

最終 repository-wide regression:

```text
9243 passed in 555.37s (0:09:15)
```

---

# 21. Phase 125 で行わなかったこと

```text
new mathematical theorem
new proof-search rule
new qualified execution family
new query grammar
general E/H/Delta evaluator
general Toda bracket solver
coset / indeterminacy computation
candidate ranking
semantic target ranking
automatic best-target selection
generator-to-target resolution semantics change
proof graph visualization
REST API
database
authentication
deployment automation
SPA framework
```

---

# 22. 次 Phase との境界

Phase 125 で existing execute workflow の Web integration は完了した。

次 Phase 126 は、Phase 125 manual audit で可視化された executable-target resolution の意味論を監査する。

特に、

```text
generator input
→ proof-scope / applicability relation
→ executable target inclusion
→ target ordering
→ user-facing expectation
```

を確認する。

最初の監査対象:

```text
nu_5
```

重要:

```text
Phase 126 は audit first
```

であり、ranking、filtering、target-selection semantics の変更を先取りしない。

---

# 23. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
Web UI から数学 semantics を変更しない
CLI と Web の数学結果を分岐させない
read-only exploration と execution を混同しない
candidate number を theorem priority と解釈しない
execution target の違和感を Web 層で補正しない
focused regression で境界を固定する
browser/manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
