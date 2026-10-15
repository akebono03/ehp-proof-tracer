# 変更一覧

既存のファイル・クラス・関数・テストは一切変更しない。

新規ファイル（配置先はリポジトリ直下の `phase165_r57_r22_connection_audit/`）：

- `audit.py`: `function_names`, `static_audit`, `adapter_frontier_probe`, `main`（監査用途の新規関数）
- `test_audit.py`: 4件の監査用 pytest と import の全体
- `run.ps1`: ZIP 解凍後の実行スクリプト
- `README.md`, `AUDIT.md`, `CHANGED_CODE.md`: 監査文書

本体ファイルの内容を変更しないため、置き換える既存クラス・関数・import はない。次段階では型付き照合、候補探索、前提生成を個別に検証する。
