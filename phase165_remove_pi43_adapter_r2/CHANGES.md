# Phase 165 R2：群別 Adapter 撤去確認

- 本番コードの変更：なし。
- 新規 `audit.py`：`audit_repository()`、`main()`。ルート直下の Python ファイルを AST 監査し、Adapter の残存と共通 Provider の接続を検証する。
- 新規 `test_audit.py`：上記の4件を対象に pytest を実行する。
- 新規 `run.ps1`：監査と対象限定 pytest。全体 pytest は実行しない。
- 完了条件：`status=REMOVED`、`adapter_file_exists=false`、`active_root_references=[]`、接続3種類が true、対象テスト PASS。
- 次の作業：群別 Adapter なしで π_4^3 の未解決前提を計測して共通推論規則へ接続する。証明完成は本 R2 に含めない。
