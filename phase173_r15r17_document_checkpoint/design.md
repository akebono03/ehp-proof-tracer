# Phase 173 R15R17 文書更新設計

`README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` の **5ファイル全文**を原文から生成する。最新の GitHub `develop` で確認した各ファイルの Blob SHA を要求し、既存内容の後ろへ現時点の確認結果を追加する（README のみ最新状況を歴史的 Phase 172 節の前へ配置し、Phase 172 の見出しを歴史的記録へ訂正する）。

`development_log` と `proof_records` は過去本文のバイト列を保存して追記する。`design` と `roadmap` も Phase 173 の新しい節を追記し、過去の履歴を削らない。README は英語、他の4文書は日本語で記述する。数式は Markdown の `$` と `$$` を使用する。

`-DryRun` は変更後の各文書**全文**を `full_documents/` に出力し、Git 追跡済みファイルには書き込まない。本実行は同じ全文を出力したうえで、厳密な入力監査・バックアップを経て置き換える。既存の関連しない変更は保持し、Git index の staged 内容も保全する。全体 pytest は Phase 173 最終 Gate だけで実施する。

今回の文書は R15R17 の HTTP 監査までの記録であり、ブラウザ実表示、Phase 終了時の全体 pytest、Phase 173 の正式終了を認定しない。
