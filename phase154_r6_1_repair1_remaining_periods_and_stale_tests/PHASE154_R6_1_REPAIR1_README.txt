Phase 154-R6-1 Repair1

状況
----
R6-1 初回:
- 27 passed
- 5 failed

失敗の内訳:
1. production:
   `toda_group_proof_narrative_reason_renderer.py`
   に日本語 prose 文末 `.` が2行残存。
2. stale tests:
   R2 の4 assertion が旧 punctuation `.` を期待。

変更対象
--------
production:
- toda_group_proof_narrative_reason_renderer.py
  - `render_toda_group_proof_narrative_reason_sentence`
  - MULTIPLE_RELATION_TO_ORDER の文末
  - FINAL_GROUP_STRUCTURE の群位数文末

tests:
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py

新規:
- tests/test_phase154_r6_1_repair1_remaining_periods.py

import 変更
-----------
なし。

低レベル contract
-----------------
`tests/test_phase154_r2_fix3_reference_marker_completion.py` の
`suppress_toda_group_proof_narrative_reference_body_duplicates`
単体テストは変更しない。

R6-1 の current public contract
-------------------------------
- 日本語 Narrative prose 文末は `。`
- Reference title period は維持
- comma normalization はまだ行わない

完了条件
--------
- focused tests PASS
- 5代表群で `TOTAL ascii_period_sentence_endings: 0`
- `TOTAL ascii_comma_prose_lines` は R6-2 用に残る

全体テスト
----------
実行しない。Phase 154 最後にのみ実行する。

次
----
R6-1 完了後、Phase 154-R6-2:
prose separator comma `,` -> `、`
