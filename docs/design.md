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
proof-scope relevance != executable relevance
applicability relevance != executable relevance
aggregate statement 内の別 branch occurrence != executable source relevance
既知関係の発見 != 写像評価
適用可能候補 != 証明成功
候補番号 != 数学的優先度
operation query != general evaluator
limited theorem-specific handoff != general query inference
target group zero specialization != general zero-target evaluator
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
executable relevance filtering != theorem ranking
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
E(nu_5 o eta_8)
```

それぞれ

\[
E(\nu_5)=\nu_6,
\]

\[
E(\sigma_{11})=\sigma_{12},
\]

\[
E(\nu_5\eta_8)=0
\]

を返す。

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
→ standard applicability exploration
→ qualified-family grouping
→ executable relevance guard
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ candidate number selection when required
→ existing qualified execution
→ executed ProofStep
→ existing structured execution presentation
→ CLI / Web
```

重要:

```text
proof-scope relevance は broad のまま維持する
applicability relevance は broad のまま維持する
execute だけ executable relevance を追加で要求する
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
repository_nu5_stable_bridge_specialization.py
repository_sigma11_suspension_specialization.py
repository_nu5_eta8_suspension_zero_specialization.py
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

executable relevance guard
!= theorem ranking
!= new theorem fact

theorem-specific operation handoff
!= independent theorem root

Web execution result
= existing execution workflow が返した既存の executed ProofStep の presentation
```

---

# 5. Repository 非破壊

Phase 113 の TodaGroupQuery specialization、Phase 114 の `E(nu_5)` handoff、Phase 115 の `E(sigma_11)` handoff、Phase 128 の `E(nu_5 o eta_8)` handoff は元 repository に独立 root を追加しない。

Phase 117–125 の Web UI 接続も repository を変更しない。

Phase 126 の executable relevance 修正も repository の `ProofStep` や theorem root を変更せず、user-facing executable-target inclusion だけを狭める。

Phase 128 の handoff も query ごとに一時的な specialized `ProofStep` を組み立てるだけで、`ProofRepository.entries()` を変更しない。

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

Phase 125 の Web execution は既存 qualified execution path を利用する。

Phase 126 では resolver の target inclusion semantics を修正したが、Web adapter、proof-scope exploration、applicability exploration、qualified family admission 自体は変更していない。

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
E(\sigma_{11})=\sigma_{12},
\]

\[
E(\nu_5\eta_8)=0.
\]

`E(nu_5 o eta_8)` handoff は、query operand が exactly `nu_5 o eta_8` であることを要求する。

さらに、`standard.toda.prop58` の proof-scope 内で、

\[
\pi_{10}^6=0
\]

が `ProofRule.INFERENCE` として存在し、その直接 premise に

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}
\]

があることを要求する。

これにより、

```text
E(nu_5 o eta_8)
→ allowed

E(nu_5 o eta_9)
E(nu_6 o eta_8)
H(nu_5 o eta_8)
Delta(nu_5 o eta_8)
→ handoff 対象外
```

を維持する。

同じ Prop.5.8 proof ancestry が後続 root の proof-scope にも現れるため、Phase 128-2b では `standard.toda.prop58` root に限定し、同一 specialized conclusion を dedup する。

```text
LOOKUP_MISS
!= mathematical unknown
!= evaluator required

limited handoff
!= arbitrary inference fallback
!= general E evaluator

pi_10^6 = 0 を使う今回の specialization
!= 任意の target-zero group から E(x)=0 を生成する一般規則
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

Phase 128 は parser を変更していない。

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

Phase 128 の

```text
query-proof "E(nu_5 o eta_8)" --depth 2
```

は、

\[
E(\nu_5\eta_8)=0
\]

から既存の

\[
\pi_{10}^6=0
\]

およびその直接 premise を再生する。

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

proof-scope generator occurrence は `RepositoryProofScopeGeneratorOccurrence.path` を保持する。

aggregate statement ではこの path により、

```text
pi6_3_group_relation
pi7_4_group_relation
pi8_5_group_relation
```

などの branch を区別できる。

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

generator が source ProofStep のどこかに出現
!=
その generator が qualified rule の実使用 component に対応
```

Phase 126 でも applicability discovery 自体は変更していない。

---

# 13. Generator execution の意味論

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
→ CLI / Web 表示
```

Phase 126 以降の executable target inclusion は次の3層を区別する。

```text
1. proof-scope relevance
   generator が ProofStep のどこかに出現する

2. applicability relevance
   その ProofStep が rule premise として適用可能である

3. executable relevance
   入力 generator occurrence が、
   qualified rule が実際に利用する source component に対応する
```

1 と 2 は broad のまま維持する。

3 だけを user-facing executable target resolution で追加要求する。

```text
proof-scope relevance
!= executable relevance

applicability relevance
!= executable relevance

same aggregate ProofStep
!= same mathematical source component
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

Phase 126 は candidate ordering や ranking を変更していない。

---

# 15. Phase 126 executable relevance semantics

Phase 125 browser/manual audit では `nu_5` の Web / CLI execution が

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
\]

へ到達した。

Phase 126-1 から 126-3 の監査で、原因は Web adapter ではなく resolver の broad source semantics にあることを確認した。

Toda Proposition 5.6 aggregate は少なくとも、

\[
\pi_6^3=\mathbb Z/4\{\nu'\},
\]

\[
\pi_7^4=\mathbb Z\{\nu_4\}\oplus\mathbb Z/4\{E\nu'\},
\]

\[
\pi_8^5=\mathbb Z/8\{\nu_5\}
\]

を同じ `ProofStep` conclusion に保持する。

旧 semantics では `nu_5` が `pi8_5_group_relation` に出現するだけで Prop. 5.6 全体が generator-relevant source となり、第2 qualified family

```text
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

が同じ aggregate の別 branch `pi6_3_group_relation` を利用していても executable target に含まれた。

Phase 126-4 はこの第2 family に限り、

```text
入力 generator occurrence
→ source_step identity 一致
→ occurrence.path の先頭 branch が pi6_3_group_relation
```

を executable relevance guard として要求する。

結果:

```text
nu_prime
→ pi6_3_group_relation に occurrence
→ 第2 family を維持

nu_5
→ pi8_5_group_relation に occurrence
→ 第2 family から除外

sigma_11
→ admitted qualified family なし
→ NONE を維持
```

第1 qualified family

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

は aggregate Prop. 5.6 ではなく既存の \(\pi_7^4\) relation を直接 source としているため、Phase 126-4 では追加 branch guard を入れていない。

この修正は current admitted families に対する最小修正である。

```text
executable relevance guard
!= general premise-component dependency engine
!= theorem ranking
!= target scoring
!= automatic best-target selection
```

---

# 16. Phase 127 capability priority audit

Phase 127 は新機能を追加せず、Phase 126 後の実利用 pressure を監査した。

監査した operation pressure:

```text
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
E(nu_5 o eta_8)
```

分類:

```text
H(nu_5)
→ element-level H proof 自体が不足
→ DEFER

H(sigma_11)
→ sigma_8 の Hopf relation はあるが sigma_11 transport なし
→ DEFER

Delta(sigma_11)
→ element-level Delta proof / concrete window が不足
→ DEFER

Delta(nu_prime)
→ element-level Delta proof が不足
→ DEFER

E(nu_prime)
→ E nu' expression / provenance は既存
→ operation-result semantics の整理が必要
→ KEEP

E(nu_5 o eta_8)
→ source generator と pi_10^6=0 provenance が既存
→ result semantics は明確に zero
→ KEEP
```

Phase 127-4 では、既存 semantics への適合と変更量の小ささから

\[
E(\nu_5\eta_8)=0
\]

を Phase 128 の1機能に選定した。

---

# 17. Phase 128 `E(nu_5 o eta_8)` theorem-specific handoff

Phase 128 は、

```text
query "E(nu_5 o eta_8)"
```

の direct lookup が miss した場合だけ、

\[
E(\nu_5\eta_8)=0
\]

を返す限定 handoff を追加した。

根拠は既存 Toda Proposition 5.8 proof-scope の

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\]

および derived

\[
\pi_{10}^6=0
\]

である。

`pi_10^6=0` は `ProofRule.INFERENCE` であり、その直接 premise は既存の

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\]

suspension surjectivity、および

\[
\nu_6\eta_9=0
\]

を含む。

specialized root:

\[
E(\nu_5\eta_8)=0
\]

は `ProofRule.INFERENCE` とし、直接 premise に既存 `pi_10^6=0` step を保持する。

したがって depth 2 の query-proof は、

```text
Depth 0:
E(nu_5 eta_8) = 0

Depth 1:
pi_10^6 = 0

Depth 2:
pi_9^5 = Z/2{nu_5 eta_8}
E: pi_9^5 -> pi_10^6 is surjective
nu_6 eta_9 = 0
```

を再生できる。

複数 standard root から同じ Prop.5.8 ancestry が見えるため、handoff は

```text
root_entry.key == "standard.toda.prop58"
```

に限定し、同一 specialized conclusion を dedup する。

これは theorem-specific provenance selection であり、theorem ranking ではない。

---

# 18. Safe statement presentation

既存 renderer で数式化できる statement は LaTeX を使う。

未対応 aggregate statement は type-name fallback へ落とす。

```text
safe fallback
!= raw dataclass repr
!= 推測した定理説明
```

executed premise 表示もこの境界を維持する。

---

# 19. Web UI の設計境界

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

Phase 126 の resolver 修正は CLI / Web の共通 execution facade より下層にあるため、CLI と Web で別 semantics を持たない。

Phase 128 も既存 operation-query facade に handoff を追加しただけなので、CLI / Web は同じ結果を利用する。

---

# 20. Web execution view model

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

# 21. TeX / HTML boundary

Python renderer は LaTeX string を返す。

Jinja が `data-latex` へ渡し、`static/web_math.js` が `[data-latex]` 要素を取得して `katex.render(...)` を呼ぶ。

設定:

```text
displayMode = true
throwOnError = false
```

execution candidate / result / conclusion も同じ境界を使う。

---

# 22. Phase 128 regression boundary

Phase 128 focused regression:

```text
tests/test_phase128_nu5_eta8_operation_query_handoff.py
tests/test_phase114_3_nu5_operation_query_handoff.py
tests/test_phase115_sigma11_operation_query_handoff.py

40 passed in 15.43s
```

CLI manual audit:

```text
python main.py query "E(nu_5 o eta_8)"
→ 1. E nu_5 eta_8 = 0
→ First provenance: Toda Proposition 5.8, Phase 68

python main.py query-proof "E(nu_5 o eta_8)" --depth 2
→ specialized root + existing Prop.5.8 ancestry
```

最終 repository-wide regression:

```text
python -m pytest -q
9256 passed in 570.10s (0:09:30)
```

Phase 128 完了境界:

```text
direct lookup first を維持
exact query guard を維持
standard.toda.prop58 provenance に限定
repository 非破壊
query-proof replay を維持
E(nu_5) / E(sigma_11) handoff を維持
parser を変更しない
general E evaluator を追加しない
general target-zero specialization を追加しない
new theorem root を追加しない
qualified execution family を追加しない
ranking を追加しない
```

---

# 23. Phase 128 で行わなかったこと

```text
E(nu_prime) operation-result semantics の決定
H(nu_5) の新規数学 proof
H(sigma_11) の transport
Delta(nu_prime) の新規数学 proof
Delta(sigma_11) の新規数学 proof
new proof-search rule
new qualified execution family
new query grammar
general E/H/Delta evaluator
general target-zero evaluator
general Toda bracket solver
general premise-component dependency engine
coset / indeterminacy computation
candidate ranking
semantic target ranking
automatic best-target selection
proof graph visualization
REST API
database
authentication
deployment automation
SPA framework
```

---

# 24. 次 Phase との境界

次 Phase 129 は `E(nu_prime)` の operation-result semantics を audit first で扱う。

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

の generator として存在する。

しかし、

```text
E(nu_prime)
```

に対して

```text
E(nu_prime) = E nu'
```

をそのまま operation fact とするのか、

```text
E nu' ∈ pi_7^4
```

の membership を示すのか、group decomposition まで提示するのかは別の意味論判断である。

Phase 129 は実装前に、

```text
existing representation
→ desired user-facing result
→ provenance shape
→ minimum handoff or no implementation
```

を確定する。

一般 evaluator や containment-based arbitrary operation result へ広げない。

---

# 25. 完了判断原則

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
proof-scope relevance と executable relevance を混同しない
aggregate statement の同居だけで executable source とみなさない
candidate number を theorem priority と解釈しない
execution target の違和感を Web 層で補正しない
theorem-specific handoff を一般 evaluator に拡張しない
focused regression で境界を固定する
CLI / browser manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
