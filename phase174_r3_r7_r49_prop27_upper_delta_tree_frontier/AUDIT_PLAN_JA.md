# Phase 174 R3-R7-R49 監査計画

- GitHub `develop` 現行 HEAD: `1d792feec594a67b83701d337b7745270c533484`。
- 前段 R48/R48R2 の数学コードは未変更。R48 で核の `INFERENCE`、19 ProofStep、R30 の型付き Proposition 2.7 を次の未解決 Goal として確認した。
- 変更対象: 新規 `phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/` のみ。
- `audit.py`: 新規 `inspect_integrated_prop27_frontier()`・`main()`。R48 から検証済みとされた ProofStep を注入せず、全枝を標準探索で再証明する。
- `source_guard.py`: 新規 `verify_checkout()`。GitHub HEAD、数学ソース、R48/R48R2 引継ぎハッシュ、追跡済み変更なしを検証する。
- テスト: 新規 `tests/test_static.py`・`tests/test_guard.py`・`tests/test_frontier.py`、既存 R48/R30/R29/R37 限定回帰。
- 出典順守: Toda Proposition 2.7 の一般 `GIVEN` のみ。一般命題、$n=6$ 型付き命題、上側の $\Delta$ 全射性はすべて独立の `INFERENCE`。
- 禁止事項: 新しい直接 `GIVEN`、専用数学規則、既存検索や共通 Renderer の変更、保存済みステップの注入、唯一性探索、全体 pytest。
- 完了条件: R30 の既存一般 Provider から出典付き3階層の証明が存在し、R37 の4前提から上側 $\Delta$ 全射性が `INFERENCE` となり、根の完全性 Goal で意図的に停止する。最終群は未完成維持。
- 次工程: R50 で根の Proposition 4.2 の2つの完全性、最後の零群 Goal を個別監査する。
