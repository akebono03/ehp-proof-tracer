Phase157-R4-R3 representative Reference selection integration

変更対象:
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_contribution_renderer.py
- toda_group_proof_narrative_renderer.py
- tests/test_phase157_r4_r3_reference_selection_integration.py

実装:
- 代表5群だけで Reference entry の proof_steps を
  FIXED_STATEMENT component に限定する。
- same-theorem group structure は target より前の component だけ許可する。
- component_key=None の aggregate は Reference に出さない。
- UNTRACKED / PROOF_INTERNAL は Reference に出さない。
- statement line 作成前に filtering するため、proof-internal step は
  Reference-owned body suppression の対象にもならない。

対象:
- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

境界:
- 112群全体への一般化は R5。
- 全体 pytest は Phase157 closure まで実行しない。
