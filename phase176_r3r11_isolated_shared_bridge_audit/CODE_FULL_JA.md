# Phase 176 R3R11 コード配置

- 新規 `audit.py`：監査用の関数 `git_output`、`scalar_evidence`、`interesting_evidence`、`audit`、`main` を追加。既存コードを変更しない。
- 新規 `tests/test_audit.py`：4件の単体テストを追加。既存テストは変更しない。
- 新規 `run.ps1`：DryRun、本実行、限定 pytest 用。

すべてのファイルは ZIP 内に全文収録。import と関数本体は `audit.py` および `tests/test_audit.py` の原本を参照する。
