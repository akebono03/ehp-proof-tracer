# Git ref の Dropbox 競合コピー復旧

## 目的

2026年10月28日の VS Code Git ログにある `refs/heads/develop (oomae-pc11 の競合コピー 2026-10-28)` と `refs/remotes/origin/develop (oomae-pc11 の競合コピー 2026-10-28)` を対象とする。

`git check-ref-format` に照らして空白入りの ref 名は不正。正常な `refs/heads/develop` と `refs/remotes/origin/develop` の SHA を読み取って検証し、重複した不正なファイルだけを対象とする。

## 対象

- 新規 `run.ps1`: `Invoke-GitOrFail`, `Resolve-GitDirectory`, `Get-ConflictedRefCopies` とトップレベル実行。
- 新規 `tests/test_git_ref_recovery_contract.py`: スクリプトの静的な安全性とログ由来の名称の検査。
- 新規 `README.md`, `DESIGN_JA.md`。

既存リポジトリのコード、既存テスト、文書、`.git/HEAD`、通常の ref は変更しない。

## 手順

1. デフォルトでは読み取り監査のみ。
2. Dropbox 同期を一時停止したうえで `-Repair` を指定した場合だけ競合コピーを移動する。
3. バックアップ先は `$HOME/ehp-git-ref-conflict-backup-...`。Git 管理外に置く。
4. 移動したファイルの SHA-256 を確認する。正常な2つの ref のコミット SHA が変化していないことも確認する。
5. 失敗時は移動できたファイルを元の場所へ戻す。`git reset`、`git gc`、`git pull` は実行しない。

## 注意

GitHub からオブジェクトが不足しているというメッセージは、今回のログではローカルの不正 ref と同時に発生している。原因を確定的に GitHub サーバー側と断定しない。復旧後の `git fetch origin develop` であらためて判定する。

Phase 169 の証明表示・推論の仕様には一切影響しない。全体 pytest も実行しない。
