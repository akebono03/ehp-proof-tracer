# Phase 164 R8-R1 — ProofStep 生成経路の棚卸し

- モード: 読み取り専用
- 全体 pytest: 未実施
- 解析した本番 Python ファイル数: 2995
- 構文エラー: 7

## 呼び出し分類

- copy_review: 2件
- dataclass_replace_review: 2856件
- direct_constructor: 618件
- inference_application: 90件

## 代表経路

- generator_replay: file=True, direct=0, inference=0
- operation_replay: file=True, direct=0, inference=0
- backward_reconstruction: file=True, direct=0, inference=2
- core_proof: file=True, direct=8, inference=2
- group_calculation: file=True, direct=0, inference=0

## 生成サイト例（各分類先頭15件）

### copy_review
- `phase155_closure/run_phase155_full_regression.py:56` — `main` / `copy`
- `phase155_closure_r2a_r1_reference_name_repair/run_phase155_closure_r2a_r1.py:47` — `main` / `copy`
### dataclass_replace_review
- `archive/phases/_root_files/apply_phase131_4.py:20` — `_replace_once` / `replace`
- `archive/phases/_root_files/apply_phase131_5.py:15` — `replace_once` / `replace`
- `archive/phases/_root_files/apply_phase132_7.py:25` — `replace_exact` / `replace`
- `archive/phases/_root_files/apply_phase132_8.py:28` — `replace_exact` / `replace`
- `archive/phases/_root_files/apply_phase132_9.py:24` — `replace_exact` / `replace`
- `archive/phases/phase143_10/apply_phase143_10.py:311` — `<module>` / `replace`
- `archive/phases/phase143_10/apply_phase143_10.py:312` — `<module>` / `replace`
- `archive/phases/phase143_10_fix1/apply_phase143_10_fix1.py:26` — `<module>` / `replace`
- `archive/phases/phase143_10_fix1/apply_phase143_10_fix1.py:70` — `<module>` / `replace`
- `archive/phases/phase143_10_fix2/apply_phase143_10_fix2.py:6` — `<module>` / `replace`
- `archive/phases/phase143_10_fix2/apply_phase143_10_fix2.py:100` — `<module>` / `replace`
- `archive/phases/phase143_12/apply_phase143_12.py:9` — `<module>` / `replace`
- `archive/phases/phase143_12/apply_phase143_12.py:90` — `<module>` / `replace`
- `archive/phases/phase143_12_fix1/apply_phase143_12_fix1.py:51` — `<module>` / `replace`
- `archive/phases/phase143_12_fix1/apply_phase143_12_fix1.py:159` — `<module>` / `replace`
### direct_constructor
- `archive/phases/phase130_8_backup/repository_symbolic_stable_group_specialization.py:238` — `specialize_toda_prop51_eta_index_step` / `ProofStep`
- `archive/phases/phase130_8_backup/repository_symbolic_stable_group_specialization.py:312` — `specialize_toda_prop53_eta_squared_index_step` / `ProofStep`
- `archive/phases/phase130_8_backup/repository_symbolic_stable_group_specialization.py:384` — `specialize_toda_prop56_nu_index_step` / `ProofStep`
- `audit_phase162_r3a_presentation.py:34` — `build_r2_fixture` / `ProofStep`
- `audit_phase162_r3a_presentation.py:35` — `build_r2_fixture` / `ProofStep`
- `diagnose_phase162_r3a_bridge.py:35` — `diagnose_bridge` / `ProofStep`
- `diagnose_phase162_r3a_bridge.py:35` — `diagnose_bridge` / `ProofStep`
- `hopf_rules.py:51` — `ehp_h_homomorphism_proof_step` / `ProofStep`
- `hopf_rules.py:161` — `hopf_invariant_proof_step` / `ProofStep`
- `map_facts.py:27` — `MapIsomorphismFact.to_proof_step` / `ProofStep`
- `phase153_r10_used_reference_filtering_backup/toda_group_proof_narrative_contribution_renderer.py:959` — `_phase153_r6_render_reference_statement` / `ProofStep`
- `phase153_r11_generic_reference_attribution_filtering_backup/toda_group_proof_narrative_contribution_renderer.py:960` — `_phase153_r6_render_reference_statement` / `ProofStep`
- `phase153_r12_root_reference_exclusion_across_routes_backup/toda_group_proof_narrative_contribution_renderer.py:971` — `_phase153_r6_render_reference_statement` / `ProofStep`
- `phase153_r7_backup_before_apply/toda_group_proof_narrative_contribution_renderer.py:953` — `_phase153_r6_render_reference_statement` / `ProofStep`
- `phase153_r7_independent_root_path_repair_r3_backup/toda_group_proof_narrative_contribution_renderer.py:953` — `_phase153_r6_render_reference_statement` / `ProofStep`
### inference_application
- `diagnose_phase162_r3a_bridge.py:43` — `diagnose_bridge` / `apply_inference_match`
- `phase157_r20_repair3_backup_20261004_102912/toda_prop58_zero_bootstrap.py:441` — `_build_equation57_steps` / `apply_inference_match`
- `phase159_r1_6a_backup_20261006_084251/proof.py:1042` — `apply_inference_matches` / `apply_inference_match`
- `phase159_r1_6a_backup_20261006_084251/proof.py:1065` — `apply_inference_matches_with_results` / `apply_inference_match`
- `phase159_r1_6a_backup_20261006_084251/toda_upstream_bootstrap.py:957` — `build_toda_53_nu_prime_steps` / `apply_inference_match`
- `phase159_r1_6a_backup_20261006_084251/toda_upstream_bootstrap.py:978` — `build_toda_53_nu_prime_steps` / `apply_inference_match`
- `phase159_r1_6b_backup_20261006_090001/toda_upstream_bootstrap.py:984` — `build_toda_53_nu_prime_steps` / `apply_inference_match`
- `phase159_r1_6b_backup_20261006_090001/toda_upstream_bootstrap.py:1005` — `build_toda_53_nu_prime_steps` / `apply_inference_match`
- `phase161_backward_type_closure_budget_fix/audit_phase161_backward_type_closure.py:180` — `execute_restricted_forward_chain` / `apply_inference_match`
- `phase161_backward_type_closure_probe/audit_phase161_backward_type_closure.py:152` — `execute_restricted_forward_chain` / `apply_inference_match`
- `phase161_backward_type_priority_probe/audit_phase161_backward_type_closure.py:191` — `execute_restricted_forward_chain` / `apply_inference_match`
- `phase161_conclusion_builder_validation/audit_phase161_conclusion_builder.py:63` — `examine_branch` / `apply_inference_match`
- `phase161_concrete_goal_filter_audit/audit_phase161_concrete_goal_filter.py:91` — `inspect_concrete_goal` / `apply_inference_match`
- `phase161_concrete_goal_filter_path_fix/audit_phase161_concrete_goal_filter.py:91` — `inspect_concrete_goal` / `apply_inference_match`
- `phase161_r4_r5_pi4_3_prop51_reference_linkage/backup_before_apply/toda_prop56_zero_bootstrap.py:181` — `_require_match` / `apply_inference_match`

## 判断の境界

- `ProofStep(...)` は直接生成候補である。
- `apply_inference_match(...)` は規則に基づく推論生成であり、単純なコンストラクタと統合しない。
- Replay は既存 ProofStep の identity（同一性）保持が必要であり、新規生成対象ではない。
- `dataclasses.replace` は他のデータクラスも対象とするため個別に確認する。
- 本結果は静的棚卸しであり、R8 の実装完了判定ではない。
