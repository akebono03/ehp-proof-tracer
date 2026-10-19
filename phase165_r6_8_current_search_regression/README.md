# Phase 165 R6-8 — 現行探索への移行用回帰テスト

## 変更対象
新規ファイル `phase165_r6_8_current_search_regression/test_phase165_r6_8_current_search_regression.py` の新規テスト関数2つ、および実行用 `run.ps1`、`README.md`。既存 Python コード、class、function、import は変更しない。

## 目的
廃止済み Phase 50 probe を介さない現行の `search_group_from_registered_goal` に対して、π₄³ と π₃² の目標を共通探索し、最終結論が GIVEN ではなく INFERENCE の ProofStep によって裏付けられているか確認する。既存の旧テスト105件の代替として数学的に同等という主張はしない。

## 実行方法
`powershell -ExecutionPolicy Bypass -File .\phase165_r6_8_current_search_regression\run.ps1`

## 完了条件
2件の限定テストが PASS。これは R6-8 の中間ゲートであり、105件の import エラー解消を意味しない。旧 probe の結果を消費する downstream の置換には別途作業が必要。次 Phase の機能追加なし。全体 pytest は行わない。
