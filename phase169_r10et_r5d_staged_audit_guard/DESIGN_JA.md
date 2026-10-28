# Phase 169 R10ET-R5D — Git index の許可条件を安全に修正

## 状況

R10ET-R5C は実装前のガードで停止した。`develop` HEAD は `3a8014efb91ddf76060c4d07d73153e55ea52c75`（R4 実装のコミット）で、本体コードの未コミット変更は存在しない。しかし、R5 の9ファイルに加え R5B の10ファイルが Git staging area に存在したため、R5C の「R5 の9ファイルだけ」という制限に反した。証明探索・限定 pytest は実行されておらず、部分的な製品変更もない。

## 変更対象と追加位置

- 新規 `phase169_r10et_r5d_staged_audit_guard/run.py`：既存 R5C ランナーの独立コピー。`ALLOWED_STAGED_AUDIT_DIRECTORIES` を `REVIEWED_HEADS` 直前に追加し、`reviewed_index_snapshot()` 全体を置換。`FOCUSED` のテスト場所とログ識別子を R5D に変更。`verify_preconditions()` と `main()` は検査対象のバイト一致・rollback の意味を変更しない。
- `tests/test_r5d_guard.py`、`tests/test_r5d_git_index.py`：新規ファイル。変更前後の Git index を実験で検査する。
- `patch.py`、`audit.py` と `tests/test_r5_patch.py`、`tests/test_r5_live.py` は R5C から自立動作するよう移植。新規数学規則や引用処理を追加しない。
- README.md（英語）、DESIGN_JA.md（日本語）は新規ファイルとして全文作成。既存の `README.md`, `docs/design.md`, `docs/development_log.md`, `docs/roadmap.md`, `docs/proof_records.md` は変更しない。

## 安全条件

Git index にある変更が **新規追加（`A`）のみ** であり、パス先頭がレビュー済みの R5、R5B、R5C、R5D の4ディレクトリのいずれかである場合だけ許可する。部分的にステージされている場合も問題ない。ステージ済みの本体ファイル、未知のディレクトリ、`M`、`D`、`R`、パス逸脱などを拒否する。

`git diff --cached --raw` を実行前に保存し、終了後も同一であることを検証する。Git index を変更するコマンドは使用しない。`develop` HEAD、R4 の2ファイル、R5 入力5ファイルについては従来と同じ厳密なソース照合を継続する。想定外の変化や検証失敗があれば R5 の5ファイルだけを復元し、コミット済み R4 とステージ済み監査資料は維持する。

## 完了条件

- 限定 pytest PASS。
- R2 の16ケースと同じ完成証明・Trust・Reference・Projection の監査が PASS。
- `R10ET_R5D_INDEX_PRESERVED=True`、`R10ET_R5D_COMPLETE=PASS`、`R10ET_R5D_EXIT=0`。
- `git status -sb` に本体への R5 の5ファイル以外の追加変更がない。
- 全体 pytest は Phase 169 終了時まで実行しない。

## 次段階との境界

R5D は R5 の本番 Definition 優先適用を実行するための安全ガード修正のみ。個別命題台帳の削除や、将来の複数 stem を含めた理論の一般化は先取りしない。R5D が成功した後に、残存する個別 Definition への依存を R6 で監査する。
