# Phase 169 R3U1 — 変更一覧・コード全文

## 本番関数

`phase165_r14_r5_ehp_connection.py` 内の `expand_cited_ehp_terminal_goal()` 全体を R3U と同内容で置換。実装全文は `full_functions/expand_cited_ehp_terminal_goal_FULL.py`。R3U1 固有の本番コード修正はない。トップレベル import 変更なし（関数内 import は全文収録）。

## テスト関数

対象ファイルは以下の3件。いずれも import は変更せず、置換する関数をそれぞれ全文収録する。

- `phase169_r3i_cited_ehp_inference/tests/test_phase169_r3i_cited_ehp_inference.py`
- `phase169_r3i1_proof_closure_audit/tests/test_phase169_r3i_cited_ehp_inference.py`
- `phase169_r3i2_import_repair/tests/test_phase169_r3i_cited_ehp_inference.py`

R3U からの継続置換:

- `test_r3i_only_exact_screened_claims_propose_cited_rules()`
- `test_r3i_derived_terminal_steps_have_exact_cited_ancestors()`
- `test_r3i_historical_inference_only_rules_remain_intact()`
- `test_r3i_real_recursive_proof_of_terminal_goals()`

**R3U1 の差分**は `test_r3i_historical_inference_only_rules_remain_intact()` の Hopf 側について、別々の factory 呼び出しの `guard` と `conclusion_builder` を関数オブジェクトの `is` ではなく `.__code__ is` で比較する2式のみ。関数全文は `full_functions/test_r3i_historical_inference_only_rules_remain_intact_FULL.py`。残り3関数の全文も `full_functions/` 内に収録。

## 新規ファイル

- `tests/test_phase169_r3u_delta_diagonal_dependency.py`：R3U と同じ5テスト関数・全 import（新規テストファイル、配置はこのパッケージ内）。
- `audit.py`：R3U と同じ完成証明の実監査。
- `install.py`, `run.ps1`：全関数の置換、変更前・変更後全文の `output/` 保存、限定 pytest、失敗時復元。

完了条件は `5 + 8 + 8 + 8 + 10 = 39` 件 PASS と、Delta 単射の祖先に (5.1) を含む実監査 PASS。全体 pytest は実行しない。
