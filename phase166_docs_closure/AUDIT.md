# Phase 166 文書更新の仕様

更新対象：リポジトリ直下 `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md`。追加する関数は `apply.py` の `main()`（新規ファイル）。既存関数・クラス・import は変更しない。

GitHub `develop` の現行文書を確認。履歴を保持するため旧本文に日付付きの現行状態を追加し、全ファイルをそれぞれ全文で書き直す。適用後の全文と適用前のバックアップを出力ディレクトリに保存する。重複適用は停止する。

Phase 166 は限定監査を終えて実装停止したが、全体 pytest 合格は未認定。Phase 167 は π₄³ の Narrative 修正から開始し、その後 π₅³ の partial 探索を調査する。

今回 pytest は実行しない。既存本番コード・既存テストを変更しない。
