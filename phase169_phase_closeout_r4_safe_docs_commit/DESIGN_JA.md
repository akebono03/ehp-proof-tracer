# Phase 169 Closeout R4 — 終了文書5件の安全な Git 登録

## 対象と責務

対象は Phase 169 Closeout R3B で更新済みの `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` の Git 登録のみ。変更する既存ファイル・本体クラス・関数・メソッドはない。追加ファイルは新規パッケージの `run.py`、`run.ps1`、`tests/test_commit_guard.py`、本説明文書と `README.md`、`__init__.py`。

## 監査手順

レビュー済み HEAD `1e881f45b2f3f3ecbb1052750c9d7a7b5bf95712` と origin/develop、GitHub の remote HEAD が一致していることを確認する。既存 tracked 変更が5文書だけ、ステージ済み変更がないことを確認する。変更前の committed Git blob、R1 Gate の JSON・ログと67/3546 PASS、R3B manifest、変更前・変更後の全文コピーの一致を検証する。検証が不成立なら停止する。

## 実行条件

`run.ps1` は監査専用（Git に変更を加えない）。`run.ps1 -Commit` は利用者が明示して実行した場合だけ、検証後に正確に5文書を Git stage・commit する。自動 push や reset/restore/clean/pull はしない。commit 前のパッチを `%LOCALAPPDATA%\EHPProofTracerRecovery` に保存する。監査フォルダは未追跡のまま残す。

## テストと完了境界

R4 では補助関数の限定 pytest のみを行う。Phase 169 最終の全体 pytest は R1 の3546 PASS を証拠として使用し、再実行しない。コミット成功はローカル履歴の確定であり、remote の更新ではない。GitHub への反映は別作業とする。未完の数学的主張や DB 整備は Phase 170 の監査対象であり、R4 では実装しない。
