# Phase 169 R3I — 引用済み GIVEN を用いた EHP 終端推論

## 監査時の現状

GitHub `akebono03/ehp-proof-tracer` develop HEAD は `b284eceddcaf2d438b2a7dbdb3ffc4281d30d1ed`。R3H 実行後の出力では、限定 pytest 24 件 PASS、引用 (5.3) に対して `H(ν′)=η₅` の GIVEN が1件、Proposition 5.1 の複合 GIVEN が1件。実探索の π₄² は complete、π₅³ は partial。R3H による未証明 GIVEN の増設はない。

既存の n=3 EHP 終端規則は `ProofRule.INFERENCE` だけを前提とする。これは以前の独立に導出済みの証拠を想定した制約であり、正当な先行文献から直接引用された `GIVEN` には適合しない。

## 本番変更対象（最小限）

1. `phase165_r52_r9_shared_math.py` のトップレベル `shared_expansion_provider()` **全文置換**。その内部で引用・文献順のスクリーニングを終えた `available` だけを新 Provider に渡す。旧 Provider と汎用 Provider はそのまま残す。
2. `phase165_r14_r5_ehp_connection.py` の `audit_ehp_connection()` の**直前**に `expand_cited_ehp_terminal_goal()` を**新規追加**。先行文献から得られた下位 Goal がすべて唯一存在する場合に限り、既存の `InferenceRule` の `match_guard` と `conclusion_builder` をそのまま再利用し、当該推論の前提規則を `GIVEN` に束縛する。

モジュール先頭の import の変更はない。新関数は `dataclasses.replace` と `proof.ProofRule` を関数内部で import する。関数全文は `full_functions/`、適用後の各ファイル全文は `output/` に保存する。

R3H の `build_shared_typed_bridge()`、`phase169_r3h_source_registry.py`、旧 EHP 規則、`toda_rules.py`、Renderer、既存テストは**変更しない**。追加する推論規則は古いルールを破壊せず、`INFERENCE` として結論を構築する。

## テストと完了条件

限定 pytest は以下を指定する。

- `phase169_r3i_cited_ehp_inference/tests/test_phase169_r3i_cited_ehp_inference.py`（新規8件）
- `phase165_r14_r5_ehp_connection/test_phase165_r14_r5_ehp_connection.py`
- `tests/test_phase161_r3_backward_goal_schema.py`
- `phase166_r3g_toda45_registry_connection/test_r3g.py`
- `phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py`
- `phase169_r3f3_focused_collection_repair/tests/test_phase169_r3f_ehp_terminal_subgoals.py`

実探索監査は π₄² が complete であること、π₅³ の引用命題が Proposition 5.3 に解決されること、(5.3) の引用が先行すること、2つの終端結論が実際に `INFERENCE` により得られ、その ProofStep の前提が正当な `GIVEN` であることを検証する。レポートは `output/cited_ehp_inference.json` に書く。π₅³ の complete は事前に仮定しない。

成功表示は `R3I_FOCUSED_PYTEST_EXIT_CODE=0`、`R3I_AUDIT_EXIT_CODE=0`、`R3I_COMPLETE`。失敗時は2ファイルを R3H 状態に戻す。全体 pytest は Phase 169 の最後まで実行しない。

## 次 Phase との境界

R3I は EHP 終端命題の合法的な導出だけを扱う。巡回群の表示正規化、自己参照のない文章生成、Reference 表示の整理、および π₆⁴ 以降の輸送は次段階で扱う。π₅³ 完成とみなすのは、完全なルート ProofStep の検証が成功した場合に限る。
