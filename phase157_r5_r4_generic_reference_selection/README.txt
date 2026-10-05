Phase157-R5-R4 — generic Reference selection

変更対象:
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_contribution_renderer.py
- toda_group_proof_narrative_renderer.py
- tests/test_phase157_r5_r4_generic_reference_selection.py

変更内容:
- R4 representative-only filter/restore は互換性のため残す。
- 新しい generic filter/restore を追加する。
- renderer / contribution renderer の production path は generic helper を使う。
- PROOF_INTERNAL / UNTRACKED / component_key=None aggregate は Reference から除外する。
- same-theorem fixed component ordering は既存 eligibility helper を使う。

import 変更:
- toda_group_proof_narrative_contribution_renderer.py
- toda_group_proof_narrative_renderer.py

apply 後の import block 全文:
phase157_r5_r4_output/
- contribution_reference_import_after.txt
- renderer_reference_import_after.txt

今回しないこと:
- 112群再監査（R5-R5）
- 112群 full Narrative
- repository-wide pytest
- proof graph の変更
- theorem data の変更

focused tests:
- R5-R4 generic helper
- R5-R3 catalog
- R4 helper compatibility
- R4-R2 catalog
- R2 boundary
- Phase153 selector

次:
Phase157-R5-R5 で112群 cross-audit を再実行する。
