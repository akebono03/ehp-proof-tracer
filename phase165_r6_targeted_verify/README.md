# Phase 165 R6 限定検証

既存 production code と既存テストは変更しません。GitHub 上の関連 run.ps1 を調べ、対象を3件に限定しました。テストは既存ファイルがある場合だけ実行し、見つからなければ MISSING として未完了を報告します。各テストの制限時間は90秒です。全体 pytest や全体収集は行いません。検証結果は phase165_r6_audit_results/targeted_verify/report.json に出力します。

実行：`powershell -ExecutionPolicy Bypass -File .\phase165_r6_targeted_verify\run.ps1`

このテストの PASS は Phase 165 全体の完了を意味しません。Web 描画は別途確認が必要です。
