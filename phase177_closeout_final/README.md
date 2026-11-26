# Phase 177 Closeout Final — 保存済み実測による文書確定

実測 HEAD：`70d3ba540adebe96ada08728d045c1153e7e919a`（develop）。実測後の監査パッケージ8ファイルのみを追加した HEAD `a8d61bf5cf0953a33d8b0985f78ebb75fd62ad3c` も、差分と各 blob の一致を条件に許容する。

初回 Measurement の全体 pytest `3546 passed in 40.59s` と R1 の非安定登録15群・k=5 登録6群の complete を再利用する。初回の KeyboardInterrupt、R1、元のログ・証明木・Narrative を変更しない。新規証明探索、全体 pytest、限定 pytest、本番コード・既存テストの変更は行わない。旧 Phase 174 Source Guard 4件は未解決のまま。

- `run.ps1 -DryRun`：HEAD、監査スクリプトのハッシュ、保存済みレポート、JSONL、テストログ、登録範囲、出典、文書基準を読み取り確認する。文書の書き込みなし。
- `run.ps1`：同じ検査後、完全な5文書の原本・更新版と ZIP を `%LOCALAPPDATA%\EHPProofTracerAudit\phase177_closeout_final\attempt_*\` に生成し、整合性を確認してからリポジトリの5文書のみを更新する。
- `README.md`、`docs/design.md`、`docs/roadmap.md` は新しい現在地を先頭に追加し、Phase 176 の先頭見出しを履歴扱いとする。`docs/development_log.md`、`docs/proof_records.md` は追記を基本とし、既存日本語文書の数学用語「不安定」は「非安定」に統一する。実測ログの SHA-256 を記載する。
- 文書の置換は同一ディレクトリ内の一時ファイルを使う。ロック等で停止した場合、成功した置換は保持し、未知の内容は上書きしない。失敗した attempt と原本・全文ZIP を保存する。ロックを解消し、状態を確認してから同じ Final を再実行できる。全体 pytest を再実行しない。既に成功した場合は `final_report.json` により再実行を拒否する。
- 本番コード、インデックス、過去の証拠を変更せず、5文書の実バイト一致と `git diff --check` を確認した場合のみ `PASS_PHASE177_ACTIVE_SCOPE_CLOSED_WITH_HISTORICAL_GUARD_OPEN` を出力する。

PowerShell はリポジトリルートで実行する。元の Measurement/R1 パッケージと `%LOCALAPPDATA%` 内の監査証拠を保持する。生成された全文は attempt 内の `final_full/`、ZIP は `EHP_Phase177_Final_Five_Full_Documents.zip`、最終レポートは `final_report.json`。Git commit/push は自動実行しない。

本訂正版は未完了の Final を置き換える。旧 Final の成功済みレポートがある場合は実行しない。実測時の HEAD と証拠のハッシュは変更しない。
