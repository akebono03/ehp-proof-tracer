# Phase 165-R55 変更内容・完了条件

- 変更：`phase165_r52_r4_flask_bridge.py` の `build_group_proof_progress_view()` を既存入口のまま接続変更。
- 変更：`templates/index.html` から R54 の独立した生成元入力フォームを削除。
- 新規：`phase165_r55_nk_only_goal.py` の `registered_group_goal_candidates()`、`search_group_from_registered_goal()`。
- 新規：`test_phase165_r55_nk_only_goal.py` の対象テスト４件。
- 既存の R54 POST API は互換性のため残すが、画面には表示しない。
- 固定文献命題の `Relation` を証明目標候補として参照する。証明前提としての使用は禁止し、既存の root screening に委ねる。
- 完了条件：n=2,k=1 を Web に入力したとき、候補が一意なら R53 の共通探索を実行し、その結果を Web に表示する。候補不足・競合では未完成を表示する。
- 次作業：証明全体を共通 Narrative 契約に接続する。R55 では Renderer を変更しない。
- テスト：`python -m pytest -q test_phase165_r55_nk_only_goal.py test_phase165_r54_explicit_web_goal.py`。全体 pytest は Phase 終了時のみ。
