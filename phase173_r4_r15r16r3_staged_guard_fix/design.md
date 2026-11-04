# Phase 173 R4-R15R16R3 設計

## 障害と修正

前回の R15R16R2 は `git diff --cached --name-only` に1つでも項目があると停止した。
しかし, ステージされた無関係のファイルには干渉しないため, この条件は過剰だった.

本修正では, 対象ファイルに関する index / worktree / レビュー済み R15R16 内容の同一性を検証してから実行する.
未対象のステージ済みファイルには触れない.

## 保護する状態

- `git add`, `git reset`, `git restore --staged`, `git commit` を自動実行しない.
- GitHub develop とローカル HEAD が一致することを確認する.
- 対象ファイルのコミット済み blob を確認する.
- R15R16 の未コミット内容を再検証する.
- ステージ済みの対象ファイルの index が内容一致しなければ中止する.
- 導入後も index を変更せず, ロールバックは導入前の worktree に戻す.

## Phase 境界

数学的な Proof Search, 既存 API, Citation 判定, 完了/未完了の分類は変更しない.
全体 pytest は Phase 173 終了時のみ実行する.
