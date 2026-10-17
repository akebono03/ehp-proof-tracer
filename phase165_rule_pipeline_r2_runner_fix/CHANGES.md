# Phase 165 R2 実行修正

- `run.ps1`：作業ディレクトリをリポジトリ直下に設定し、監査を `python -m phase165_rule_pipeline_r2_runner_fix.audit` で起動する。
- `test_audit.py`：監査関数の import をパッケージ名付きにする。
- `audit.py`：変更なし。
- 本番コード：変更なし。
- 対象 pytest：2件。全体 pytest は実施しない。
