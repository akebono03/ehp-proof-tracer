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
運用リポジトリの組み立て != 定理事実
証明範囲の走査 != 定理探索
既知関係の発見 != 写像評価
Toda bracket membership の発見 != bracket の解法
適用可能候補 != 証明成功
関連度カテゴリ != 定理順位
引き渡し検証 != 定理事実
実行資格を満たす候補 != 一意な実行対象
実行ファミリーのグループ化 != 生カタログの重複除去
代表候補の選択 != 定理順位付け
一般 qualification != family 固有の実行戦略
family dispatch != 定理順位付け
production application recovery != 任意の companion premise 探索
性能最適化 != 数学的意味論の変更
利用者向け target resolver != 定理順位付け
候補番号 != 数学的優先度
表示 != 証明 object
repository target goal の等値 != 実行済み conclusion の object identity
CLI での指定 != proof graph 内部指定
既知群同一性検索 != qualified execution
既知群の証明再生 != 定理適用実行
symbolic theorem の具体化 != 任意の symbolic AST 書き換え
具体化 provenance != production rule の再実行
演算問い合わせ検索 != 演算 evaluator
重複除去済み表示 != 生 provenance の削除
演算問い合わせの証明再生 != 包含する定理の再生
安全な型 fallback != 推測した数学的説明
```

---

# 2. 現在の主要経路

計算:

```text
式 / statement
→ proof / inference
→ Toda 固有知識
→ ProofRepository / rule catalog
→ bounded search
→ TodaGroupQuery / lookup
→ group result
→ EHP / proof provenance
→ presentation
→ report
```

生成元 / 適用可能性:

```text
生成元文字列
→ GeneratorSymbol
→ 標準運用 repository
→ 再帰的 ProofStep ancestry
→ 生成元固有の proof-scope 具体化
→ 出現
→ Toda membership / 既知の写像関係
→ 前提 pattern 適合性
→ 適用候補
→ 関連度分類済み表示
```

既知群の証明再生:

```text
生成元
→ 既知群同一性
→ source ProofStep
→ 有界な直接 ancestry
→ 再生表示
→ show-proof
```

qualified execution:

```text
生成元
→ 実行可能対象 resolver
→ 候補選択
→ qualified execution 引き渡し
→ 有界実行
→ 実際に実行された ProofStep
→ 結果 + 証明
→ execute
```

演算問い合わせ:

```text
演算問い合わせ文字列
→ 最小 query parser
→ repository / proof-scope 検索
→ 生 match
→ 数学 statement の表示 grouping
→ 安定した優先順
→ query CLI
```

演算問い合わせの証明再生:

```text
query 結果
→ 選択された表示事実
→ 主要 provenance match
→ 選択事実自身の ProofStep
→ 有界な直接前提再生
→ statement 表示
→ query-proof CLI
```

---

# 3. 主要モジュール

基礎:

```text
expression.py
proof.py
proof_repository.py
rule_catalog.py
repository_inference.py
homotopy_groups.py
toda_rules.py
```

探索 / 適用可能性:

```text
生成元_input.py
repository_proof_scope.py
repository_proof_scope_exploration.py
repository_proof_scope_facade.py
repository_proof_scope_applicability.py
repository_生成元_applicability_facade.py
repository_生成元_applicability_selection.py
repository_生成元_applicability_presentation.py
repository_生成元_applicability_renderer.py
```

既知群 / 具体化 / 再生:

```text
repository_生成元_known_group_identity_lookup.py
repository_生成元_known_group_identity_presentation.py
repository_生成元_known_group_identity_renderer.py
repository_symbolic_sigma_specialization.py
repository_生成元_known_group_proof_replay.py
repository_生成元_known_group_proof_replay_presentation.py
repository_生成元_known_group_proof_replay_renderer.py
```

演算問い合わせ / 再生:

```text
repository_operation_query.py
repository_operation_query_lookup.py
repository_operation_query_facade.py
repository_operation_query_presentation.py
repository_operation_query_renderer.py
repository_operation_query_proof_replay.py
repository_operation_query_proof_replay_presentation.py
repository_operation_query_proof_replay_statement_presentation.py
repository_operation_query_proof_replay_renderer.py
```

qualified execution:

```text
repository_生成元_applicability_execution_seed.py
repository_生成元_applicability_execution_entry.py
repository_生成元_applicability_execution_orchestration.py
repository_生成元_production_application_recovery.py
repository_生成元_production_application_execution_seed.py
repository_生成元_two_premise_execution_integration.py
repository_生成元_qualified_execution_selection.py
repository_生成元_qualified_execution_family.py
repository_生成元_qualified_execution_family_selection.py
repository_生成元_qualified_execution_dispatch.py
repository_生成元_standard_qualified_execution_facade.py
```

利用者向け実行:

```text
repository_生成元_user_execution_resolver.py
repository_生成元_user_execution_handoff.py
repository_生成元_user_execution_proof_step.py
repository_生成元_user_execution_presentation.py
repository_生成元_user_execution_renderer.py
repository_生成元_user_execution_facade.py
repository_生成元_user_execution_candidate_presentation.py
repository_生成元_user_execution_candidate_renderer.py
main.py
```

---

# 4. 証明事実と metadata

証明事実の中心:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata である。

renderer、facade、CLI、resolver、探索、applicability 分類、表示 grouping は証明事実を追加しない。

---

# 5. Repository 非破壊

query / 探索 / 適用可能性 / 実行計画 / 既知群再生 / 演算問い合わせ / 演算問い合わせ証明再生 は元の repository を読み取り専用として扱う。

execution は新しい inference result を構成できるが、元 repository を変更しない。

```text
entries before == entries after
```

必要な経路では既存 `ProofStep` identity を保持する。

---

# 6. 適用可能性の意味論

候補は概念的に

```text
catalog_entry
premise_index
premise_pattern
source_step
bindings
```

を保持する。

```text
前提適合性 != 全 premise 成立
候補 != rule execution
候補 != 証明成功
候補 != 定理事実
```

関連度カテゴリは定理順位付けではない。

---

# 7. Qualified execution の境界

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

複数前提候補から companion premise を任意探索しない。

一致条件:

```text
同じ root_entry identity
同じ inference_rule identity
target conclusion == 明示的 goal
target premises[candidate premise_index] is candidate.source_step
```

`UNIQUE` のときだけ 正確な `premises` tuple を利用する。

recovery された premise tuple は同じ順序・同じ `ProofStep` identity のまま 実行 seed に使う。

---

# 8. 利用者向け実行可能対象の意味論

workflow 状態:

```text
NONE
AMBIGUOUS
EXECUTED
```

規則:

```text
実行可能対象 0 件
→ NONE

実行可能対象 1 件 + candidate_number 省略
→ 自動実行

複数の実行可能対象 + candidate_number 省略
→ AMBIGUOUS

candidate_number 指定あり
→ その 1-based 対象を選択
```

`candidate_number` は表示順に対応する 1-based 指定 であり、数学的優先度を意味しない。

```text
candidate number != 定理順位付け
```

---

# 9. 最終実行済み ProofStep の境界

user-facing execution は repository 側の 元の target step を presentation しない。

実際に 有界実行 が生成した

```text
repository_inference_result.goal_step
```

を 最終実行済み `ProofStep` とする。

```text
実行済み goal_step
は元の repository target_step と必ずしも同一ではない
```

ただし

```text
executed goal_step.conclusion == selected target goal
```

である。

---

# 10. 既知群同一性の意味論

既知群同一性 lookup は、まず 明示的 ambient-group 事実 を利用する。

explicit fact がない場合でも、限定された 生成元 に対して既存 proof scope の 群 relation から ambient group を導出できる。

代表例:

```text
nu_5
sigma'''
sigma''
sigma'
sigma_8
sigma_9
generic concrete sigma_n specialization
```

target group が一意に定まる場合だけ 既知群同一性 node を返す。

```text
既知群同一性 lookup
!= theorem search
!= qualified execution
```

---

# 11. indexed sigma 具体化の境界

Toda Proposition 5.15 の symbolic higher step は

\[
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9
\]

を表す。

concrete generic 具体化 は indexed `GeneratorSymbol(family="σ", index=n)` の 具体 integer \(n\ge 10\) に限定する。

specialization step は symbolic higher step を 直接 premise として保持する。

```text
concrete sigma_n group step
→ premise: symbolic Proposition 5.15 higher step
```

任意の symbolic AST substitution engine は導入しない。

---

# 12. show-proof と execute の分離

```text
show-proof
→ 既知群の proof を表示 / 再生

execute
→ 生成元 に関連する qualified 定理適用 を実行
```

したがって、

```text
show-proof != execute
```

---

# 13. 演算問い合わせの意味論

Phase 110 の 演算問い合わせ は「既存の proof 事実を探す」ための経路である。

対象問い合わせ:

```text
H(<被演算子>)
E(<被演算子>)
Delta(<被演算子>)
<生成元> o <生成元>
```

被演算子 は Phase 110 では 生成元 または 1 個の 二項合成 に限定する。

代表:

```text
H(nu_prime)
Delta(iota_9)
E(eta_2 o nu_prime)
eta_2 o nu_prime
```

重要:

```text
演算問い合わせ lookup
!= inference
!= 数学的評価
```

該当事実 が見つからない場合も、それは「repository / proof scope に対応する既知 fact がない」ことだけを意味する。

---

# 14. 演算問い合わせ検索の境界

`H` は既存 写像 relation 経路 を利用する。

`E` は repository 内で既存表現が複数あるため、既存 `MapApplication(E, ...)` と `Suspension(...)` の意味を 検索時に認識する。

\(\Delta\) は `TodaDeltaImageUpToSignStatement` を既存 statement のまま保持する。

合成問い合わせ は 正確な合成 の 構造的包含 を探す。

parser / lookup は evaluator 入力 を生成しない。

---

# 15. Raw 出現 と 表示 grouping

proof scope は同じ `ProofStep` が複数 repository root から到達可能なことを provenance として保持する。

したがって 生 lookup 結果を削除してはいけない。

Phase 110 の deduplication は 表示層 だけで行う。

```text
raw lookup result
→ 同一数学 statement の grouping
→ 表示 item
```

各 表示 item は、その statement に対応する全 生 match を保持する。

```text
重複除去済み表示
!= provenance 削除
```

---

# 16. 演算問い合わせの表示優先順

主要表示順 は概念的に

```text
最小 proof-scope depth
→ 安定した元 source 順
```

である。

これは 利用者向け可読性 のための順序であり、

```text
表示順 != 定理順位付け
```

である。

---

# 17. 演算問い合わせ証明再生の境界

query 事実再生 の root は 包含する repository 定理 root ではない。

```text
表示 item
→ primary_match
→ primary_match.scope_node.proof_step
→ 再生 root
```

つまり、例えば

\[
H(\nu')=\eta_5
\]

を replay する場合、depth 0 はこの relation 自身である。

```text
operation-query 証明再生
!= repository theorem replay
```

---

# 18. 複数事実の選択

query に複数の 数学的事実 がある場合、自動で先頭を 証明再生 しない。

```text
1 fact
→ --fact 省略可

multiple facts
→ 事実一覧
→ --fact N が必要
```

`--fact` は 1-based 指定 である。

```text
事実番号 != 定理順位付け
```

---

# 19. 演算問い合わせ再生 depth

Phase 110 の 再生 default は 直接 premises の 1 段。

```text
max_depth = 1
```

CLI `--depth` はまだ追加しない。

必要性が確認された場合のみ次 Phase 以降で検討する。

---

# 20. Operation-query statement 表示

statement 表示は次の優先順を取る。

```text
既存 Toda proof statement renderer
→ 既存 repository conclusion renderer
→ Phase 110 限定 statement 固有表示
→ 安全な class 名 fallback
```

利用者向け再生 で dataclass の巨大な raw `repr` に落とさない。

Phase 110 で明示的に追加した 表示 coverage:

```text
Toda53NuPrimeBracketSpecializationStatement
TodaLemma57TwoIota5ImageMembershipStatement
TodaDeltaSurjectiveStatement
```

例:

\[
\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1,
\]

\[
E^2\nu'\in2\iota_5\circ\pi_8^5,
\]

\[
\Delta:\pi_8^5\to\pi_6^2
\quad\text{is surjective}.
\]

aggregate 定理 statement は branch を推測せず、

```text
`TodaProp56FiniteDimensionalStatement`
```

のような 安全な型 fallback を使う。

---

# 21. CLI 境界

現行:

```text
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
python main.py show-proof nu_prime
python main.py show-proof sigma_11
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "E(eta_2 o nu_prime)"
```

`query-proof`:

```text
既知事実なし
→ message + exit 1

複数事実 + --fact 省略
→ 事実一覧を表示 + --fact N を要求 + exit 1

選択事実
→ 証明再生 + exit 0

不正な query / 不正な事実番号
→ argparse error + exit 2
```

---

# 22. Windows UTF-8 CLI 境界

Windows の既定 CP932 では `η₂`、`ν₄` などの Unicode 数学文字を stdout に出力できない場合がある。

実プロセス CLI のみ stdout / stderr を UTF-8 に再構成する。

---

# 23. Phase 110 完了

Phase 110 は user-facing 演算問い合わせ の実需要監査から開始し、既存 proof 事実検索 と 証明再生 を閉じた。

確定した意味論:

```text
lookup != evaluator
```

```text
重複除去済み表示 != 生 provenance の削除
```

```text
query-proof root = 選択事実自身の ProofStep
```

```text
複数事実
→ 暗黙の自動選択をしない
```

```text
unknown replay statement
→ 安全な型 fallback
```

最終 repository 全体 regression:

```text
9055 passed in 455.09s (0:07:35)
```

最終 whitespace 確認:

```text
git diff --check
clean
```

---

# 24. 保留中の機能

```text
複数実行可能対象からの意味論的自動選択
定理順位付け
証明コスト最適化
producer 順位付け
一般的な無制限 backtracking
永続 cache / 並列化
repository snapshot / versioning
古い search report の検出
新たな production 上の必要がない第3 qualified family
任意に入れ子可能な演算問い合わせ grammar
Unicode 合成入力
LaTeX 演算問い合わせ parser
operation-query CLI --depth
別 provenance の手動選択
一般 Toda bracket solver
一般合成 evaluator
一般 E / H / Δ evaluator
coset / 不定性計算
より広い unstable stem
奇素数成分の完全統合
全素数成分を含む通常の球面ホモトピー群計算
無制限 symbolic AST substitution
高度な再帰的証明可視化
Web UI
```

---

# 25. 次 Phase との境界

Phase 110 は完了。

Phase 111 では 一般 evaluator を自動的に開始しない。

まず、Phase 110 までに揃った CLI 機能 全体を利用者視点で監査し、次に実際に不足している操作・表示・query grammar・証明再生 depth などの 必要性 を確認する。

```text
current CLI 機能 audit
→ actual user 必要性
→ 次に不足している最小機能
```
