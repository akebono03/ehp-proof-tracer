# Phase 165-R54 変更一覧・完了条件

- 既存変更: `web_app.py` の import 全体、および `create_app()` 全体（インストール後の `CHANGED_CODE.md` に全文出力）。
- 既存変更: `templates/index.html` の Group query 節へ明示的な目標入力フォームを追加。
- 新規: `phase165_r54_explicit_web_goal.py` の `parse_explicit_free_cyclic_eta_goal()` と `build_explicit_free_cyclic_eta_web_view()`。
- 新規テスト: `test_phase165_r54_explicit_web_goal.py` の4関数。
- 実行: `python -m pytest -q test_phase165_r54_explicit_web_goal.py`。全体 pytest は実行しない。
- 完了条件: Web から `(n,k,eta_n)` を受け、R53 と同じ `search_shared_group_goal()` を実行し、その実結果を共通 Renderer へ渡す。目標を証明済みの前提にしない。
- 境界: 自動群構造発見は変更しない。別の群構造や生成元を受ける一般パーサーは今後の作業。15 Step の数学的依存関係監査も別途必要。
