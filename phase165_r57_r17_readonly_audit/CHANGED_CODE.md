# R57-R17 新規コード

この Phase では既存ファイル・クラス・メソッドの変更はない。

追加位置: リポジトリ直下の `phase165_r57_r17_readonly_audit/` ディレクトリ。

- `audit.py`: `safe_string()`、`summarize_result()`、`diagnose()`、`render_report()`、`main()`。すべて新規関数。完全な import とコードは同梱 `audit.py` に収録。
- `test_audit.py`: 診断用の新規テスト4関数。完全な import とコードは同梱 `test_audit.py` に収録。
- `run.ps1`: Windows PowerShell 実行スクリプト。

変更一覧: 新規監査パッケージのみ。既存 API 変更なし。

対象 pytest: `python -m pytest -q phase165_r57_r17_readonly_audit/test_audit.py`

完了条件: テスト4件成功、実環境の `audit_results.json` と `audit_results.txt` が生成されること。

次 Phase との境界: 監査結果を確認するまでは型付き命題や推論規則を追加しない。
