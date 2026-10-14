# R57-R8 変更コード

変更対象：`phase165_r52_r9_shared_math.py::shared_expansion_provider()`、`phase165_r55_nk_only_goal.py::registered_group_goal_candidates()`。新規 `phase165_r57_r8_eta_specialization.py`（既存プロジェクト直下）。テスト `test_phase165_r57_r8_general_specialization.py`。

import：両既存ファイルでは変更しない。必要な import は関数内。既存 `shared_expansion_provider()` の変更後全文は `shared_expansion_provider.py.txt` に格納。新しい関数・クラスの全文は `phase165_r57_r8_eta_specialization.py`。テスト関数と import の全文は `test_phase165_r57_r8_general_specialization.py`。

現地の R55 が GitHub HEAD に存在しないため、インストーラはローカルの元関数の署名を AST で保持し、変更後の完全な関数を `INSTALLED_FUNCTIONS.md` に書く。異なる署名は自動変更せず停止する。
