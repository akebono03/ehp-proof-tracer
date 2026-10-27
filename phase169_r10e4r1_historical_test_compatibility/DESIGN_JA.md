# Phase 169 R10E4R1 — 旧テスト互換性の修復

R10E4 実行ログの 84 PASS / 1 FAIL は、R10E2 の `test_r10e2_guarded_patch_refuses_double_application()` が、R10E2 パッチ後のモジュール全文と現行モジュールの byte-for-byte 一致を要求することによる。

R10E4 は同じ `expand_prior_general_group_transport()` に DB 先行結果のフォールバックを追加するため、この全文一致は成立しない。本変更では旧テストの該当する 1 行だけを、R10E2 の source-first 選択コードが残っていることと、R10E4 の DB 先行処理が存在することを確認するアサーションに置き換える。二重パッチを拒否する元のチェックは保存する。

本番の群構造規則、命題台帳、DB、引用処理、Renderer は変更しない。対象の既存テストを含む R10E4 の元の限定 pytest と監査を実行する。失敗時、旧テストは R10E4R1 が、本番 3 ファイルは R10E4 がそれぞれ復元する。`git reset`、全体 pytest は行わない。

R10E4 の本番変更成功は、元の R10E4 `run.ps1` によるテスト・監査が成功した後にのみ確認できる。旧テストを修正しただけでは R10E4 の完了を宣言しない。
