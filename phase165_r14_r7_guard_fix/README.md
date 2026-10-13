# Phase 165 R14-R7 match_guard API 修正

変更対象: `phase165_r14_r7_map_discovery.py` の `_check_inverse_transport()` 関数全文。

既存の `proof.py` において `match_guard(premises, bindings)`、`conclusion_builder(premises)` という別の契約であることを確認。`_check_inverse_transport` のみ2引数に変更。`_build_inverse_transport` は変更しない。その他の既存 API は保持。

テスト: `test_phase165_r14_r7_map_discovery.py` の既存8件、および `test_inverse_transport_match_guard_accepts_two_argument_api()`（新規1件）を実行。全体 pytest は実行しない。

完了条件: 9件の関連テスト成功、Hopf 写像候補1件、出典未確認の前提0件、ProofStep 生成0件。

R14-R8境界: Toda (5.1) と Hopf 生成元対応の出典照合・Registry 接続を別作業として行う。
