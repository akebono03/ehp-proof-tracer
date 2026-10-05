Phase157-R3 repair3

目的:
- depth 3 の pi_6^3 で、presentation.nodes から外れた
  Proposition 5.3 の suspension isomorphism を、
  recursive proof graph から回収して proof body に表示する。
- Reference には戻さない。
- fixed statement selection や他群の挙動は変更しない。

Production:
- toda_group_proof_narrative_contribution_renderer.py
  - _phase157_r3_find_recursive_proof_step_by_rule_name() を追加
  - _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism() を全体置換

Tests:
- tests/test_phase157_r3_repair3_recursive_internal_recovery.py を追加
- 既存 Phase157-R2/R3 focused tests を再実行

Repository-wide pytest は Phase157 closure まで実行しない。
