# R57-R8 修正監査

- 原因: R55 の関数定義は `registered_group_goal_candidates(bridge, *, n: int, k: int)` であり、`n, k` は `kwonlyargs` である。
- 元の `_replace_selector()` は `kwonlyargs` を拒否し、`args.args` のみをパラメータとして検出していた。
- 修正: `args.args` と `kwonlyargs` を統合し、既存のシグネチャを保存する。位置専用引数・可変長引数は従前どおり拒否する。
- 前回の `install()` は書き込み前に例外を出したため、半端なソース変更は発生しない設計。
- 機能追加・証明前提追加は行わない。
- 全体 pytest は実行しない。
