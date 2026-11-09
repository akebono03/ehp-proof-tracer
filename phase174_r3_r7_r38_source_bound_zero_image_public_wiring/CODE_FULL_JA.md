# R38 コード全体

更新する既存関数の全文は `CHANGED_FUNCTION_FULL.py` に収録した。更新後の import 全文は `IMPORTS_FULL.txt`、更新するモジュール全文は `replacement/context_provider_registry.py` に収録した。

新規モジュールは `provider.py`、`install.py`、`audit.py`。追加位置は新規ディレクトリ `phase174_r3_r7_r38_source_bound_zero_image_public_wiring/` の直下。テスト関数・import 全文は `tests/test_static.py` と `tests/test_public.py` に収録した。既存クラス・既存テストは変更しない。

既存 Context Provider は4件を保持し、R36 の条件付き Provider と今回の R38 条件付き Provider を追加する。データベース prior を引用付き GIVEN に格上げする変更はない。`ProofStep` を新規作成しない。根の専用分岐、専用 Narrative、最終結論の GIVEN は追加しない。
