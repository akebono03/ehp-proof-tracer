# Phase 165 R5-R5 補助 Renderer 呼び出し監査

状態: **REVIEW_REQUIRED**（監査結果の人手レビューが必要）

基準 R5-R2: `STATIC_PASS_REVIEW_REQUIRED`

## 件数

- candidates: 26
- candidate_independent_entries: 4
- called_helpers_for_review: 16
- no_direct_caller_for_review: 6
- parse_errors: 0

## 候補ごとの分類

### `phase162_r3_narrative_connection.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_phase162_r3_narrative`
- 直接呼出元: `phase162_web_narrative_integration.py`, `tests/test_phase162_r3_narrative_connection.py`
- 呼出箇所: `phase162_web_narrative_integration.py:297`→`render_phase162_r3_narrative`, `tests/test_phase162_r3_narrative_connection.py:41`→`render_phase162_r3_narrative`, `tests/test_phase162_r3_narrative_connection.py:52`→`render_phase162_r3_narrative`, `tests/test_phase162_r3_narrative_connection.py:62`→`render_phase162_r3_narrative`, `tests/test_phase162_r3_narrative_connection.py:73`→`render_phase162_r3_narrative`, `tests/test_phase162_r3_narrative_connection.py:81`→`render_phase162_r3_narrative`, `tests/test_phase162_r3_narrative_connection.py:100`→`render_phase162_r3_with_public_references`

### `phase165_r57_r10_step_narrative.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_completed_from_proofsteps`
- 直接呼出元: `phase165_r56_presentation_adapter.py`, `toda_group_proof_narrative_renderer.py`
- 呼出箇所: `phase165_r56_presentation_adapter.py:67`→`has_transport_proof_ancestry`, `phase165_r56_presentation_adapter.py:70`→`render_completed_from_proofsteps`, `toda_group_proof_narrative_renderer.py:11854`→`ordered_proof_ancestry`

### `phase165_r57_r2_partial_narrative.py`

- 判定: `POTENTIAL_INDEPENDENT_ENTRY`
- 定義: `render_incomplete_public_narrative`
- 直接呼出元: `toda_group_proof_narrative_renderer.py`
- 呼出箇所: `toda_group_proof_narrative_renderer.py:11776`→`render_incomplete_public_narrative`

### `toda_full_proof_report_renderer.py`

- 判定: `NO_DIRECT_CALL_FOUND_REVIEW`
- 定義: `render_toda_full_proof_report_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_group_proof_aggregate_statement_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_aggregate_statement_prose`
- 直接呼出元: `toda_group_proof_generic_narrative_renderer.phase165_r42_backup.py`, `toda_group_proof_generic_narrative_renderer.phase165_r48_backup.py`, `toda_group_proof_generic_narrative_renderer.phase165_r48_sidecar_backup.py`, `toda_group_proof_narrative_shared_components.py`
- 呼出箇所: `toda_group_proof_generic_narrative_renderer.phase165_r42_backup.py:1237`→`render_toda_group_proof_aggregate_statement_prose`, `toda_group_proof_generic_narrative_renderer.phase165_r48_backup.py:1260`→`render_toda_group_proof_aggregate_statement_prose`, `toda_group_proof_generic_narrative_renderer.phase165_r48_sidecar_backup.py:1260`→`render_toda_group_proof_aggregate_statement_prose`, `toda_group_proof_narrative_shared_components.py:1269`→`render_toda_group_proof_aggregate_statement_prose`

### `toda_group_proof_generic_narrative_renderer.phase165_r42_backup.py`

- 判定: `NO_DIRECT_CALL_FOUND_REVIEW`
- 定義: `render_toda_group_proof_generic_narrative_markdown`, `render_toda_group_proof_generic_proof_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_group_proof_generic_narrative_renderer.phase165_r48_backup.py`

- 判定: `NO_DIRECT_CALL_FOUND_REVIEW`
- 定義: `render_toda_group_proof_generic_narrative_markdown`, `render_toda_group_proof_generic_proof_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_group_proof_generic_narrative_renderer.phase165_r48_sidecar_backup.py`

- 判定: `NO_DIRECT_CALL_FOUND_REVIEW`
- 定義: `render_toda_group_proof_generic_narrative_markdown`, `render_toda_group_proof_generic_proof_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_group_proof_narrative_argument_body_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_argument_body_markdown`
- 直接呼出元: `audit_phase144_6_r5_24.py`, `audit_phase144_6_r5_33.py`, `tests/test_phase143_42_argument_body_contribution_renderer.py`, `toda_group_proof_narrative_argument_multi_renderer.py`, `toda_group_proof_narrative_argument_single_renderer.py`
- 呼出箇所: `audit_phase144_6_r5_24.py:252`→`render_toda_group_proof_narrative_argument_body_markdown`, `audit_phase144_6_r5_33.py:142`→`render_toda_group_proof_narrative_argument_body_markdown`, `tests/test_phase143_42_argument_body_contribution_renderer.py:122`→`render_toda_group_proof_narrative_argument_body_markdown`, `tests/test_phase143_42_argument_body_contribution_renderer.py:165`→`render_toda_group_proof_narrative_argument_body_markdown`, `tests/test_phase143_42_argument_body_contribution_renderer.py:198`→`render_toda_group_proof_narrative_argument_body_markdown`, `tests/test_phase143_42_argument_body_contribution_renderer.py:230`→`render_toda_group_proof_narrative_argument_body_markdown`, `tests/test_phase143_42_argument_body_contribution_renderer.py:271`→`render_toda_group_proof_narrative_argument_body_markdown`, `tests/test_phase143_42_argument_body_contribution_renderer.py:358`→`render_toda_group_proof_narrative_argument_body_markdown`, `tests/test_phase143_42_argument_body_contribution_renderer.py:391`→`render_toda_group_proof_narrative_argument_body_markdown`, `toda_group_proof_narrative_argument_multi_renderer.py:498`→`render_toda_group_proof_narrative_argument_body_markdown`, `toda_group_proof_narrative_argument_multi_renderer.py:606`→`_toda_group_proof_narrative_exactness_contribution_key`, `toda_group_proof_narrative_argument_single_renderer.py:102`→`render_toda_group_proof_narrative_argument_body_markdown`

### `toda_group_proof_narrative_argument_discourse.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_argument_discourse_marker`
- 直接呼出元: `audit_phase144_6_r5_32.py`, `audit_phase144_6_r5_43_11b.py`, `audit_phase144_6_r5_43_11d.py`, `tests/test_phase143_34_argument_header_method.py`, `toda_group_proof_narrative_argument_multi_renderer.py`, `toda_group_proof_narrative_argument_renderer.py`, `toda_group_proof_narrative_contribution_renderer.py`
- 呼出箇所: `audit_phase144_6_r5_32.py:68`→`classify_toda_group_proof_narrative_argument_discourse_roles`, `audit_phase144_6_r5_43_11b.py:63`→`classify_toda_group_proof_narrative_argument_discourse_roles`, `audit_phase144_6_r5_43_11d.py:103`→`classify_toda_group_proof_narrative_argument_discourse_roles`, `tests/test_phase143_34_argument_header_method.py:51`→`classify_toda_group_proof_narrative_argument_discourse_roles`, `toda_group_proof_narrative_argument_multi_renderer.py:244`→`classify_toda_group_proof_narrative_argument_discourse_roles`, `toda_group_proof_narrative_argument_renderer.py:155`→`render_toda_group_proof_narrative_argument_discourse_marker`, `toda_group_proof_narrative_contribution_renderer.py:3380`→`classify_toda_group_proof_narrative_argument_discourse_roles`

### `toda_group_proof_narrative_argument_multi_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_multi_argument_markdown`
- 直接呼出元: `audit_phase144_6_r5_21.py`, `audit_phase144_6_r5_23.py`, `audit_phase144_6_r5_24.py`, `audit_phase144_6_r5_25.py`, `audit_phase144_6_r5_26.py`, `audit_phase144_6_r5_27.py`, `audit_phase144_6_r5_31.py`, `audit_phase144_6_r5_32.py`, `audit_phase144_6_r5_34.py`, `audit_phase144_6_r5_36.py`, `audit_phase144_6_r5_37.py`, `audit_phase144_6_r5_38.py`, `audit_phase144_6_r5_43_1.py`, `audit_phase144_6_r5_43_11.py`, `audit_phase144_6_r5_43_11a.py`, `audit_phase144_6_r5_43_11b.py`, `audit_phase144_6_r5_43_11d.py`, `audit_phase144_6_r5_43_3.py`, `audit_phase144_6_r5_43_5.py`, `audit_phase144_6_r5_43_6.py`, `audit_phase144_6_r5_43_8.py`, `tests/test_phase143_46_multi_argument_narrative_assembler.py`, `tests/test_phase143_47_multi_argument_shared_contribution_dedup.py`, `tests/test_phase143_49_dependency_label_narrative_policy.py`, `tests/test_phase143_50_generic_statement_prose_renderer.py`, `tests/test_phase143_51a_r_provenance_semantic_catalog.py`, `tests/test_phase143_51b_aggregate_statement_prose.py`, `tests/test_phase143_53b_r_conclusion_aware_connector.py`, `tests/test_phase143_53b_transition_connectors.py`, `tests/test_phase143_55b_conclusion_step_ordering.py`, `tests/test_phase143_57c_step_derivation_connector.py`, `tests/test_phase143_58a_negative_scalar_sum.py`, `tests/test_phase143_59b_group_structure_duplicate_suppression.py`, `tests/test_phase143_61b_direct_premise_narrative.py`, `tests/test_phase143_61b_r_semantic_suppression_priority.py`, `tests/test_phase143_63a_r_exactness_repair.py`, `tests/test_phase143_63a_residual_fallback_provenance.py`, `tests/test_phase143_71a_eta_definition_visibility.py`, `tests/test_phase144_5_generic_definition_order_equations.py`, `tests/test_phase144_6_pi6_generic_production_route.py`, `tests/test_phase144_6_r25_9a_pi5_suppression.py`, `tests/test_phase144_6_r25_9a_r1_relocation_hidden.py`, `tests/test_phase144_6_r4_supporting_fact_filtering.py`, `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py`, `tests/test_phase146_7_generic_argument_purpose_prose.py`, `tests/test_phase148_rc2_3_exactness_exposure.py`, `tests/test_phase148_rc2_3_repair_r1.py`, `tests/test_phase148_rc2_4_cross_group_audit.py`, `tests/test_phase148_rc2_4_repair_r1_exposure_path_audit.py`, `tests/test_phase148_rc2_4_repair_r2.py`, `tests/test_phase149_rc3_3_minimal_ordering.py`, `tests/test_phase158_r5_4_repair_common_equation_numbering.py`, `tests/test_phase159_pi4_3_contribution_connector_ownership.py`, `tests/test_phase159_pi4_3_trailing_premise_order.py`, `toda_group_proof_narrative_contribution_ordering.py`, `toda_group_proof_narrative_contribution_renderer.py`, `toda_group_proof_narrative_proof_chain_renderer.py`
- 呼出箇所: `audit_phase144_6_r5_21.py:190`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_23.py:138`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_24.py:113`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_24.py:241`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_25.py:194`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_26.py:101`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_26.py:205`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_27.py:106`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_27.py:194`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_27.py:251`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_31.py:136`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_31.py:226`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_32.py:105`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_34.py:69`→`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`, `audit_phase144_6_r5_36.py:80`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_36.py:163`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_37.py:83`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_38.py:106`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_43_1.py:39`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_43_11.py:71`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_43_11a.py:91`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_43_11a.py:358`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_43_11b.py:40`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_43_11d.py:67`→`render_toda_group_proof_narrative_multi_argument_markdown`, `audit_phase144_6_r5_43_3.py:160`→`render_toda_group_proof_narrative_multi_argument_markdown`
- 記録省略: 11件（JSON にも上限あり）

### `toda_group_proof_narrative_argument_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_argument_purpose_sentence`, `render_toda_group_proof_narrative_argument_header_method_section`
- 直接呼出元: `tests/test_phase143_34_argument_header_method.py`, `toda_group_proof_narrative_argument_multi_renderer.py`, `toda_group_proof_narrative_argument_single_renderer.py`, `toda_group_proof_narrative_contribution_renderer.py`
- 呼出箇所: `tests/test_phase143_34_argument_header_method.py:106`→`render_toda_group_proof_narrative_argument_header_method_section`, `tests/test_phase143_34_argument_header_method.py:276`→`render_toda_group_proof_narrative_argument_header_method_section`, `toda_group_proof_narrative_argument_multi_renderer.py:431`→`render_toda_group_proof_narrative_argument_header_method_section`, `toda_group_proof_narrative_argument_single_renderer.py:89`→`render_toda_group_proof_narrative_argument_header_method_section`, `toda_group_proof_narrative_contribution_renderer.py:180`→`render_toda_group_proof_narrative_argument_purpose_sentence`, `toda_group_proof_narrative_contribution_renderer.py:4000`→`render_toda_group_proof_narrative_argument_purpose_sentence`

### `toda_group_proof_narrative_argument_single_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_single_argument_markdown`
- 直接呼出元: `tests/test_phase143_44_single_argument_narrative_renderer.py`, `toda_group_proof_narrative_argument_multi_renderer.py`
- 呼出箇所: `tests/test_phase143_44_single_argument_narrative_renderer.py:89`→`render_toda_group_proof_narrative_single_argument_markdown`, `tests/test_phase143_44_single_argument_narrative_renderer.py:297`→`render_toda_group_proof_narrative_single_argument_markdown`, `toda_group_proof_narrative_argument_multi_renderer.py:438`→`_normalize_toda_group_proof_narrative_argument_header_spacing`

### `toda_group_proof_narrative_concrete_transport.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_concrete_transport_proof_from_steps`
- 直接呼出元: `tests/test_phase162_r4_b3_common_renderer_fix.py`
- 呼出箇所: `tests/test_phase162_r4_b3_common_renderer_fix.py:27`→`render_concrete_transport_proof_from_steps`, `tests/test_phase162_r4_b3_common_renderer_fix.py:37`→`render_concrete_transport_proof_from_steps`

### `toda_group_proof_narrative_contribution_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`
- 直接呼出元: `audit_phase144_6_r5_43_1.py`, `audit_phase144_6_r5_43_11.py`, `audit_phase144_6_r5_43_11a.py`, `audit_phase144_6_r5_43_11b.py`, `audit_phase144_6_r5_43_11d.py`, `audit_phase144_6_r5_43_3.py`, `audit_phase144_6_r5_43_5.py`, `audit_phase144_6_r5_43_6.py`, `audit_phase144_6_r5_43_8.py`, `tests/test_phase144_6_public_route_cutover.py`, `tests/test_phase144_6_r4_supporting_fact_filtering.py`, `tests/test_phase150_rc4_5_visible_reasons.py`, `tests/test_phase150_rc4_5c_2_exactness_to_map_property.py`, `tests/test_phase150_rc4_5d_3_multiple_relation_to_order.py`, `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`, `tests/test_phase150_rc4_5f_2_final_group_structure_reason.py`, `tests/test_phase150_rc4_7d_generic_reason_vocabulary.py`, `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`, `tests/test_phase156_r6_3_reason_prose_canonicalization.py`, `tests/test_phase159_exactness_connector_normalization.py`, `tests/test_phase159_pi4_3_contribution_connector_ownership.py`, `tests/test_phase159_pi4_3_exactness_reason_unification.py`, `tests/test_phase159_pi4_3_exactness_surjectivity_unification.py`, `tests/test_phase159_pi4_3_trailing_premise_order.py`, `tests/test_phase159_pi6_3_zero_map_reason_order.py`, `tests/test_phase159_r1_7c_r4_exact_sequence_late_prefix_suppression_repair2.py`, `tests/test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py`, `toda_group_proof_narrative_renderer.phase165_r43_backup.py`, `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`, `toda_group_proof_narrative_renderer.phase165_r48_backup.py`, `toda_group_proof_narrative_renderer.py`
- 呼出箇所: `audit_phase144_6_r5_43_1.py:54`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `audit_phase144_6_r5_43_11.py:85`→`_contribution_insertion_indices`, `audit_phase144_6_r5_43_11.py:92`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `audit_phase144_6_r5_43_11.py:99`→`_contribution_connector_lines`, `audit_phase144_6_r5_43_11a.py:108`→`_contribution_insertion_indices`, `audit_phase144_6_r5_43_11a.py:167`→`_provider_anchor_index`, `audit_phase144_6_r5_43_11b.py:54`→`_contribution_insertion_indices`, `audit_phase144_6_r5_43_11d.py:81`→`_contribution_insertion_indices`, `audit_phase144_6_r5_43_11d.py:88`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `audit_phase144_6_r5_43_11d.py:95`→`_contribution_connector_lines`, `audit_phase144_6_r5_43_3.py:175`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `audit_phase144_6_r5_43_3.py:182`→`_contribution_insertion_indices`, `audit_phase144_6_r5_43_5.py:265`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `audit_phase144_6_r5_43_6.py:190`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `audit_phase144_6_r5_43_8.py:201`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `tests/test_phase144_6_public_route_cutover.py:32`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `tests/test_phase144_6_r4_supporting_fact_filtering.py:71`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `tests/test_phase150_rc4_5_visible_reasons.py:49`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `tests/test_phase150_rc4_5_visible_reasons.py:104`→`_toda_group_proof_narrative_reference_owned_step_ids`, `tests/test_phase150_rc4_5_visible_reasons.py:149`→`_toda_group_proof_narrative_reference_owned_step_ids`, `tests/test_phase150_rc4_5c_2_exactness_to_map_property.py:120`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `tests/test_phase150_rc4_5d_3_multiple_relation_to_order.py:59`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py:74`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `tests/test_phase150_rc4_5f_2_final_group_structure_reason.py:138`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`, `tests/test_phase150_rc4_7d_generic_reason_vocabulary.py:6`→`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`
- 記録省略: 40件（JSON にも上限あり）

### `toda_group_proof_narrative_exactness_method_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_exactness_method_transition`, `render_toda_group_proof_narrative_exactness_method_component_latex`
- 直接呼出元: `tests/test_phase143_30_exactness_method_transition.py`, `tests/test_phase143_32_exactness_component_latex.py`, `toda_group_proof_narrative_argument_renderer.py`, `toda_group_proof_narrative_renderer.phase165_r43_backup.py`, `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`, `toda_group_proof_narrative_renderer.phase165_r48_backup.py`, `toda_group_proof_narrative_renderer.py`
- 呼出箇所: `tests/test_phase143_30_exactness_method_transition.py:86`→`render_toda_group_proof_narrative_exactness_method_transition`, `tests/test_phase143_30_exactness_method_transition.py:185`→`render_toda_group_proof_narrative_exactness_method_transition`, `tests/test_phase143_30_exactness_method_transition.py:201`→`render_toda_group_proof_narrative_exactness_method_transition`, `tests/test_phase143_32_exactness_component_latex.py:105`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `tests/test_phase143_32_exactness_component_latex.py:127`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `tests/test_phase143_32_exactness_component_latex.py:188`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `tests/test_phase143_32_exactness_component_latex.py:209`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `tests/test_phase143_32_exactness_component_latex.py:228`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `tests/test_phase143_32_exactness_component_latex.py:245`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `toda_group_proof_narrative_argument_renderer.py:165`→`render_toda_group_proof_narrative_exactness_method_transition`, `toda_group_proof_narrative_argument_renderer.py:219`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `toda_group_proof_narrative_renderer.phase165_r43_backup.py:6123`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py:6123`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `toda_group_proof_narrative_renderer.phase165_r48_backup.py:6123`→`render_toda_group_proof_narrative_exactness_method_component_latex`, `toda_group_proof_narrative_renderer.py:6121`→`render_toda_group_proof_narrative_exactness_method_component_latex`

### `toda_group_proof_narrative_proof_chain_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 直接呼出元: `audit_phase144_6_r5_20.py`, `audit_phase144_6_r5_21.py`, `audit_phase144_6_r5_23.py`, `audit_phase144_6_r5_24.py`, `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py`
- 呼出箇所: `audit_phase144_6_r5_20.py:397`→`render_toda_group_proof_narrative_from_proof_chains_markdown`, `audit_phase144_6_r5_21.py:171`→`render_toda_group_proof_narrative_from_proof_chains_markdown`, `audit_phase144_6_r5_23.py:148`→`render_toda_group_proof_narrative_from_proof_chains_markdown`, `audit_phase144_6_r5_24.py:190`→`render_toda_group_proof_narrative_from_proof_chains_markdown`, `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:41`→`render_toda_group_proof_narrative_from_proof_chains_markdown`, `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:116`→`render_toda_group_proof_narrative_from_proof_chains_markdown`, `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:145`→`render_toda_group_proof_narrative_from_proof_chains_markdown`, `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:177`→`render_toda_group_proof_narrative_from_proof_chains_markdown`, `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:201`→`render_toda_group_proof_narrative_from_proof_chains_markdown`

### `toda_group_proof_narrative_reason_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_reason_sentence`
- 直接呼出元: `phase162_r3g_existing_reason_bridge.py`, `phase162_r3h_reason_inventory.py`, `phase162_r3i_semantic_sidecar_audit.py`, `tests/test_phase150_rc4_5_visible_reasons.py`, `tests/test_phase150_rc4_5b_3_reference_binding.py`, `tests/test_phase150_rc4_5c_2_exactness_to_map_property.py`, `tests/test_phase150_rc4_5d_3_multiple_relation_to_order.py`, `tests/test_phase150_rc4_5f_2_final_group_structure_reason.py`, `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`, `tests/test_phase156_r6_3_reason_prose_canonicalization.py`, `tests/test_phase159_generic_zero_exactness_map_property.py`, `tests/test_phase159_pi4_3_exactness_reason_unification.py`, `tests/test_phase159_pi4_3_exactness_surjectivity_unification.py`, `tests/test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py`, `toda_group_proof_narrative_contribution_renderer.py`, `toda_group_proof_narrative_reason_renderer.py`
- 呼出箇所: `phase162_r3g_existing_reason_bridge.py:74`→`render_toda_group_proof_narrative_reason_sentence`, `phase162_r3h_reason_inventory.py:75`→`render_toda_group_proof_narrative_reason_sentence`, `phase162_r3i_semantic_sidecar_audit.py:67`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase150_rc4_5_visible_reasons.py:84`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase150_rc4_5_visible_reasons.py:159`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase150_rc4_5b_3_reference_binding.py:63`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase150_rc4_5c_2_exactness_to_map_property.py:115`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase150_rc4_5d_3_multiple_relation_to_order.py:58`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase150_rc4_5f_2_final_group_structure_reason.py:133`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py:47`→`_toda_group_proof_narrative_reason_insertion_index`, `tests/test_phase156_r6_3_reason_prose_canonicalization.py:61`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase159_generic_zero_exactness_map_property.py:160`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase159_generic_zero_exactness_map_property.py:198`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase159_generic_zero_exactness_map_property.py:239`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase159_pi4_3_exactness_reason_unification.py:142`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase159_pi4_3_exactness_reason_unification.py:212`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase159_pi4_3_exactness_surjectivity_unification.py:132`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py:46`→`render_toda_group_proof_narrative_reason_sentence`, `tests/test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py:85`→`render_toda_group_proof_narrative_reason_sentence`, `toda_group_proof_narrative_contribution_renderer.py:10400`→`insert_toda_group_proof_narrative_reason_prose`, `toda_group_proof_narrative_contribution_renderer.py:10572`→`order_toda_group_proof_narrative_injective_image_order_reason`, `toda_group_proof_narrative_contribution_renderer.py:10604`→`order_toda_group_proof_narrative_injective_image_order_reason`, `toda_group_proof_narrative_contribution_renderer.py:10705`→`order_toda_group_proof_narrative_injective_image_order_reason`, `toda_group_proof_narrative_contribution_renderer.py:10712`→`finalize_phase165_r49_typed_reason_order`, `toda_group_proof_narrative_reason_renderer.py:470`→`render_toda_group_proof_narrative_reason_sentence`

### `toda_group_proof_narrative_references.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_reference_entries_markdown`
- 直接呼出元: `phase162_r4_b3_renderer_audit.py`, `phase162_validated_proof_presentation.py`, `phase165_r14_r43_reference_reason.phase165_r44_removed.py`, `tests/test_phase144_6_r3_structured_references.py`, `tests/test_phase150_rc4_5_visible_reasons.py`, `tests/test_phase153_r3_3_reference_statement_selection.py`, `tests/test_phase153_r5_reference_selection.py`, `tests/test_phase156_r5_repair4_bridge_reference_inference.py`, `tests/test_phase157_r4_r3_reference_selection_integration.py`, `tests/test_phase157_r4_r3_repair1_reference_retention.py`, `tests/test_phase157_r5_r4_generic_reference_selection.py`, `toda_group_proof_narrative_concrete_transport.py`, `toda_group_proof_narrative_contribution_renderer.py`, `toda_group_proof_narrative_renderer.phase165_r43_backup.py`, `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`, `toda_group_proof_narrative_renderer.phase165_r48_backup.py`, `toda_group_proof_narrative_renderer.py`
- 呼出箇所: `phase162_r4_b3_renderer_audit.py:43`→`build_toda_group_proof_narrative_reference_entries`, `phase162_validated_proof_presentation.py:169`→`extract_toda_group_proof_step_literature_reference`, `phase162_validated_proof_presentation.py:183`→`TodaGroupProofNarrativeReferenceEntry`, `phase162_validated_proof_presentation.py:225`→`render_toda_group_proof_narrative_reference_entries_markdown`, `phase165_r14_r43_reference_reason.phase165_r44_removed.py:17`→`extract_toda_group_proof_step_literature_reference`, `tests/test_phase144_6_r3_structured_references.py:34`→`extract_toda_group_proof_step_literature_reference`, `tests/test_phase144_6_r3_structured_references.py:49`→`extract_toda_group_proof_step_literature_reference`, `tests/test_phase144_6_r3_structured_references.py:70`→`TodaGroupProofNarrativeReferenceEntry`, `tests/test_phase144_6_r3_structured_references.py:76`→`render_toda_group_proof_narrative_reference_entries_markdown`, `tests/test_phase150_rc4_5_visible_reasons.py:88`→`build_toda_group_proof_narrative_reference_entries`, `tests/test_phase150_rc4_5_visible_reasons.py:98`→`exclude_toda_group_proof_narrative_root_reference`, `tests/test_phase150_rc4_5_visible_reasons.py:133`→`build_toda_group_proof_narrative_reference_entries`, `tests/test_phase150_rc4_5_visible_reasons.py:143`→`exclude_toda_group_proof_narrative_root_reference`, `tests/test_phase153_r3_3_reference_statement_selection.py:33`→`TodaGroupProofNarrativeReferenceEntry`, `tests/test_phase153_r3_3_reference_statement_selection.py:54`→`select_toda_group_proof_narrative_reference_statement_steps`, `tests/test_phase153_r3_3_reference_statement_selection.py:94`→`select_toda_group_proof_narrative_reference_statement_steps`, `tests/test_phase153_r3_3_reference_statement_selection.py:145`→`select_toda_group_proof_narrative_reference_statement_steps`, `tests/test_phase153_r3_3_reference_statement_selection.py:190`→`select_toda_group_proof_narrative_reference_statement_steps`, `tests/test_phase153_r5_reference_selection.py:48`→`TodaGroupProofNarrativeReferenceEntry`, `tests/test_phase153_r5_reference_selection.py:63`→`select_toda_group_proof_narrative_reference_statement_steps`, `tests/test_phase153_r5_reference_selection.py:85`→`TodaGroupProofNarrativeReferenceEntry`, `tests/test_phase153_r5_reference_selection.py:94`→`select_toda_group_proof_narrative_reference_statement_steps`, `tests/test_phase153_r5_reference_selection.py:126`→`TodaGroupProofNarrativeReferenceEntry`, `tests/test_phase153_r5_reference_selection.py:149`→`select_toda_group_proof_narrative_reference_statement_steps`, `tests/test_phase153_r5_reference_selection.py:170`→`TodaGroupProofNarrativeReferenceEntry`
- 記録省略: 59件（JSON にも上限あり）

### `toda_group_proof_narrative_renderer.phase165_r43_backup.py`

- 判定: `POTENTIAL_INDEPENDENT_ENTRY`
- 定義: `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`

- 判定: `POTENTIAL_INDEPENDENT_ENTRY`
- 定義: `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_group_proof_narrative_renderer.phase165_r48_backup.py`

- 判定: `POTENTIAL_INDEPENDENT_ENTRY`
- 定義: `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_group_proof_narrative_transition_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_group_proof_narrative_transition_connector`
- 直接呼出元: `tests/test_phase150_rc4_7b_production_repair.py`, `toda_group_proof_narrative_argument_multi_renderer.py`
- 呼出箇所: `tests/test_phase150_rc4_7b_production_repair.py:48`→`render_toda_group_proof_narrative_transition_connector`, `tests/test_phase150_rc4_7b_production_repair.py:70`→`render_toda_group_proof_narrative_transition_connector`, `toda_group_proof_narrative_argument_multi_renderer.py:451`→`render_toda_group_proof_narrative_transition_connector`

### `toda_group_proof_outline_renderer.py`

- 判定: `NO_DIRECT_CALL_FOUND_REVIEW`
- 定義: `render_toda_group_proof_outline_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_group_result_proof_replay_renderer.py`

- 判定: `NO_DIRECT_CALL_FOUND_REVIEW`
- 定義: `render_toda_group_result_proof_replay_markdown`
- 直接呼出元: 検出なし
- 呼出箇所: 検出なし

### `toda_proof_narrative_renderer.py`

- 判定: `CALLED_HELPER_REVIEW`
- 定義: `render_toda_proof_statement_latex`, `render_toda_proof_step_mathematical_markdown`, `render_toda_readable_proof_narrative_markdown`
- 直接呼出元: `cli.py`, `main.py`, `phase162_r3e_structured_root_renderer.py`, `tests/test_phase109_31_known_group_replay_narrow_rendering.py`, `tests/test_phase111_8_symbolic_dimension_presentation.py`, `tests/test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py`, `tests/test_phase143_75ab3_whitehead_correction_rendering.py`, `tests/test_phase143_75ac4_hopf_odd_multiple_rendering.py`, `tests/test_phase143_75ad_double_suspension_rendering.py`, `tests/test_phase143_75t_toda58_equation_aggregate_semantic_rendering.py`, `tests/test_phase143_75w_toda54_bracket_up_to_sign_semantic_rendering.py`, `tests/test_phase143_75y_nu4_construction_semantic_rendering.py`, `toda_full_proof_report_renderer.py`, `toda_group_proof_aggregate_statement_renderer.py`, `toda_group_proof_generic_narrative_renderer.phase165_r42_backup.py`, `toda_group_proof_generic_narrative_renderer.phase165_r48_backup.py`, `toda_group_proof_generic_narrative_renderer.phase165_r48_sidecar_backup.py`, `toda_group_proof_narrative_concrete_transport.py`, `toda_group_proof_narrative_contribution_renderer.py`, `toda_group_proof_narrative_exactness_method_renderer.py`, `toda_group_proof_narrative_reason_renderer.py`, `toda_group_proof_narrative_renderer.phase165_r43_backup.py`, `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`, `toda_group_proof_narrative_renderer.phase165_r48_backup.py`, `toda_group_proof_narrative_renderer.py`, `toda_group_proof_narrative_shared_components.py`, `toda_group_proof_outline_renderer.py`, `toda_group_result_proof_replay_renderer.py`, `toda_group_structure_transport_reason.py`, `web_generator_execution.py`, `web_generator_exploration.py`, `web_generator_proof.py`, `web_group_proof_common.py`, `web_operation_query.py`, `web_operation_query_proof.py`
- 呼出箇所: `cli.py:115`→`render_toda_proof_statement_latex`, `main.py:817`→`render_toda_proof_statement_latex`, `main.py:837`→`render_toda_proof_statement_latex`, `main.py:885`→`render_toda_proof_statement_latex`, `main.py:982`→`render_toda_proof_statement_latex`, `main.py:984`→`render_toda_proof_statement_latex`, `main.py:1000`→`render_toda_proof_statement_latex`, `main.py:1034`→`render_toda_proof_statement_latex`, `main.py:1042`→`render_toda_proof_statement_latex`, `phase162_r3e_structured_root_renderer.py:57`→`render_toda_primary_group_latex`, `phase162_r3e_structured_root_renderer.py:59`→`render_toda_primary_group_latex`, `tests/test_phase109_31_known_group_replay_narrow_rendering.py:59`→`render_toda_proof_statement_latex`, `tests/test_phase109_31_known_group_replay_narrow_rendering.py:73`→`render_toda_proof_statement_latex`, `tests/test_phase109_31_known_group_replay_narrow_rendering.py:90`→`render_toda_proof_statement_latex`, `tests/test_phase111_8_symbolic_dimension_presentation.py:27`→`render_toda_primary_group_latex`, `tests/test_phase111_8_symbolic_dimension_presentation.py:55`→`render_toda_primary_group_latex`, `tests/test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py:17`→`render_toda_proof_statement_latex`, `tests/test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py:36`→`render_toda_proof_statement_latex`, `tests/test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py:53`→`render_toda_proof_statement_latex`, `tests/test_phase143_75ab3_whitehead_correction_rendering.py:17`→`render_toda_proof_statement_latex`, `tests/test_phase143_75ab3_whitehead_correction_rendering.py:36`→`render_toda_proof_statement_latex`, `tests/test_phase143_75ab3_whitehead_correction_rendering.py:52`→`render_toda_proof_statement_latex`, `tests/test_phase143_75ac4_hopf_odd_multiple_rendering.py:17`→`render_toda_proof_statement_latex`, `tests/test_phase143_75ac4_hopf_odd_multiple_rendering.py:35`→`render_toda_proof_statement_latex`, `tests/test_phase143_75ac4_hopf_odd_multiple_rendering.py:54`→`render_toda_proof_statement_latex`
- 記録省略: 294件（JSON にも上限あり）

## 注意

- Static direct imports and calls do not prove runtime reachability.
- Candidate list originates from the R5-R2 name-based discovery, not all Python render functions.
- An entry function is a review flag, not proof that it bypasses the canonical renderer.
- A helper call may be reached from a separate legacy route; call graphs require review.
- Historical Phase162 fixture failures remain unresolved; this package does not run them.
- No mathematical correctness or arbitrary (n,k) search completeness is certified.
