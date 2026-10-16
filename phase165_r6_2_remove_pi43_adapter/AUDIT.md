# Phase 165 R6-2 専用 Adapter 廃止

GitHub 現行の `phase165_r52_r9_shared_math.py`、`phase165_r52_r23_existing_rule_adapter.py`、R8・R26 および関連テストを確認した。

`shared_expansion_provider()` の Provider 列挙から `expand_existing_pi43_rules` を外し、専用 import を削除する。専用 Python モジュールは復旧可能なバックアップへ移動する。汎用規則への置換が実証されていないため、未証明 Goal は未証明のままとする。

変更ファイル：`phase165_r52_r9_shared_math.py`。退避ファイル：`phase165_r52_r23_existing_rule_adapter.py`。新規：`apply.py`、`test_apply.py`、`run.ps1`。既存クラスは変更しない。変更する関数は `shared_expansion_provider()`（実際の変更は Provider 一覧から1項目を除くのみ）。import は対象の専用 import 1つのみを除去する。全体 pytest は Phase 最終時まで実行しない。

既存の群専用規則 factory 自体は削除しない。証明成功は保証しない。古い履歴資料と関連テストは変更しない。
