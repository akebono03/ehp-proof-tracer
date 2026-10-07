Phase 159 - pi_4^3 repair3c
Minimal production implementation

変更対象
--------
1. toda_group_proof_narrative_contribution_ordering.py
   - _anchored_chain_step_ids()
   - _necessity_for_chain()

2. toda_group_proof_generic_narrative_renderer.py
   - toda_rules import
   - _render_generic_narrative_statement_prose()

3. tests/test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py
   - 新規 focused regression tests

実装内容
--------
repair3b で確認した provider-anchor ancestry を generic contribution
selection に接続する。

- current provider anchor -> conclusion の downstream chain は維持
- provider anchor <- prerequisite の upstream ancestry を local body 内で追加
- upstream step が provider anchor の prerequisite である場合、
  necessity に provider anchor を記録
- TodaDeltaImageFreeCyclicStatement を
    Im Delta = Z{...}
  と semantic rendering
- TodaSuspensionKernelFreeCyclicStatement を
    ker E = Z{...}
  と semantic rendering

行わないこと
------------
- pi_4^3 rule-name hard-code
- build_toda_group_proof_narrative_arguments() の変更
- supporting_blocks の拡張
- Reference の変更
- public renderer 固有分岐の追加
- repository-wide pytest
- Phase 159 の closure

Focused pytest
--------------
tests/test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py
tests/test_phase143_39_exactness_contribution_ownership.py
tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py
tests/test_phase149_rc3_3_minimal_ordering.py

完了条件
--------
- pi_4^3 で Delta(iota_5), Im Delta, ker E, E surjective が
  ordered contributions に到達する
- Delta -> Im Delta -> ker E の依存順を維持する
- image/kernel が rule-name fallback ではなく semantic prose になる
- existing exactness ownership / generic contribution ordering /
  unowned-recursive hiding 契約が focused tests で維持される

次との境界
----------
repair3c は contribution production の修正まで。
public Narrative の最終 prose 順序・Reference linkage・重複抑制に残差がある場合は、
repair3d で public output を audit してから必要最小限を修正する。
