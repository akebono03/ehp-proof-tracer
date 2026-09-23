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
HTML validation != 数学的 domain validation
proof depth control != 新しい proof search
safe fallback != 推測した数学的説明
generator proof Web adapter != 新しい proof engine
generator exploration Web adapter != 新しい repository semantics
generator proof-scope Web adapter != 新しい proof-scope semantics
generator applicability Web adapter != 新しい applicability semantics
Web grouping != 新しい occurrence classification
Web 表示制限 != applicability result の切り捨て
show-proof != execute
explore != explore-proof
explore-proof != explore-applicable
explore-applicable != candidate selection
explore-applicable != execute
explore != execute
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

## Web group query

```text
browser form
→ Flask route
→ web_group_query
→ build_standard_toda_report(n,k)
→ structured group presentation
→ existing LaTeX renderer
→ Jinja
→ KaTeX
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
→ explore_standard_repository_generator_applicability_input(...)
→ RepositoryGeneratorApplicabilityExplorationResult
→ build_repository_generator_applicability_presentation(...)
→ RepositoryGeneratorApplicabilityPresentation
→ thin Web applicability adapter
→ compact Web view
→ Jinja
→ KaTeX
```

重要:

```text
Web adapter は候補探索を行わない
Web adapter は source classification を再実装しない
Web adapter は relevance ordering を再実装しない
Web adapter は candidate を選択しない
Web adapter は execute しない
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

generator exploration:

```text
repository_element_lookup.py
repository_element_exploration.py
repository_element_presentation.py
repository_element_renderer.py
repository_element_facade.py
web_generator_exploration.py
```

generator proof-scope exploration:

```text
repository_proof_scope.py
repository_proof_scope_exploration.py
repository_proof_scope_facade.py
repository_proof_scope_renderer.py
repository_symbolic_sigma_specialization.py
web_generator_proof_scope.py
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

renderer、facade、CLI、Web adapter、Flask route、表示 grouping、表示件数制限は独立した定理事実を追加しない。

Phase 123 の `web_generator_applicability.py` は既存 `RepositoryGeneratorApplicabilityPresentation` を Web 用 immutable view に射影するだけである。

```text
applicability candidate
!= proof
!= selected theorem application
!= executed result
```

---

# 5. Repository 非破壊

Phase 113 の TodaGroupQuery specialization、Phase 114 の `E(nu_5)` handoff、Phase 115 の `E(sigma_11)` handoff は元 repository に root を追加しない。

Phase 117–123 の Web UI 接続も repository を変更しない。

```text
explore
explore-proof
explore-applicable
```

はいずれも read-only であり、Phase 123 の Web route も repository-nonmutating である。

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

generator exploration、generator proof-scope exploration、generator applicability exploration は proof replay ではないため、Web 独自の proof depth selector を持たない。

proof-scope の `shortest_depth` は既存探索結果の metadata である。

---

# 9. 表示と deduplication / truncation

同一数学 statement が複数 proof-scope path から得られる場合、表示 layer は grouping できる。

```text
deduplicated presentation
!= provenance deletion
```

Phase 123 では browser-scale result volume に対して、underlying applicability result を変更せず、HTML へ射影する件数だけを制限する。

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

表示制限は candidate identity、source grouping、relevance ordering、repository、proof provenance を変更しない。

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

`eta_999` の zero result は normal result であり not-found error ではない。

---

# 11. Generator proof-scope exploration の意味論

`explore-proof` は standard production repository から recursive proof scope を構築し、その scope に対して既存の generator specialization を適用する。

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

zero result は normal result である。

---

# 12. Generator applicability exploration の意味論

`explore-applicable` は既存 proof-scope 内の source statement に対して、既存 applicability catalog から候補を列挙する read-only capability である。

構造:

```text
RepositoryGeneratorApplicabilityExplorationResult
  proof_scope_exploration
  candidates

RepositoryGeneratorApplicabilityPresentation
  source_groups
  toda_membership_source_groups
  map_relation_source_groups
  other_source_groups
  rule_group_count
  rule_family_count
```

source group:

```text
scope_node
source_statement
candidates
rule_groups
rule_families
```

rule family:

```text
name
catalog entries
raw candidate count
```

Web は既存 `source_group.rule_families` を利用するため、既存 relevance ordering を維持する。

Web は Phase 123 で relevance category label 自体を新しい public field として公開しない。

### `nu_prime`

Phase 123 browser result:

```text
Proof-scope occurrences: 626
Applicability candidates: 176616
Source statements with candidates: 542
Rule groups: 123300
Rule families: 29308
```

source categories:

```text
Toda memberships: 46
Map relations: 44
Other statements: 452
```

### `sigma_11`

```text
Proof-scope occurrences: 1
Applicability candidates: 686
Source statements with candidates: 1
Rule groups: 472
Rule families: 112
```

source statement:

\[
\pi_{18}^{11}
=
\mathbb Z/16\{\sigma_{11}\}.
\]

### `eta_999`

```text
Proof-scope occurrences: 0
Applicability candidates: 0
Source statements with candidates: 0
Rule groups: 0
Rule families: 0
```

これは normal zero result である。

重要な境界:

```text
explore-applicable
!= candidate selection
!= qualified execution
!= execute
```

---

# 13. Safe statement presentation

既存 renderer で数式化できる statement は LaTeX を使う。

未対応 aggregate statement は type-name fallback へ落とす。

```text
safe fallback
!= raw dataclass repr
!= 推測した定理説明
```

Phase 123 の applicability source も `render_repository_conclusion_latex()` を利用し、`TypeError` / `ValueError` の場合だけ type-name fallback を使う。

---

# 14. Web UI の設計境界

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

Phase 123 までに、

```text
group query
operation query
operation query-proof
generator show-proof
generator explore
generator explore-proof
generator explore-applicable
```

を接続した。

新しい数学 engine は導入していない。

---

# 15. Web view model

generator applicability rule family:

```text
name
catalog_entry_count
raw_candidate_count
```

generator applicability source:

```text
statement_latex | fallback_type_name
root_key
depth
source_statement_type
raw_candidate_count
rule_family_count
rule_families[]
```

generator applicability:

```text
generator_input
generator_latex
occurrence_count
candidate_count
source_count
rule_group_count
rule_family_count
toda_memberships[]
map_relations[]
other_sources[]
```

意図的に Web view へ含めないもの:

```text
candidate identity
candidate selector
fixed_point_safe
premise indexes
bindings
public relevance-category field
qualified execution state
execute action
```

Web view model は presentation 用であり、proof truth の保存場所ではない。

---

# 16. TeX / HTML boundary

Python renderer は LaTeX string を返す。

Jinja が `data-latex` へ渡し、`static/web_math.js` が全 `[data-latex]` 要素を取得して `katex.render(...)` を呼ぶ。

設定:

```text
displayMode = true
throwOnError = false
```

Phase 123 の applicability generator / source statement も同じ `[data-latex]` 境界を使う。

---

# 17. Phase 123 regression boundary

Phase 123 で固定した境界:

```text
explore-applicable Web = existing applicability exploration + presentation
CLI Markdown は解析しない
source classification を Web で再実装しない
relevance ordering を Web で再実装しない
candidate selection を追加しない
execute を追加しない
detailed Web toggle を追加しない
unknown indexed generator の zero result は正常結果
full summary counts を保持する
browser 描画 source は各 category 最大 5
browser 描画 rule family は各 source 最大 10
rule-family details は初期折りたたみ
omitted counts を明示する
表示制限は underlying result semantics を変更しない
既存 group / operation / proof / explore / explore-proof Web path を壊さない
repository / proof semantics を変更しない
```

Phase 123-4 focused tests:

```text
13 passed in 61.24s
```

Phase 123-5A focused regression:

```text
17 passed in 69.57s
```

browser/manual integration:

```text
nu_prime
→ full summary counts preserved
→ category source limit verified
→ rule-family limit / folding verified

sigma_11
→ 1 source
→ pi_18^11 = Z/16{sigma_11}
→ compact rule-family display verified

eta_999
→ 0 / 0 / 0 / 0 / 0
→ normal result
```

最終 repository-wide regression:

```text
9229 passed in 509.16s (0:08:29)
```

---

# 18. Phase 123 で行わなかったこと

```text
new mathematical theorem
new proof-search rule
new qualified execution family
new query grammar
general E/H/Delta evaluator
general Toda bracket solver
coset / indeterminacy computation
candidate selection Web UI
execute Web integration
detailed applicability Web toggle
candidate identity exposure as an action
proof graph visualization
REST API
database
authentication
deployment automation
SPA framework
```

---

# 19. 次 Phase との境界

Phase 123 で、優先していた read-only Web capability の接続は一通り完了した。

次は `execute` を直ちに Web 化せず、Phase 124 で次を監査する。

```text
execute Web integration readiness
candidate selection / ambiguity / status presentation
現在の単一ページ Web UI の情報量
Web UI organization / usability cleanup の優先度
```

Phase 124 は監査を先に行い、必要なら次の1 capability または1 UI 整理だけを選ぶ。

---

# 20. 完了判断原則

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
browser-scale result volume を実測する
focused regression で境界を固定する
browser/manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
