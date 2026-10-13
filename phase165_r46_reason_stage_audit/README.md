# Phase 165 R46 — 既存理由リンクの各段階の監査

これは **read-only** の診断です。既存コードを変更せず、`_phase159_r1_6c_link_proof_reasons` の入力・出力と公開 Narrative の結果を比較します。R46 の以前の修正 ZIP は実行しないでください。

変更対象（production）: なし。

新規: `audit.py` の `report()`、`test_audit.py` のテスト3件、`run.ps1`。`audit.py` はプロジェクトルートの `phase165_r46_stage_audit_output/report.json` に記録します。

確認事項: 3件の完全性由来ステップの表示一致キー、Phase 159 リンク前後の接続語数、最終公開出力との比較、再リンク後の文章正規化で接続語が除去されるか。

対象 pytest のみ、全体 pytest なし。これをもって Reference 一般形表示の修正は行いません。
