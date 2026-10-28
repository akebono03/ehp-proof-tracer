# Phase 169 — Git 環境保全・競合参照隔離

## 背景

2026-10-28 の読み取り専用診断では、`.git` 内に Dropbox の競合コピーファイル3件、R5D の長い生成パス273文字、Git HEAD `232a92883b0cb009762b437cbb3cc550f00ab6bd` が記録された。GitHub の develop HEAD と一致することも確認済み。ただし、R5D の本体変更は未コミットであり、保全対象である。

## 変更対象

新規フォルダのみ。`recover.py` の `git()`、`sha256()`、`conflict_paths()`、`path_within()`、`preflight()`、`capture_paths()`、`backup_and_quarantine()`、`main()`、`run.ps1` と新規テスト。既存のアプリケーション、関連テスト、ドキュメントは書き換えない。

## 実行仕様

初期状態は `Audit` で読み取り専用。`Quarantine` は `-DropboxPaused` を明示し、Dropbox を共有する各 PC の同期を手動で一時停止し、VS Code 等を終了した後にのみ実行する。

対象は `.git/refs/heads/develop (oomae-pc11 の競合コピー 2026-10-28)`、`.git/refs/remotes/origin/develop (oomae-pc11 の競合コピー 2026-10-28)`、`.git/logs/HEAD (oomae-pc11 の競合コピー 2026-10-28)` の厳密な3ファイル。件数とパスが一致しない場合、隔離を拒否する。

操作前に `.git` 全体、既存 index、R5D の5ファイル、Git が検出した追跡対象の作業差分およびステージ対象ファイルを Dropbox 外の `%LOCALAPPDATA%` に複製する。index と隔離対象の SHA-256 を照合する。隔離後は `git status` と `git show-ref` を読み取り専用で再確認する。不一致時は移動済みの3ファイルの復帰を試みる。`git reset`・`git clean` は実行しない。

## 境界と完了条件

この環境復旧によって R10ET-R6 の Proof Tree 監査が完了するわけではない。R5D の長い出力ファイルもそのまま保存する。Git が正常に参照を読めることを確認後、R6 の監査を再開する。全体 pytest は Phase 終了時にのみ実行する。
