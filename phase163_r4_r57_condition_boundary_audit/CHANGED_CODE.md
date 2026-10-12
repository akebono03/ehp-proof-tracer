# Phase 163 R4-R57 変更一覧

既存ファイルは変更しない。以下の新規ファイルのみ追加する。

- `phase163_r4_r57_condition_boundary_audit.py`：`SOURCE_FILES`、`CONTEXT_RULES`、`UNVERIFIED` の直後に `sha256`、`_source_evidence`、`build_boundary_report`、`write_report`、`main` を定義。
- `tests/test_phase163_r4_r57_condition_boundary_audit.py`：9件の限定テストを定義。
- `run.ps1`：テストと監査の実行。
- `README.md`：英語の操作説明。
- `CHANGED_CODE.md`：本書。

各 Python ファイルの import・関数・テストは全文掲載した実ファイルであり、省略はない。

完了条件：3定義について明示・文脈・未検証を根拠行付きで区別し、9件の限定テストを通過すること。

次の R4-R58 まで、本番 Registry への登録、ID 発行、数学的 AST 化は扱わない。全体 pytest は Phase 最終段階まで実施しない。
