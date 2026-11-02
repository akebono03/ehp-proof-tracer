# Phase 173 R4-R1 — Git 作業ツリー停止原因診断

## 対象

新規追加のみ：`phase173_r4_r1_git_status_diagnostic/run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`。既存ファイル、クラス、関数、import、公式文書の変更はない。

## 目的

従来の R4-R1 監査の `preflight()` が `git status --porcelain --untracked-files=no` を理由に停止したため、どの追跡済みファイルが変更済みか、ステージ済み／未ステージか、出典・推論の既レビュー対象に含まれるかを読み取り専用で判定する。

## 安全条件

Git を変更するコマンドは呼ばない。`git reset`、`git checkout`、`git restore`、`git stash`、`git add`、`git commit` を実行しない。ZIP 展開時の既存コード上書きも不要（新規ディレクトリのみ）。診断レポートは `%LOCALAPPDATA%` 以下に保存する。

## 状態の読み方

- `CLEAN_TRACKED_WORKTREE`：追跡済みファイルの変更は見つからない（監査をそのまま再実行できる可能性）。
- `REVIEWED_SOURCE_MODIFIED_STOP`：R4-R1 が SHA を確認する重要ソースに変更がある。変更内容の確認前に監査のガードを緩和しない。
- `OTHER_TRACKED_FILES_MODIFIED_REVIEW_REQUIRED`：その他の追跡済みファイルに変更がある。まずファイル名と差分を確認し、監査実行への影響を判断する。

## 完了条件

`PHASE173_R4_R1_DIAGNOSTIC=PASS` と `CLASSIFICATION`、変更ファイル一覧、レポート先が表示されること。これは数学的証明・R4-R1 監査完了の判定ではない。全体 pytest は実行しない。
