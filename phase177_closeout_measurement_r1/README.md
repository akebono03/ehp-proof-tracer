# Phase 177 Closeout Measurement R1

元の Measurement は全体 pytest 3546 passed in 40.59s と k=5 登録6群の完成を確認した後、過大な831群探索を手動中断した。元の失敗記録を変更せず、保存されたレポート・ログ・JSONL の整合性と現行 HEAD を確認する。

対象は `stable_rules.is_in_toda_stable_range` が偽で、$0\le k\le5$ の登録15群。安定範囲は $n\ge k+2$。安定313群と今後の不安定503群は新たに探索しない。15群のうち8群は元の実測結果を再利用し、残る7群のみ既存の worker で探索する。k=5 の6群（安定1群を含む）は元の結果を別集計する。全体 pytest は再実行しない。

元の `phase177_closeout_measurement/` パッケージと `%LOCALAPPDATA%/EHPProofTracerAudit/phase177_closeout_measurement/` の証拠ファイルが必要。`run.ps1 -DryRun` の後 `run.ps1` を実行する。復旧結果は同じ監査ルートの `phase177_closeout_measurement_r1/` に保存する。既存コード、テスト、文書を変更しない。最終成功 `PASS_PHASE177_CLOSEOUT_SCOPED_MEASUREMENT_DOCUMENTS_PENDING` は実測監査の成功であり、正式終了は文書更新後とする。
