# Phase 165 R6-2 R4-R8 実装監査

変更対象: `phase165_r3_recursive_search.py` の import と `reconstruct_registered_goal()`。新規ファイル: `phase165_r6_2_r4_r8_dedup.py` の2関数。変更前に GitHub の現行探索器と関連テストを確認した。GitHub 側にはユーザー環境の最新パッチが反映されていない場合があるため、インストーラーは実ファイルの一致箇所と構文を検査する。

同一性条件は、同じ結論、同一の `GIVEN` ProofStep オブジェクト、2つの既知のスカラー特殊化 Rule Name、及び `specialize_typed_statement()` による数学的特殊化確認。異なる文献証人や独立した証明経路は統合しない。Rule Name は現行コードの安定 ID ではないため、将来の規則識別子整備では再監査が必要。

実行する pytest: `test_install.py`, `test_integration.py`, `tests/test_phase165_r3_recursive_search.py`。全体 pytest は行わない。

完了条件: この2経路の重複だけが1件として扱われ、独立な導出を保持し、正規探索の既存例が回帰しないこと。次段階: 公開 Narrative での参照と表示の検証。今回 Renderer は変更しない。
