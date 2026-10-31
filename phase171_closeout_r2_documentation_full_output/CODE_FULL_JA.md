# Phase 171 Closeout R2 — コード提示

本番実装の関数・クラス・import は変更しない。新規追加は
`phase171_closeout_r2_documentation_full_output/update_docs.py` と
`run.ps1` と `tests/test_document_writer.py` のみ。全文はそれぞれのファイルに収録する。
追加箇所はリポジトリ直下の新しい監査ディレクトリ。

置換対象の文書5ファイルは `update_docs.py` がレビュー済みコミットの**全文**を
読み取り、履歴を保持して完全な更新ファイルとして出力する。追記本文は
`sections/*.md` に省略せず収録する。

- 新規関数：`git`, `lf_text`, `section_text`, `updated_document`, `atomic_write`,
  `current_files`, `output_directory`, `run_focused`, `export_full_documents`, `main`。
- 追加テスト：`tests/test_document_writer.py` のテスト関数全文と必要な import は同ファイル。
- 既存 API・Proof Tree は変更しない。
- 全体 pytest：Phase 終了時の次 Gate で1度だけ実施。
