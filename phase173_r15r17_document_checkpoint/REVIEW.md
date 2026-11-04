# レビュー対象と境界

変更先の既存ファイル:

1. `README.md` — Phase 173 の現状（英語）、旧 Phase 172 の見出しの履歴化。
2. `docs/design.md` — 単一 ProofNarrativeModel と検証境界。
3. `docs/development_log.md` — R1 から R3R5 の実測と未実施事項の追記。
4. `docs/roadmap.md` — Phase 終了までの依存事項。
5. `docs/proof_records.md` — 抽象群の検証と記名生成元の未完成の区別。

実装は `docs_builder.py` の `apply_document_update`（全文を構成）、`verify_repository`（コード変更検査）、`generate_files`（全文出力・バックアップ）などのみを新規追加。既存 Python コードやテストは変更しない。

`full_documents/` に5ファイル全文を出力し、R15R17 の未完了事項を意図的に残す。ブラウザの目視確認や Phase 173 の全体テストは後続の正式 Gate で行う。
