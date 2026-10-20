# Phase 166 R3-C 変更箇所

- 既存 `phase165_r3_recursive_search.py`：import 全体と `reconstruct_registered_goal` 全体（インストールで保存される `INSTALLED_SOURCE.py.txt` を参照）。`_typed_reference_steps` は残すが使用しない。`GoalExpansion`、`RegisteredGoalUnresolved` など既存クラスは変更しない。
- 新規 `phase166_r3c_ordered_search/phase166_r3c_ordered_search.py`：`ordered_fixed_reference_steps` を新規追加（全文は同梱）。
- 新規 `phase166_r3c_ordered_search/install.py`：`install` 関数を新規追加（全文同梱）。
- 新規 `phase166_r3c_ordered_search/tests/test_phase166_r3c_ordered_search.py`：9件の限定テスト（全文と import 同梱）。
- `run.ps1`：限定テスト実行。

既存の `lookup_mode` 引数と `verified_assertion_ids` 引数は保持する。3経路の文献引用条件を同一の掲載順判定へ接続する。証明内部の再利用順序は対象外。R3-D の証明全体検証は先取りしない。

完了条件：限定9テスト PASS。全体 pytest は Phase 166 末尾のみ。
