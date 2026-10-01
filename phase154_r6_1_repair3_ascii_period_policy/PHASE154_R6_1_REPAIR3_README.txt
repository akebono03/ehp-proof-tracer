Phase 154-R6-1 Repair3 — ASCII period policy

正しい punctuation policy
-------------------------
ユーザー指定:
- 読点: `,`
- 句点: `.`

R6-1 の担当範囲:
- sentence ending のみ `.` に統一する。
- comma は R6-2 に残す。

変更対象 production
-------------------
1. toda_group_proof_generic_narrative_renderer.py
   - `_normalize_toda_group_proof_narrative_sentence_endings`
   - `_generic_short_exact_sequence_reason_prose`
   - `_generic_narrative_sentence_lead`

2. toda_group_proof_narrative_reason_renderer.py
   - `render_toda_group_proof_narrative_reason_sentence`

3. toda_group_proof_narrative_references.py
   - `render_toda_group_proof_narrative_reference_entries_markdown`

4. toda_group_proof_narrative_argument_renderer.py
   - `render_toda_group_proof_narrative_argument_purpose_sentence`
   - `render_toda_group_proof_narrative_argument_header_method_section`

5. toda_group_proof_narrative_exactness_method_renderer.py
   - `render_toda_group_proof_narrative_exactness_method_transition`

6. toda_group_proof_narrative_argument_body_renderer.py
   - `_render_toda_group_proof_narrative_argument_exactness_body_block`
   - `_insert_toda_group_proof_narrative_relocated_direct_premises`

7. toda_group_proof_narrative_contribution_renderer.py
   - `suppress_toda_group_proof_narrative_reference_body_duplicates`
   - `link_toda_group_proof_narrative_reference_body_consumers`

8. toda_group_proof_narrative_renderer.py
   - `_append_narrative_for_step`
   - `render_toda_group_proof_narrative_markdown`
   - legacy Narrative sentence endings

import 変更
-----------
なし。

テスト
------
wrong-policy R6-1 tests を削除:
- tests/test_phase154_r6_1_shared_punctuation_normalization.py
- tests/test_phase154_r6_1_repair1_remaining_periods.py
- tests/test_phase154_r6_1_repair2_idempotent_resume.py

新規:
- tests/test_phase154_r6_1_repair3_ascii_period_policy.py

R2/R5 の current-contract punctuation expectation は
`。` から `.` に戻す。

完了条件
--------
- focused tests PASS
- 5代表群で `TOTAL japanese_period_sentence_endings: 0`
- ASCII period sentence endings が存在する
- Japanese comma `、` は R6-2 まで残る

全体テスト
----------
実行しない。Phase 154 最後にのみ実行する。

次
----
Phase 154-R6-2:
Japanese comma `、` -> ASCII comma `,`
