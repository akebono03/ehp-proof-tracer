# Phase 165 R6 限定確認

リポジトリルートへ展開し `powershell -ExecutionPolicy Bypass -File .\phase165_r6_closure_check_fast\run.ps1` を実行。

変更対象: 新規 `check.py`, `run.ps1`, `README.md` のみ。既存コードとテストは変更しない。最大3ファイルの限定テストを60秒上限で実施。全体収集・全体 pytest・削除は行わない。対象がなければ未検証を明示。結果は `phase165_r6_audit_results/closure_check_fast/report.json` に出力。
