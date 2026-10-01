Phase 154-R6-1 Repair2 — Idempotent Resume

原因
----
Repair1 は production と最初の test を更新した後、
別 test が R6-1 初回ですでに `。` へ更新済みだったため停止した。

つまり code の不整合ではなく、apply script が
「必ず旧 `.` が存在する」と仮定していたことが原因。

Repair2
-------
旧 pattern があれば更新する。
新 pattern がすでにあれば `already-current` としてそのまま進む。

変更対象 production
-------------------
`toda_group_proof_narrative_reason_renderer.py`

変更関数:
`render_toda_group_proof_narrative_reason_sentence`

変更箇所:
- MULTIPLE_RELATION_TO_ORDER
- FINAL_GROUP_STRUCTURE

import 変更
-----------
なし。

変更対象 tests
--------------
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py
- tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py
- tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py

新規:
- tests/test_phase154_r6_1_repair2_idempotent_resume.py

低レベル R2 Fix3 contract
-------------------------
`suppress_toda_group_proof_narrative_reference_body_duplicates`
自体の入力用 statement `...である.` は変更しない。
public Narrative expectation だけ current punctuation に合わせる。

完了条件
--------
- focused tests PASS
- TOTAL ascii_period_sentence_endings: 0
- comma は R6-2 用に残す

全体テスト
----------
実行しない。Phase 154 最後にのみ実行する。

次
----
Phase 154-R6-2:
prose separator comma `,` -> `、`
