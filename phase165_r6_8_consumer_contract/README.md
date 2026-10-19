# Phase 165 R6-8: Legacy consumer contract audit

変更対象: 新規の `phase165_r6_8_consumer_contract/audit.py`、`run.ps1`、`README.md` のみ。既存ファイル、クラス、関数、import、テストは変更しません。

依存経路が確認済みの旧 Phase 50 / 55 / 58 の利用側について、使用しているデータのキーと、依存する旧ビルダーを AST から抽出します。`phase165_r6_audit_results/r6_8_consumer_contract/report.json` に保存します。

```powershell
powershell -ExecutionPolicy Bypass -File .\phase165_r6_8_consumer_contract\run.ps1
```

この静的調査だけで置換の数学的同値性は保証されません。既存の検証内容を保存した最小限の移行案を決めるための境界確認です。実装変更・pytest は行いません。R6-8 は未完了のままです。
