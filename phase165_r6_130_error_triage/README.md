# Phase 165 R6: 130 件の収集エラー分類

既存の `phase165_r6_error_triage/triage.py` を再利用し、保存済み `phase165_r6_audit_results/collection_close/collection.log` を解析する。

変更対象は新規 `phase165_r6_130_error_triage/run.ps1` と `README.md` のみ。既存コード・テスト・import 変更なし。

出力は `phase165_r6_audit_results/collection_close/triage_130.json`。エラー原因の分類であり、削除や修正の実施ではない。エラーの全件を解析できなければ収集ログの全体を確認し、未解析分は保留とする。

`powershell -ExecutionPolicy Bypass -File .\phase165_r6_130_error_triage\run.ps1`

pytest の収集・実行は行わず、Phase 165 最後の全体 pytest も実施しない。次 Phase の機能追加なし。
