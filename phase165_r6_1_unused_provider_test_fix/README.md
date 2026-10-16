# Phase 165 R6-1：旧 Provider 撤去後のテスト修正

## 変更対象

- `phase165_r52_r7_registered_common_proof/test_phase165_r52_r7_registered_common_proof.py` のテストモジュール全体。既存の `build_standard_toda_report` に依存する古いテストを、共通探索の委譲・旧 Provider の不在・入力検証・未解決停止を調べる4件に変更する。
- 新規 `phase165_r6_1_unused_provider_test_fix/run.ps1`：変更前ガード、テストのバックアップ、限定 pytest 実行。

Production code は変更しない。既に適用済みの旧 Provider 撤去を前提とし、未適用の場合は変更しない。全体 pytest は Phase 165 最終段階に限る。

## 実行

リポジトリ直下で ZIP を展開し、`powershell -ExecutionPolicy Bypass -File .\phase165_r6_1_unused_provider_test_fix\run.ps1` を実行する。

## 完了条件

4件の限定テストが通ること。これは共通探索の実際の数学的証明成功を意味しない。次の R6-2 では型付き規則の汎用逆向き適用を扱う。
