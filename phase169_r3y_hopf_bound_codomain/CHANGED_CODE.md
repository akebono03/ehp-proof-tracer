# R3Y コード変更一覧

- `phase165_r3_recursive_search.py`: `GoalExpansion` の直後に新規クラス `SourceBoundGoal` を追加。`reconstruct_registered_goal()` 全体を置換。
- `phase165_r14_r5_ehp_connection.py`: `expand_cited_ehp_terminal_goal()` 全体を置換。
- 既存 R3I / R3I1 / R3I2 の各テストファイル: テスト関数4件を全文置換。
- 新規 `tests/test_phase169_r3y_hopf_bound_codomain.py`: テスト4件と fixture 1件を追加。
- 既存 import 節の変更はありません。新たな import は変更済み関数の内部で全て記載しています。

各関数・クラスの置換全文は `full_functions/` にあります。各変更ファイル全文は適用時に `output/` に出力されます。
