Phase 154-R6-1 — Shared punctuation normalization implementation

変更対象
--------
- toda_group_proof_generic_narrative_renderer.py
- toda_group_proof_narrative_reason_renderer.py
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_argument_renderer.py
- toda_group_proof_narrative_exactness_method_renderer.py
- toda_group_proof_narrative_argument_body_renderer.py

新規 helper
-----------
`_normalize_toda_group_proof_narrative_sentence_endings`

追加位置:
`toda_group_proof_generic_narrative_renderer.py` の
`_render_generic_narrative_step` の直前。

変更関数
--------
- `_render_generic_narrative_step`
- `_generic_short_exact_sequence_reason_prose`
- `_generic_narrative_sentence_lead`
- `render_toda_group_proof_narrative_reason_sentence`
- `render_toda_group_proof_narrative_reference_entries_markdown`
- `render_toda_group_proof_narrative_argument_purpose_sentence`
- `render_toda_group_proof_narrative_argument_header_method_section`
- `render_toda_group_proof_narrative_exactness_method_transition`
- `_render_toda_group_proof_narrative_argument_exactness_body_block`
- `_insert_toda_group_proof_narrative_relocated_direct_premises`

import 変更
-----------
なし。

R6-1 の境界
------------
- 日本語 Narrative prose の文末 `.` -> `。`
- TeX 内部は変更しない
- Reference title の `Proposition 5.8.` 等は変更しない
- comma normalization は R6-2 に残す
- final-render blind replace は行わない

テスト
------
新規:
`tests/test_phase154_r6_1_shared_punctuation_normalization.py`

current-contract の exact punctuation expectation は、
今回の仕様変更に必要なものだけ `.` -> `。` に更新する。

完了条件
--------
- focused tests PASS
- 5代表群で `ascii_period_sentence_endings = 0`
- comma は残る
- Reference title period は維持

全体テスト
----------
実行しない。Phase 154 の最後にのみ実行する。

次
----
R6-2: prose separator comma `,` -> `、`
