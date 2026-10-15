# Phase 165 R57-R1 runner 修正

- 対象ファイル：`phase165_r57_r1_single_entry/run.ps1`（全文置換）
- 原因：R56-R2 のテストは `phase165_r56_r2_public_renderer/` に同梱されているが、旧 run.ps1 はリポジトリ直下のみを確認していた。
- 変更：対象テストをリポジトリ直下・R57 パッケージ・対応する展開済み Phase パッケージから明示的に解決する。
- 変更しないもの：Python のクラス・関数・import、旧方式の削除、Renderer、証明探索、ProofStep、テスト内容。
- 実行：R57-R1、R56-R2、R56、R55 の対象テスト4モジュール。
- 完了条件：4モジュールが収集され、全件 PASS。全体 pytest は実行しない。
- 次段階：監査一覧をもとに部分証明の公開用 Renderer 統一と不要な旧経路削除を別途進める。
