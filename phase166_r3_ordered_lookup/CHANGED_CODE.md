# Phase 166 R3 — 変更一覧

対象の現行 GitHub ファイル・関連テストを確認した。

- 変更: `phase165_r52_r15_ordered_citation.py`。import 全文および `ordered_typed_reference_steps()` 全体をパッケージ内のファイルで置換。
- 変更: `phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py`。旧独立承認必須テストを合意済み順序ルールに合わせファイル全文置換。
- 新規: `phase166_r3_ordered_lookup/tests/test_phase166_r3_ordered_lookup.py`。ファイル先頭の import 全文、`_fixture()`、5個のテスト関数全文を収録。
- 新規: `phase166_r3_ordered_lookup/run.ps1`。置換前のバックアップと限定 pytest。
- 変更しない: `phase165_r3_recursive_search.py`、Web entry、`unified_statement_registry.py`、`sphere.db`、Renderer。

限定 pytest：`python -m pytest -q phase166_r3_ordered_lookup/tests/test_phase166_r3_ordered_lookup.py tests/test_phase163_r3_registry_validation.py`。

完了条件：限定テスト PASS、Web の $\pi_3^2$ 完全証明維持、順序未設定の整備方針確認。今回の実装は `typed_reference_ordered` のみであり R3 全体を閉じない。

次の境界：実際の Web 探索経路の同定、命題位置の登録、順序比較の統一、`sphere.db` からの Goal Builder は別工程。
