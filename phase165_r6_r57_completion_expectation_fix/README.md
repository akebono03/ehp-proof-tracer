# Phase 165 R6 — R57-R1 完成判定テストの更新

## 変更対象
`phase165_r57_r1_single_entry/test_phase165_r57_r1_single_entry.py` の `test_standard_route_real_pi32_public_renderer()` 全体。対象関数の assert を 1 箇所修正し、`partial_result is False` のチェックを追加する。実装コード・import・他のテストは変更しない。

## 実行
`powershell -ExecutionPolicy Bypass -File .\phase165_r6_r57_completion_expectation_fix\run.ps1`

実際の探索結果を完成に偽装しない。complete でない場合にはテストが失敗する。既存の表示テキストに対する検査を維持する。全体 pytest は Phase 165 の最後に実行する。

## 終了条件と境界
R57-R1 3 テスト PASS。これは R6 全体の完了・全テスト PASS・ブラウザーの MathJax 表示成功を意味しない。次の Phase の機能は追加しない。
