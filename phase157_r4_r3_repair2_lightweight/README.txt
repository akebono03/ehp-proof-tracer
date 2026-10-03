Phase157-R4-R3 repair2

原因:
- restore helper で (LiteratureReference, proof_steps) を set key にしたため、
  ProofStep dataclass の hash が premises を再帰的に hash し、
  深い proof graph で極端に重くなった。
- R4-R3 のテストが representative 5 groups の full Narrative を
  複数回生成しており、Phase155 の「重いテストを増やさない」方針に反していた。

変更:
1. toda_group_proof_narrative_references.py
   - restore helper の retained key を、
     reference locator / label + ProofStep identity(id) の tuple に変更。
   - ProofStep 本体を hash しない。

2. tests/test_phase157_r4_r3_reference_selection_integration.py
   - full Narrative 生成を廃止。
   - synthetic ProofStep を用いた boundary filter の unit test に置換。

3. tests/test_phase157_r4_r3_repair1_reference_retention.py
   - pi_12^5 full Narrative 生成を廃止。
   - restore helper の identity-based retention / marker renumbering を
     synthetic graph で直接検証する unit test に置換。

今回変更しない:
- toda_group_proof_narrative_renderer.py
- toda_group_proof_narrative_contribution_renderer.py
- Reference selection の意味論
- R4-R2 catalog

テスト:
- lightweight focused tests only
- representative full Narrative loop は実行しない
- repository-wide pytest は Phase157 closure まで実行しない
