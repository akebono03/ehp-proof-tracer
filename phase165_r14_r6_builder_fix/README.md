# Phase 165 R14-R6 修正 — conclusion_builder 引数契約

変更対象: `phase165_r14_r6_generic_iso.py` の `_build_isomorphism()` と `_build_transfer()`（各関数全文）、`test_phase165_r14_r6_generic_iso.py` の末尾に `test_conclusion_builders_follow_existing_single_argument_contract()` を追加。import 変更なし。

既存 `proof.py` の `apply_inference_match()` は builder に `inference_match.premises` のみを渡すため、builder の不要な `bindings` 引数を削除しました。`match_guard` の引数契約は変更しません。追加テストで builder が1引数であることを確認します。

`run.ps1` は修正した完全モジュールを上書きし、関連する7件の pytest と監査を実行。全体テストなし。完了条件: 7 passed と監査正常終了。次段階の登録済み前提と EHP 証明生成には踏み込みません。
