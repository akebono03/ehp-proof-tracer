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

## Web operation query

```text
browser query
→ Flask route
→ web_operation_query
→ existing operation-query facade
→ existing structured presentation
→ statement_latex
→ Jinja
→ KaTeX
```

## query-proof

```text
selected fact
→ primary existing provenance
→ existing ProofStep
→ bounded ancestry
→ replay presentation
→ CLI / Web
```

Web では fact を明示選択し、複数 fact の最初を自動選択しない。

---

# 3. 主要モジュール

Web:

```text
web_app.py
web_group_query.py
web_operation_query.py
web_operation_query_proof.py
templates/index.html
static/web_math.js
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

renderer、facade、CLI、Web adapter、Flask route、表示 grouping は独立した定理事実を追加しない。

---

# 5. Repository 非破壊

Phase 113 の TodaGroupQuery specialization、Phase 114 の `E(nu_5)` handoff、Phase 115 の `E(sigma_11)` handoff は元 repository に root を追加しない。

Phase 117–118 の Web UI も repository を変更しない。

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

Web は Phase 118 の usability boundary として

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

---

# 9. 表示と deduplication

同一数学 statement が複数 proof-scope path から得られる場合、表示 layer は grouping できる。

```text
deduplicated presentation
!= provenance deletion
```

複数 statement がある場合:

```text
全 fact を表示
→ 自動選択しない
→ 利用者が明示選択
```

proof replay の root は選択された query fact 自身の `ProofStep` である。

---

# 10. Safe statement presentation

proof replay の statement が既存 renderer で数式化できる場合は LaTeX を使う。

未対応 aggregate statement は type-name fallback へ落とす。

```text
safe fallback
!= raw dataclass repr
!= 推測した定理説明
```

---

# 11. Web UI の設計境界

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

Phase 118 で operation query / query-proof まで接続されたが、新しい数学 engine は導入していない。

---

# 12. Web view model

group query:

```text
n
k
status
result_latex
```

operation query:

```text
query_input
found
items[]
  statement_latex
  provenance_count
```

operation query proof:

```text
query_input
fact_number
conclusion_latex
provenance
steps[]
max_depth
```

Web view model は presentation 用であり、proof truth の保存場所ではない。

---

# 13. TeX / HTML boundary

Python renderer は LaTeX string を返す。

Jinja が `data-latex` へ渡し、`static/web_math.js` が全 `[data-latex]` 要素を取得して `katex.render(...)` を呼ぶ。

設定:

```text
displayMode = true
throwOnError = false
```

---

# 14. Phase 118 regression boundary

Phase 118 で固定した境界:

```text
Web operation query = existing operation-query result
existing statement_latex を再利用
複数 fact は自動選択しない
selected fact 自身を replay root にする
provenance を保持
depth 0 / 1 / 2 を Web から選択可能
unsupported statement は safe type-name fallback
raw Python repr を browser に漏らさない
KaTeX は全 [data-latex] 要素を描画
group-query path を壊さない
repository / proof semantics を変更しない
```

最終 repository-wide regression:

```text
9169 passed in 465.97s (0:07:45)
```

---

# 15. Phase 118 で行わなかったこと

```text
new query grammar
general E/H/Delta evaluator
general Toda bracket solver
coset / indeterminacy computation
new theorem root
arbitrary inference fallback
show-proof Web integration
explore Web integration
execute Web integration
proof graph visualization
REST API
database
authentication
deployment automation
SPA framework
```

---

# 16. 次 Phase との境界

Phase 119 は、次に Web 接続する価値が高い既存 capability を再監査する。

候補:

```text
show-proof
explore
explore-proof
explore-applicable
execute
```

特に `execute` は候補選択と実行 semantics を含むため、read-only capability と同じ感覚で Web に露出しない。

---

# 17. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
Web UI から数学 semantics を変更しない
CLI と Web の数学結果を分岐させない
focused regression で境界を固定する
repository-wide regression で Phase を閉じる
```
