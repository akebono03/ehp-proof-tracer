# Phase 165 R5 — Safe Cleanup Audit

この ZIP は読み取り専用です。既存コードやテストを削除しません。

## 目的

Phase 165 の共通探索・表示経路で使う主要ファイルについて、Python ソースとテストからの静的参照を記録します。静的参照の不在だけでは未使用を証明できないため、削除候補は自動承認しません。

## 実行

プロジェクト直下で `powershell -ExecutionPolicy Bypass -File .\phase165_r5_safe_cleanup\run.ps1` を実行します。

結果は `phase165_r5_audit_results/audit_result.json` に保存されます。既存ファイルは変更しません。全体 pytest は実行しません。

## 完了条件

監査 JSON が生成され、削除ゼロ・製品コード変更ゼロが記録され、保留した候補について検査限界が明記されていることです。削除の確証がなければ、そのまま R5 を終了します。R6 で全体 pytest と実際の Web 表示を確認します。
