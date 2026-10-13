# Phase 165 共通 Renderer 全体監査

## Scope and limits
読み取り専用 AST 監査。動的な実行順序、数学的正当性、Web 出力の完全性は別途実行時検証が必要。

## ファイル別機能と呼び出し

### `web_group_proof.py`
- 存在: True
- 行数: 764 / トップレベル定義: 10
- `_split_group_proof_rendered_line` L487–528; relevant calls: (none detected)
- `_build_group_proof_rendered_lines` L619–689; relevant calls: _split_group_proof_rendered_line@680, WebGroupProofRenderedLineView@681, WebGroupProofRenderedLineView@636, WebGroupProofRenderedLineView@664, WebGroupProofRenderedLineView@670, WebGroupProofRenderedLineView@645
- `build_standard_web_group_proof_view` L692–764; relevant calls: _build_group_proof_rendered_lines@751, render_toda_group_proof_outline_markdown@748, render_toda_group_proof_narrative_markdown@750

### `phase164_r5_r2_common_replay.py`
- 存在: True
- 行数: 23 / トップレベル定義: 1

### `toda_group_proof_presentation.py`
- 存在: True
- 行数: 181 / トップレベル定義: 2

### `toda_group_proof_narrative_renderer.py`
- 存在: True
- 行数: 12014 / トップレベル定義: 124
- **同名再定義: {'render_toda_group_proof_narrative_markdown': 3}**
- `_render_finite_dimensional_aggregate_statement_latex` L302–383; relevant calls: _render_scalar_latex@366, render_toda_raw_group_structure_latex@339, render_toda_primary_group_latex@350, _render_scalar_latex@362, render_toda_primary_group_latex@335
- `_render_prop44_suspension_injective_statement_latex` L388–408; relevant calls: render_toda_primary_group_latex@405, render_toda_primary_group_latex@401
- `_render_group_proof_narrative_latex` L410–815; relevant calls: _render_prop44_suspension_injective_statement_latex@425, _render_finite_dimensional_aggregate_statement_latex@438, render_toda_proof_statement_latex@812, render_repository_conclusion_latex@798, render_toda_expression_latex@508, render_toda_expression_latex@525, render_toda_expression_latex@540, render_toda_primary_group_latex@554, render_toda_primary_group_latex@589, render_toda_primary_group_latex@608, render_toda_primary_group_latex@623, render_toda_expression_latex@637, render_toda_primary_group_latex@652, render_toda_primary_group_latex@667, render_toda_raw_group_structure_latex@686, render_toda_raw_group_structure_latex@705, render_toda_raw_group_structure_latex@724, render_toda_primary_group_latex@743, render_toda_primary_group_latex@758, render_toda_expression_latex@777, _render_scalar_latex@791, _render_scalar_latex@456, _render_scalar_latex@492, render_toda_expression_latex@521
- `_render_group_proof_narrative_fact` L818–879; relevant calls: _render_generic_narrative_step@832, _render_group_proof_narrative_latex@858
- `_is_phase134_5_reference_step` L956–965; relevant calls: (none detected)
- `_phase134_5_pi6_3_reference_steps` L1029–1037; relevant calls: _phase134_9_reference_steps@1035
- `_phase134_5_reference_title` L1039–1060; relevant calls: (none detected)
- `_phase134_5_reference_statement_lines` L1063–1123; relevant calls: render_repository_conclusion_latex@1107, render_toda_primary_group_latex@1088, render_toda_primary_group_latex@1084, render_toda_expression_latex@1080
- `_is_phase134_9_reference_step` L1183–1197; relevant calls: (none detected)
- `_phase134_9_reference_steps` L1282–1299; relevant calls: _is_phase134_9_reference_step@1295
- `_phase134_3_reference_text` L1361–1376; relevant calls: (none detected)
- `_phase136_2_pi6_3_reference_blocks` L1439–1534; relevant calls: (none detected)
- `_phase136_pi6_3_reason_lead` L1625–1646; relevant calls: (none detected)
- `_phase134_28_reference_section_lines` L2222–2312; relevant calls: (none detected)
- `_render_phase134_3_pi6_3_narrative_markdown` L2404–2758; relevant calls: _phase134_5_pi6_3_reference_steps@2408, _render_group_proof_narrative_latex@2414, _phase136_2_pi6_3_reference_blocks@2465, _phase134_28_reference_section_lines@2469, _phase134_5_reference_title@2441, _phase134_5_reference_statement_lines@2459
- `_phase134_9_reference_title` L3032–3053; relevant calls: _phase134_5_reference_title@3051
- `_phase134_11_pi8_5_reference_steps` L3240–3284; relevant calls: (none detected)
- `_render_phase134_9_pi8_5_narrative_markdown` L3567–3716; relevant calls: _phase134_11_pi8_5_reference_steps@3577, _render_group_proof_narrative_latex@3609, _phase134_28_reference_section_lines@3640, _phase134_9_reference_title@3631
- `_phase134_24_render_pi15_8_narrative` L3718–3974; relevant calls: render_repository_conclusion_latex@3787, render_repository_conclusion_latex@3793, render_toda_primary_group_latex@3799, render_toda_primary_group_latex@3805, render_toda_primary_group_latex@3811, render_toda_expression_latex@3817, render_toda_expression_latex@3823, render_toda_expression_latex@3829, render_toda_expression_latex@3835, render_toda_expression_latex@3844, render_toda_expression_latex@3853, render_toda_expression_latex@3859, render_toda_raw_group_structure_latex@3865, render_repository_conclusion_latex@3871, _phase134_28_reference_section_lines@3888
- `_phase153_r3_10_connect_public_reference_section` L3976–4222; relevant calls: build_toda_group_proof_narrative_reference_entries@4018, filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary@4023, _toda_group_proof_narrative_reference_statement_lines_by_number@4033, filter_toda_group_proof_narrative_reference_entries_by_body_usage@4141, exclude_toda_group_proof_narrative_root_reference@4152, _toda_group_proof_narrative_reference_statement_lines_by_number@4170, suppress_toda_group_proof_narrative_reference_body_restatements@4177, render_toda_group_proof_narrative_reference_entries_markdown@4184, render_repository_conclusion_latex@4092
- `_phase157_r11_r17_normalize_public_connectors` L4322–4376; relevant calls: (none detected)
- `_phase157_r11_r17_normalize_public_numeric_equalities` L4379–4523; relevant calls: (none detected)
- `_normalize_toda_group_proof_narrative_display_closing_fragments` L4527–4587; relevant calls: (none detected)
- `_phase158_baseline_render_toda_group_proof_narrative_markdown` L4773–5053; relevant calls: exclude_toda_group_proof_narrative_root_reference@4860, render_toda_group_proof_narrative_reference_entries_markdown@4867, build_toda_group_proof_narrative_reference_reuse_marker_by_step_id@4878, render_toda_group_proof_narrative_multi_argument_with_contributions_markdown@4812, add_transport_link_to_common_markdown@4828, build_toda_group_proof_narrative_reference_entries@4842, _toda_group_proof_narrative_reference_statement_lines_by_number@4849, suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry@4987, suppress_toda_group_proof_narrative_reference_body_duplicates@4994, link_toda_group_proof_narrative_reference_body_consumers@5000, filter_toda_group_proof_narrative_reference_entries_by_body_usage@5011, render_toda_group_proof_narrative_reference_entries_markdown@5018, _render_group_proof_narrative_fact@4956, _render_group_proof_narrative_fact@4945
- `_phase158_render_public_equation_connector` L5225–5261; relevant calls: (none detected)
- `_phase158_normalize_public_equation_numbers` L5264–5516; relevant calls: _phase158_render_public_equation_connector@5421
- `_phase159_public_exactness_latex` L5968–5999; relevant calls: (none detected)
- `_phase159_consolidate_public_exactness_lines` L6002–6104; relevant calls: _phase159_public_exactness_latex@6011
- `_phase159_r1_7b_exactness_step_latex` L6367–6400; relevant calls: render_toda_proof_statement_latex@6379
- `_phase159_r1_7b_inline_exactness_latex` L6405–6459; relevant calls: (none detected)
- `_phase159_r1_7b_exactness_matches_map_property` L6594–6614; relevant calls: (none detected)
- `_phase159_r1_7b_normalize_public_exact_sequences` L6721–7042; relevant calls: canonical_exactness@6789, canonical_exactness@6812, _phase159_r1_7b_inline_exactness_latex@6859, canonical_exactness@6780, canonical_exactness@7002, canonical_exactness@6838, _phase159_r1_7b_exactness_step_latex@6755, canonical_typed_exactness@6867, _phase159_r1_7b_exactness_matches_map_property@6914
- `_phase159_r1_7c_r4_normalize_proof_body_prose` L7051–7142; relevant calls: (none detected)
- `_phase158_normalize_public_narrative_contract` L7145–7292; relevant calls: _phase158_normalize_public_equation_numbers@7241, _phase159_r1_7b_normalize_public_exact_sequences@7245, _phase159_r1_7c_r4_normalize_proof_body_prose@7256
- `_phase159_normalize_public_map_property_wording` L7349–7421; relevant calls: _render_generic_narrative_step@7400
- `_phase159_foundational_reference_statement` L7424–7448; relevant calls: _render_generic_narrative_step@7437
- `_phase159_render_foundational_reference_section` L7451–7580; relevant calls: _phase159_foundational_reference_statement@7563
- `_phase159_inject_foundational_reference_section` L7582–7653; relevant calls: _phase159_render_foundational_reference_section@7595
- `_phase159_normalize_public_reference_map_property_wording` L7655–7762; relevant calls: (none detected)
- `_phase159_r1_6c_step_reference_locator` L7877–7902; relevant calls: (none detected)
- `_phase159_r1_6c_reference_number` L7980–8017; relevant calls: (none detected)
- `_phase159_r1_6c_canonicalize_toda_51_reference` L8020–8131; relevant calls: (none detected)
- `_phase159_r1_6c_remove_redundant_exactness_sentence` L8134–8201; relevant calls: (none detected)
- `_phase159_r1_6c_render_statement_numbers` L8206–8262; relevant calls: (none detected)
- `_phase159_r1_6d_finalize_reference_and_linkage` L8427–8498; relevant calls: (none detected)
- `_phase159_r1_6d_reorder_target_group_fact_after_surjectivity` L8625–8797; relevant calls: render_toda_primary_group_latex@8662, _render_generic_narrative_step@8669
- `_phase159_r1_7c_preexisting_render_toda_group_proof_narrative_markdown` L8826–8889; relevant calls: _phase158_baseline_render_toda_group_proof_narrative_markdown@8830, _phase158_normalize_public_narrative_contract@8835, _phase159_normalize_public_map_property_wording@8841, _phase159_normalize_public_reference_map_property_wording@8847, _phase159_r1_6c_canonicalize_toda_51_reference@8852, _phase159_r1_6c_remove_redundant_exactness_sentence@8857, _phase159_r1_6c_render_statement_numbers@8862, _phase159_r1_6d_finalize_reference_and_linkage@8867, _phase159_r1_6d_reorder_target_group_fact_after_surjectivity@8878, _phase159_inject_foundational_reference_section@8885
- `_phase159_r1_7c_rendered_step_math_content` L8940–8975; relevant calls: _render_generic_narrative_step@8944
- `_phase159_r1_7c_rendered_equality_parts` L9010–9045; relevant calls: _phase159_r1_7c_rendered_step_math_content@9017
- `_phase159_r1_7c_reference_prefix` L9153–9177; relevant calls: (none detected)
- `_phase159_r1_7c_normalize_public_equality_chains` L9568–9614; relevant calls: (none detected)
- `_phase159_r1_7c_r4_normalize_public_map_property_prose` L9616–9780; relevant calls: (none detected)
- `_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning` L9891–10342; relevant calls: build_toda_group_proof_narrative_reason_sidecar@9949, _render_generic_narrative_group_map_latex@10002, append_exactness_connector@10263
- `_phase159_reorder_unique_preimage_definition_premise_locality` L10344–10599; relevant calls: _render_generic_narrative_step@10477
- `_phase159_r1_7c_r4_reorder_public_equation_reference_conclusions` L10602–10753; relevant calls: (none detected)
- `_phase159_render_pi_n_plus_1_n_stable_transport_narrative` L11104–11278; relevant calls: (none detected)
- `render_toda_group_proof_narrative_markdown` L11281–11328; relevant calls: _phase159_render_pi_n_plus_1_n_stable_transport_narrative@11285, _phase158_baseline_render_toda_group_proof_narrative_markdown@11294, _phase158_normalize_public_narrative_contract@11299, _phase159_r1_7c_r4_normalize_public_map_property_prose@11305, _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning@11310, _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions@11315, _phase159_r1_6d_finalize_reference_and_linkage@11321, _phase159_order_public_unique_preimage_definition_premises@11323
- `render_toda_group_proof_narrative_markdown` L11329–11365; relevant calls: _phase158_baseline_render_toda_group_proof_narrative_markdown@11333, _phase158_normalize_public_narrative_contract@11338, _phase159_reorder_unique_preimage_definition_premise_locality@11344, _phase159_r1_7c_r4_normalize_public_map_property_prose@11350, _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning@11355, _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions@11362
- `_phase160_r7_render_stable_finite_cyclic_transport_narrative` L11374–11989; relevant calls: render_toda_primary_group_latex@11473
- `render_toda_group_proof_narrative_markdown` L11991–12013; relevant calls: _phase160_r7_render_stable_finite_cyclic_transport_narrative@11995, _phase160_r7_previous_public_narrative_renderer@12003, normalize_public_narrative_contract@12008, suppress_toda_group_proof_narrative_dangling_connectors@12009

### `toda_group_proof_generic_narrative_renderer.py`
- 存在: True
- 行数: 2477 / トップレベル定義: 29
- `_render_generic_eta_composition_latex` L150–173; relevant calls: (none detected)
- `_normalize_generic_eta_family_latex` L176–330; relevant calls: (none detected)
- `_render_generic_narrative_expression_latex` L333–439; relevant calls: _render_generic_eta_composition_latex@336, _normalize_generic_eta_family_latex@434, render_toda_expression_latex@435, _render_generic_narrative_expression_latex@425, _render_generic_narrative_expression_latex@428
- `_try_render_generic_narrative_expression_latex` L442–450; relevant calls: render_toda_expression_latex@446
- `_try_render_generic_narrative_group_structure_latex` L453–464; relevant calls: render_toda_raw_group_structure_latex@457
- `_normalize_generic_narrative_statement_latex` L467–588; relevant calls: _normalize_generic_eta_family_latex@484, _normalize_generic_eta_family_latex@494, _try_render_generic_narrative_expression_latex@507, _render_generic_narrative_expression_latex@515, _try_render_generic_narrative_group_structure_latex@521, _normalize_generic_eta_family_latex@528
- `_normalize_generic_narrative_step_latex` L591–600; relevant calls: _normalize_generic_narrative_statement_latex@596
- `_render_generic_narrative_group_map_latex` L603–640; relevant calls: render_toda_primary_group_latex@637, render_toda_primary_group_latex@633
- `_render_phase153_r3_6_component_latex` L643–700; relevant calls: _normalize_generic_narrative_statement_latex@696, render_repository_conclusion_latex@662, _normalize_generic_narrative_statement_latex@674, render_toda_proof_statement_latex@682, _render_scalar_latex@655, _render_scalar_latex@651
- `_render_phase153_r3_6_component_list_prose` L705–733; relevant calls: _render_phase153_r3_6_component_latex@714
- `_render_phase153_r3_9_group_term_latex` L736–772; relevant calls: render_toda_primary_group_latex@744, _render_phase153_r3_9_group_term_latex@754
- `_render_phase153_r3_9_reference_statement_prose` L775–939; relevant calls: _render_phase153_r3_9_group_term_latex@786, _render_phase153_r3_9_group_term_latex@791, _render_phase153_r3_6_component_list_prose@839, _render_phase153_r3_6_component_list_prose@855, _render_phase153_r3_6_component_list_prose@872, _render_phase153_r3_6_component_list_prose@890, _render_generic_narrative_group_map_latex@907, render_toda_expression_latex@828, render_toda_raw_group_structure_latex@917, render_toda_expression_latex@933, render_toda_expression_latex@929, render_toda_expression_latex@812, render_toda_expression_latex@808, render_toda_expression_latex@804
- `_render_phase153_r3_6_reference_statement_prose` L942–1212; relevant calls: _render_phase153_r3_6_component_list_prose@1005, _render_phase153_r3_6_component_list_prose@1032, _render_phase153_r3_6_component_list_prose@1047, _render_phase153_r3_6_component_list_prose@1076, _render_phase153_r3_6_component_list_prose@1108, _render_phase153_r3_6_component_list_prose@1176, _render_phase153_r3_6_component_list_prose@1189, _render_phase153_r3_6_component_list_prose@1202, render_toda_expression_latex@1071, render_toda_primary_group_latex@959, render_toda_expression_latex@975, _render_scalar_latex@999, render_toda_expression_latex@1067, render_toda_expression_latex@1141, render_toda_expression_latex@1165, render_toda_primary_group_latex@955, render_toda_expression_latex@971, _render_scalar_latex@995, render_toda_expression_latex@1137, render_toda_expression_latex@1161, render_toda_expression_latex@991, render_toda_expression_latex@951, render_toda_raw_group_structure_latex@1133, render_toda_expression_latex@1157
- `_render_generic_narrative_statement_prose` L1215–1475; relevant calls: _render_phase153_r3_9_reference_statement_prose@1242, _render_phase153_r3_6_reference_statement_prose@1251, render_toda_group_proof_aggregate_statement_prose@1260, _render_generic_narrative_group_map_latex@1232, _render_generic_narrative_group_map_latex@1356, _render_generic_narrative_group_map_latex@1375, _render_generic_narrative_group_map_latex@1394, _render_generic_narrative_group_map_latex@1413, render_toda_primary_group_latex@1303, render_toda_raw_group_structure_latex@1324, render_toda_raw_group_structure_latex@1345, render_toda_primary_group_latex@1445, render_toda_expression_latex@1457, render_toda_expression_latex@1469, render_toda_expression_latex@1228, render_toda_expression_latex@1441, render_toda_expression_latex@1226, render_toda_primary_group_latex@1297, render_toda_expression_latex@1437, render_toda_expression_latex@1433, render_toda_primary_group_latex@1291
- `_normalize_toda_group_proof_narrative_sentence_endings` L1477–1525; relevant calls: (none detected)
- `_render_generic_narrative_step` L1528–1593; relevant calls: _render_generic_narrative_statement_prose@1542, _normalize_toda_group_proof_narrative_sentence_endings@1549, render_repository_conclusion_latex@1556, render_toda_proof_statement_latex@1568, _normalize_generic_narrative_step_latex@1574
- `_generic_short_exact_sequence_reason_prose` L2092–2110; relevant calls: (none detected)
- `_render_generic_narrative_proof_block` L2198–2353; relevant calls: _render_generic_narrative_step@2307, _generic_short_exact_sequence_reason_prose@2324
- `render_toda_group_proof_generic_narrative_markdown` L2356–2438; relevant calls: _render_generic_narrative_step@2424
- `render_toda_group_proof_generic_proof_markdown` L2441–2477; relevant calls: _generic_narrative_proof_order_indices@2459, _render_generic_narrative_proof_block@2465

### `toda_group_proof_narrative_reason_renderer.py`
- 存在: True
- 行数: 1694 / トップレベル定義: 6
- `render_toda_group_proof_narrative_reason_sentence` L23–288; relevant calls: render_toda_expression_latex@50, render_toda_expression_latex@53, _render_generic_narrative_step@74, render_toda_raw_group_structure_latex@125, _render_generic_narrative_expression_latex@169, _render_generic_narrative_expression_latex@174, _render_generic_narrative_step@198, _render_generic_narrative_expression_latex@224, _render_generic_narrative_expression_latex@229, render_toda_expression_latex@258
- `order_toda_group_proof_narrative_injective_image_order_reason` L292–1188; relevant calls: _render_generic_narrative_step@413, render_toda_group_proof_narrative_reason_sentence@449, visible_reason_paragraph@492, visible_reason_paragraph@601, _render_generic_narrative_step@637, visible_reason_paragraph@928, _render_generic_narrative_step@1040, _render_generic_narrative_step@668, visible_reason_index@676, _render_generic_narrative_step@752, visible_reason_index@760, _render_generic_narrative_step@957, _render_generic_narrative_step@1107, _render_generic_narrative_step@1055
- `_toda_group_proof_narrative_reason_insertion_index` L1190–1244; relevant calls: _render_generic_narrative_step@1195, _render_generic_narrative_step@1228
- `_normalize_exactness_to_map_property_reason_prose` L1249–1507; relevant calls: render_toda_group_proof_narrative_reason_sentence@1261, _render_generic_narrative_step@1438
- `_normalize_exactness_to_kernel_reason_prose` L1509–1614; relevant calls: render_toda_group_proof_narrative_reason_sentence@1521, _render_generic_narrative_step@1585, _render_generic_narrative_step@1578
- `insert_toda_group_proof_narrative_reason_prose` L1617–1693; relevant calls: render_toda_group_proof_narrative_reason_sentence@1636, _toda_group_proof_narrative_reason_insertion_index@1655, _normalize_exactness_to_map_property_reason_prose@1679, _normalize_exactness_to_kernel_reason_prose@1687

### `toda_group_proof_narrative_reasons.py`
- 存在: True
- 行数: 1101 / トップレベル定義: 11
- `_exactness_to_map_property_reason` L298–498; relevant calls: TodaGroupProofNarrativeReason@488
- `_exactness_to_kernel_reason` L501–590; relevant calls: TodaGroupProofNarrativeReason@580
- `_injective_image_order_reason` L593–685; relevant calls: TodaGroupProofNarrativeReason@675
- `_multiple_relation_to_order_reason` L688–749; relevant calls: TodaGroupProofNarrativeReason@742
- `_final_group_structure_reason` L752–916; relevant calls: TodaGroupProofNarrativeReason@903
- `_aggregate_derivation_reason` L919–935; relevant calls: TodaGroupProofNarrativeReason@931
- `_final_result_derivation_reason` L938–953; relevant calls: TodaGroupProofNarrativeReason@949
- `build_toda_group_proof_narrative_reason_sidecar` L956–1101; relevant calls: TodaGroupProofNarrativeReasonSidecar@1098, _exactness_to_map_property_reason@1048, _exactness_to_kernel_reason@1055, _injective_image_order_reason@1065, _multiple_relation_to_order_reason@1074, _final_group_structure_reason@1080, _aggregate_derivation_reason@1086, TodaGroupProofNarrativeReason@1036, _final_result_derivation_reason@1094

### `toda_group_proof_narrative_semantics.py`
- 存在: True
- 行数: 1125 / トップレベル定義: 15
- `_reference_application_semantics` L950–992; relevant calls: TodaGroupProofNarrativeReferenceApplicationSemantic@978, TodaGroupProofNarrativeReferenceIdentity@980

### `toda_group_proof_narrative_references.py`
- 存在: True
- 行数: 2233 / トップレベル定義: 14
- `_infer_toda_group_proof_literature_reference_from_rule_name` L47–99; relevant calls: LiteratureReference@70, LiteratureReference@82, LiteratureReference@94
- `extract_toda_group_proof_step_literature_reference` L102–158; relevant calls: _infer_toda_group_proof_literature_reference_from_rule_name@156, LiteratureReference@111, LiteratureReference@148
- `_same_toda_group_proof_literature_reference` L160–173; relevant calls: (none detected)
- `build_toda_group_proof_narrative_reference_entries` L182–256; relevant calls: extract_toda_group_proof_step_literature_reference@199, TodaGroupProofNarrativeReferenceEntry@239, _same_toda_group_proof_literature_reference@213
- `exclude_toda_group_proof_narrative_root_reference` L259–480; relevant calls: extract_toda_group_proof_step_literature_reference@317, _same_toda_group_proof_literature_reference@337, is_toda_fixed_statement_component_reference_eligible@422
- `select_toda_group_proof_narrative_reference_statement_steps` L483–650; relevant calls: extract_toda_group_proof_step_literature_reference@595, extract_toda_group_proof_step_literature_reference@599
- `filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary` L651–798; relevant calls: is_toda_fixed_statement_component_reference_eligible@752
- `filter_phase157_r4_representative_reference_entries_by_fixed_statement_boundary` L801–949; relevant calls: is_toda_fixed_statement_component_reference_eligible@920
- `filter_toda_group_proof_narrative_reference_entries_by_step_usage` L951–1094; relevant calls: extract_toda_group_proof_step_literature_reference@1040, _same_toda_group_proof_literature_reference@1049
- `filter_toda_group_proof_narrative_reference_entries_by_body_usage` L1097–1249; relevant calls: (none detected)
- `restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage` L1253–1707; relevant calls: (none detected)
- `restore_phase157_r4_representative_fixed_reference_entries_after_body_usage` L1710–2027; relevant calls: (none detected)
- `render_toda_group_proof_narrative_reference_entries_markdown` L2029–2233; relevant calls: (none detected)

### `toda_group_proof_narrative_contribution_renderer.py`
- 存在: True
- 行数: 10705 / トップレベル定義: 81
- `_is_toda_group_proof_narrative_reference_statement_candidate` L784–819; relevant calls: (none detected)
- `_phase157_r20_reference_scalar_value` L950–997; relevant calls: _phase157_r20_reference_scalar_value@975, _phase157_r20_reference_scalar_value@982
- `_phase157_r20_specialize_reference_value` L1000–1131; relevant calls: _phase157_r20_specialize_reference_value@1019, _phase157_r20_specialize_reference_value@1026, _phase157_r20_specialize_reference_value@1110, _phase157_r20_specialize_reference_value@1069, _phase157_r20_specialize_reference_value@1083, _phase157_r20_specialize_reference_value@1056
- `_phase157_r20_reference_descendants` L1216–1276; relevant calls: (none detected)
- `_phase157_r20_reference_range_allows` L1279–1318; relevant calls: (none detected)
- `_phase157_r20_specialize_reference_relation` L1321–1431; relevant calls: _phase157_r20_reference_descendants@1345, _phase157_r20_reference_scalar_value@1380, _phase157_r20_reference_scalar_value@1387, _phase157_r20_specialize_reference_value@1412, _phase157_r20_reference_range_allows@1403
- `_phase157_r20_canonical_fixed_reference_line` L1434–1454; relevant calls: (none detected)
- `_phase153_r6_reference_aggregate_component` L1457–1562; relevant calls: _phase157_r20_specialize_reference_relation@1539, extract_toda_group_proof_step_literature_reference@1500
- `_phase153_r6_render_reference_statement` L1565–1608; relevant calls: _phase153_r6_reference_aggregate_component@1592, project_reference_component_step@1602, _render_generic_narrative_step@1606
- `build_toda_group_proof_narrative_reference_reuse_marker_by_step_id` L1611–1682; relevant calls: select_toda_group_proof_narrative_reference_statement_steps@1658, _render_generic_narrative_step@1634, _is_toda_group_proof_narrative_reference_statement_candidate@1640
- `_phase157_r5_r7_order_and_connect_fixed_definition_reference_lines` L1685–1803; relevant calls: (none detected)
- `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` L1812–2029; relevant calls: select_toda_group_proof_narrative_reference_statement_steps@1869, _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines@2013, _render_generic_narrative_step@1831, _phase157_r20_canonical_fixed_reference_line@1836, _phase153_r6_reference_aggregate_component@1916, _phase157_r20_canonical_fixed_reference_line@1995, _is_toda_group_proof_narrative_reference_statement_candidate@1843, _phase153_r6_render_reference_statement@1997, _phase153_r6_reference_aggregate_component@1882
- `_toda_group_proof_narrative_reference_statement_lines_by_number` L2032–2052; relevant calls: _select_toda_group_proof_narrative_reference_entries_and_statement_lines@2046
- `_phase154_r5_reference_source_steps_by_number` L2281–2439; relevant calls: select_toda_group_proof_narrative_reference_statement_steps@2323, _render_generic_narrative_step@2304, _phase153_r6_reference_aggregate_component@2338
- `link_toda_group_proof_narrative_reference_body_consumers` L2570–2752; relevant calls: _phase154_r5_reference_source_steps_by_number@2592, _render_generic_narrative_step@2677
- `suppress_toda_group_proof_narrative_reference_body_restatements` L2754–2915; relevant calls: (none detected)
- `suppress_toda_group_proof_narrative_repeated_reference_restatements` L2919–3055; relevant calls: _phase157_r11_reference_statement_match_key@3032, _phase157_r11_reference_statement_match_key@2988
- `_phase157_r11_reference_statement_match_key` L3056–3111; relevant calls: (none detected)
- `suppress_toda_group_proof_narrative_reference_body_duplicates` L3114–3285; relevant calls: _phase157_r11_reference_statement_match_key@3195, _phase157_r11_reference_statement_match_key@3200
- `_toda_group_proof_narrative_reference_boundary_step_ids` L3377–3386; relevant calls: (none detected)
- `_toda_group_proof_narrative_reference_owned_step_ids` L3389–3492; relevant calls: extract_toda_group_proof_step_literature_reference@3454
- `_toda_group_proof_narrative_reference_internal_step_ids` L3653–3730; relevant calls: _toda_group_proof_narrative_reference_owned_step_ids@3707, select_toda_group_proof_narrative_reference_statement_steps@3689, _render_generic_narrative_step@3665, _is_toda_group_proof_narrative_reference_statement_candidate@3671
- `suppress_toda_group_proof_narrative_reference_internal_body` L3814–3985; relevant calls: _toda_group_proof_narrative_reference_internal_step_ids@3858, render_toda_group_proof_narrative_argument_purpose_sentence@3936, _render_generic_narrative_step@3910
- `_toda_group_proof_narrative_reference_externally_used_step_ids` L3986–4024; relevant calls: _toda_group_proof_narrative_reference_internal_step_ids@3991
- `_toda_group_proof_narrative_reference_frontier_step_ids` L4027–4113; relevant calls: extract_toda_group_proof_step_literature_reference@4045, extract_toda_group_proof_step_literature_reference@4095
- `normalize_toda_group_proof_narrative_connectors` L4116–4244; relevant calls: (none detected)
- `normalize_toda_group_proof_narrative_zero_map_exactness_reason` L4476–4638; relevant calls: _phase157_r11_reference_statement_match_key@4523, _render_generic_narrative_step@4531, _render_generic_narrative_step@4564
- `_toda_group_proof_narrative_two_equation_reference_numbers` L5443–5516; relevant calls: (none detected)
- `insert_toda_group_proof_narrative_reference_map_values_before_surjectivity` L6699–6770; relevant calls: (none detected)
- `merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows` L6820–7047; relevant calls: _render_generic_narrative_step@6890, _render_generic_narrative_step@6895, render_toda_primary_group_latex@6972, render_toda_primary_group_latex@6966, render_toda_primary_group_latex@6960, render_toda_primary_group_latex@6954
- `normalize_toda_group_proof_narrative_repeated_numeric_equalities` L8230–8379; relevant calls: (none detected)
- `link_toda_group_proof_narrative_unmarked_reference_consumers` L8382–8551; relevant calls: _render_generic_narrative_step@8451, extract_toda_group_proof_step_literature_reference@8488
- `normalize_toda_group_proof_narrative_display_math_periods` L8554–8585; relevant calls: (none detected)
- `_phase159_r1_7c_r3_reference_marker` L9142–9168; relevant calls: (none detected)
- `prune_toda_group_proof_narrative_root_zero_direct_premise_references` L9565–9765; relevant calls: _toda_group_proof_narrative_reference_statement_lines_by_number@9708, extract_toda_group_proof_step_literature_reference@9632
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` L10226–10705; relevant calls: render_toda_group_proof_narrative_multi_argument_markdown@10239, build_toda_group_proof_narrative_reference_entries@10273, filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary@10278, _select_toda_group_proof_narrative_reference_entries_and_statement_lines@10287, exclude_toda_group_proof_narrative_root_reference@10302, _toda_group_proof_narrative_reference_owned_step_ids@10310, build_toda_group_proof_narrative_reason_sidecar@10316, insert_toda_group_proof_narrative_reason_prose@10336, suppress_toda_group_proof_narrative_reference_internal_body@10342, suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry@10351, suppress_toda_group_proof_narrative_reference_body_duplicates@10358, link_toda_group_proof_narrative_reference_body_consumers@10364, normalize_toda_group_proof_narrative_connectors@10371, order_toda_group_proof_narrative_local_equation_derivations@10376, order_toda_group_proof_narrative_order_support@10381, merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows@10409, normalize_toda_group_proof_narrative_connectors@10420, normalize_toda_group_proof_narrative_repeated_numeric_equalities@10425, link_toda_group_proof_narrative_unmarked_reference_consumers@10430, suppress_toda_group_proof_narrative_reflexive_equalities@10437, order_toda_group_proof_narrative_surjectivity_support@10443, order_toda_group_proof_narrative_short_exact_support@10451, suppress_toda_group_proof_narrative_repeated_reference_restatements@10457, suppress_toda_group_proof_narrative_dangling_connectors@10463

### `toda_group_proof_narrative_blocks.py`
- 存在: True
- 行数: 543 / トップレベル定義: 7

### `toda_group_proof_narrative_arguments.py`
- 存在: True
- 行数: 719 / トップレベル定義: 9

### `toda_group_proof_narrative_argument_multi_renderer.py`
- 存在: True
- 行数: 621 / トップレベル定義: 3
- `render_toda_group_proof_narrative_multi_argument_markdown` L223–619; relevant calls: order_toda_group_proof_narrative_arguments@239, build_toda_group_proof_narrative_exactness_method_components@300, select_toda_group_proof_narrative_argument_primary_exactness_component@312, render_toda_group_proof_narrative_argument_header_method_section@431, _normalize_toda_group_proof_narrative_argument_header_spacing@438, render_toda_group_proof_narrative_argument_body_markdown@498, classify_toda_group_proof_narrative_exactness_component_exposure@324, render_toda_group_proof_narrative_transition_connector@451, extract_toda_group_proof_narrative_exactness_display_contributions@590, filter_toda_group_proof_narrative_exactness_body_contributions@596, _toda_group_proof_narrative_exactness_contribution_key@606

### `toda_group_proof_narrative_classifier.py`
- 存在: True
- 行数: 428 / トップレベル定義: 14
- `_reference_types_for_root` L114–122; relevant calls: (none detected)

### `toda_group_proof_narrative_exactness_method_renderer.py`
- 存在: True
- 行数: 114 / トップレベル定義: 3
- `render_toda_group_proof_narrative_exactness_method_transition` L9–28; relevant calls: (none detected)
- `_render_toda_group_proof_narrative_exactness_map_symbol_latex` L31–59; relevant calls: (none detected)
- `render_toda_group_proof_narrative_exactness_method_component_latex` L62–114; relevant calls: render_toda_primary_group_latex@95, render_toda_primary_group_latex@109, _render_toda_group_proof_narrative_exactness_map_symbol_latex@91, _render_toda_group_proof_narrative_exactness_map_symbol_latex@105, render_toda_primary_group_latex@87, _render_toda_group_proof_narrative_exactness_map_symbol_latex@83, render_toda_primary_group_latex@79

### `toda_group_proof_narrative_transport_link.py`
- 存在: True
- 行数: 81 / トップレベル定義: 2
- `render_suspension_transport_link` L17–57; relevant calls: render_step_latex@47, render_step_latex@48, render_step_latex@49, render_step_latex@50

### `phase164_r9_narrative_contract.py`
- 存在: True
- 行数: 100 / トップレベル定義: 5
- `_normalize_connectors` L74–85; relevant calls: (none detected)
- `normalize_public_narrative_contract` L88–100; relevant calls: _normalize_connectors@99

### `toda_group_proof_outline_renderer.py`
- 存在: True
- 行数: 200 / トップレベル定義: 4
- `_render_group_proof_outline_statement` L13–58; relevant calls: render_repository_conclusion_latex@28, render_toda_proof_statement_latex@37
- `render_toda_group_proof_outline_markdown` L128–200; relevant calls: _render_group_proof_outline_statement@172, _render_group_proof_outline_statement@181

### `toda_group_proof_narrative_provenance_catalog.py`
- 存在: True
- 行数: 54 / トップレベル定義: 1

### `toda_group_proof_narrative_aggregate_semantics.py`
- 存在: True
- 行数: 149 / トップレベル定義: 4

## 同名定義と優先順位（静的確認）

- `toda_group_proof_narrative_renderer.py` の `render_toda_group_proof_narrative_markdown`: L11281, L11329, L11991. 通常のグローバル参照は最後の定義を参照するが、以前の関数を別名へ束縛している場合は旧実装も有効。

## 対象テスト候補

- `tests\test_phase102_proof_scope_renderer.py`
- `tests\test_phase103_6d15_generic_exactness_structural_classification.py`
- `tests\test_phase103_6d38_zero_group_exactness_structural_classification.py`
- `tests\test_phase103_compact_detailed_renderer.py`
- `tests\test_phase103_generator_applicability_renderer.py`
- `tests\test_phase103_grouped_applicability_renderer.py`
- `tests\test_phase103_rule_family_grouped_renderer.py`
- `tests\test_phase109_4_known_group_identity_presentation_renderer.py`
- `tests\test_phase117_web_group_query.py`
- `tests\test_phase131_5_web_group_proof.py`
- `tests\test_phase132_5_group_proof_outline_renderer.py`
- `tests\test_phase132_6_group_proof_narrative_renderer.py`
- `tests\test_phase132_8_group_proof_narrative_dedup.py`
- `tests\test_phase132_9_web_group_proof_modes.py`
- `tests\test_phase133_6_group_proof_narrative_labels.py`
- `tests\test_phase133_7_group_proof_narrative_labels.py`
- `tests\test_phase133_9_group_proof_narrative_labels.py`
- `tests\test_phase134_11_pi8_5_narrative.py`
- `tests\test_phase134_24_pi15_8_narrative.py`
- `tests\test_phase134_24_v2_raw_group_renderer.py`
- `tests\test_phase134_26_narrative_shell.py`
- `tests\test_phase134_28_reference_block_assembler.py`
- `tests\test_phase134_3_pi6_3_numbered_narrative.py`
- `tests\test_phase134_5_pi6_3_reference_fact_split.py`
- `tests\test_phase134_6_pi6_3_mathbook_narrative.py`
- `tests\test_phase134_7_pi6_3_final_narrative.py`
- `tests\test_phase134_9_group_proof_narrative_classifier.py`
- `tests\test_phase134_9_pi8_5_narrative.py`
- `tests\test_phase135_1_web_narrative_display_math.py`
- `tests\test_phase135_2_web_narrative_inline_formatting.py`
- `tests\test_phase135_3_web_narrative_readability.py`
- `tests\test_phase136_1_pi6_3_narrative_prose.py`
- `tests\test_phase136_2_pi6_3_narrative_structure.py`
- `tests\test_phase141_4_narrative_semantics.py`
- `tests\test_phase141_5_narrative_blocks_semantics.py`
- `tests\test_phase141_narrative_blocks.py`
- `tests\test_phase142_2_generic_narrative_renderer.py`
- `tests\test_phase143_22_exactness_components.py`
- `tests\test_phase143_26_exactness_relevance.py`
- `tests\test_phase143_28_exactness_selection.py`
- `tests\test_phase143_30_exactness_method_transition.py`
- `tests\test_phase143_32_exactness_component_latex.py`
- `tests\test_phase143_38_exactness_display_contributions.py`
- `tests\test_phase143_39_exactness_contribution_ownership.py`
- `tests\test_phase143_42_argument_body_contribution_renderer.py`
- `tests\test_phase143_44_single_argument_narrative_renderer.py`
- `tests\test_phase143_46_multi_argument_narrative_assembler.py`
- `tests\test_phase143_49_dependency_label_narrative_policy.py`
- `tests\test_phase143_50_generic_statement_prose_renderer.py`
- `tests\test_phase143_53a_narrative_transitions.py`
- `tests\test_phase143_61b_direct_premise_narrative.py`
- `tests\test_phase143_63a_r_exactness_repair.py`
- `tests\test_phase143_73a_internal_statement_narrative.py`
- `tests\test_phase143_74a_map_narrative.py`
- `tests\test_phase143_74b_remaining_internal_narrative.py`
- `tests\test_phase143_7_narrative_arguments.py`
- `tests\test_phase144_6_r25_20_six_group_generic_production_narrative.py`
- `tests\test_phase144_6_r3_production_references.py`
- `tests\test_phase144_6_r3_structured_references.py`
- `tests\test_phase144_6_r5_19_proof_chain_narrative_integration.py`
- `tests\test_phase144_6_r5_28_narrative_contribution_ownership_audit.py`
- `tests\test_phase144_6_r5_29_narrative_contribution_chain_ownership_audit.py`
- `tests\test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py`
- `tests\test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py`
- `tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py`
- `tests\test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py`
- `tests\test_phase144_6_r5_43_generic_renderer_contribution_connection.py`
- `tests\test_phase148_rc2_3_exactness_exposure.py`
- `tests\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py`
- `tests\test_phase150_rc4_4_reasons.py`
- `tests\test_phase150_rc4_5_visible_reasons.py`
- `tests\test_phase150_rc4_5b_3_reference_binding.py`
- `tests\test_phase150_rc4_5c_2_exactness_to_map_property.py`
- `tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests\test_phase150_rc4_5f_2_final_group_structure_reason.py`
- `tests\test_phase150_rc4_7a_cross_group_reference_normalization.py`
- `tests\test_phase150_rc4_7d_3_public_narrative_generic_route.py`
- `tests\test_phase150_rc4_7d_generic_reason_vocabulary.py`
- `tests\test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`
- `tests\test_phase150_rc4_closure_reason_visibility.py`
- `tests\test_phase153_r10_used_reference_filtering.py`
- `tests\test_phase153_r11_generic_reference_attribution_filtering.py`
- `tests\test_phase153_r12_root_reference_exclusion.py`
- `tests\test_phase153_r2_public_reference_semantic_fact.py`
- `tests\test_phase153_r3_10_public_reference_connection_repair.py`
- `tests\test_phase153_r3_11_reference_body_ownership_repair.py`
- `tests\test_phase153_r3_3_reference_statement_selection.py`
- `tests\test_phase153_r3_4_reference_statement_rendering_connection.py`
- `tests\test_phase153_r3_5_reference_body_duplicate_suppression.py`
- `tests\test_phase153_r3_6_unresolved_reference_statement_rendering.py`
- `tests\test_phase153_r3_9_remaining_reference_renderer_coverage.py`
- `tests\test_phase153_r5_reference_selection.py`
- `tests\test_phase153_r6_reference_granularity.py`
- `tests\test_phase153_r8_reference_use_prose_normalization.py`
- `tests\test_phase153_r9_reference_reuse_derivation_suppression.py`
- `tests\test_phase153_scalar_order_narrative_classification.py`
- `tests\test_phase154_r2_fix3_reference_marker_completion.py`
- `tests\test_phase154_r5_fix1_graph_backed_reference_linkage.py`
- `tests\test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py`
- `tests\test_phase156_r5_reference_attribution_separation.py`
- `tests\test_phase156_r5_repair11_reference_dependency_pruning.py`
- `tests\test_phase156_r5_repair12_reference_frontier.py`
- `tests\test_phase156_r5_repair13_root_reference_frontier.py`
- `tests\test_phase156_r5_repair4_bridge_reference_inference.py`
- `tests\test_phase156_r5_repair6_reference_boundary_collapse.py`
- `tests\test_phase156_r5_repair7_reference_boundary_filter_order.py`
- `tests\test_phase156_r5_repair8_reference_owned_ancestor_closure.py`
- `tests\test_phase156_r6_3_reason_prose_canonicalization.py`
- `tests\test_phase157_r11_r17_residual_narrative_defects.py`
- `tests\test_phase157_r11_reference_reason_punctuation.py`
- `tests\test_phase157_r19_pi6_3_reference_dependency_restoration.py`
- `tests\test_phase157_r20_repair10_reference_local_specialization.py`
- `tests\test_phase157_r20_repair12_map_property_reference_support.py`
- `tests\test_phase157_r20_repair14_late_surjectivity_reference_support.py`
- `tests\test_phase157_r20_repair31_reference_period_and_stale_frontier_tests.py`
- `tests\test_phase157_r20_repair32_exactness_intro_anchor.py`
- `tests\test_phase157_r20_repair35_reference_aware_eta_bridge_anchor.py`
- `tests\test_phase157_r20_repair42_repeated_reference_restatements.py`
- `tests\test_phase157_r20_repair47_injective_image_order_reason.py`
- `tests\test_phase157_r20_repair48_injective_image_reason_ordering.py`
- `tests\test_phase157_r20_repair53_r3_fixed_reference_attribution.py`
- `tests\test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py`
- `tests\test_phase157_r20_repair6_descendant_reference_usage.py`
- `tests\test_phase157_r20_repair8_reference_alias_descendants.py`
- `tests\test_phase157_r3_pi6_3_reference_boundary.py`
- `tests\test_phase157_r4_r3_reference_selection_integration.py`
- `tests\test_phase157_r4_r3_repair1_reference_retention.py`
- `tests\test_phase157_r5_r10_reference_proof_boundary_qed.py`
- `tests\test_phase157_r5_r4_generic_reference_selection.py`
- `tests\test_phase157_r5_r6_53_bracket_definition_reference.py`
- `tests\test_phase157_r5_r7_reference_definition_consequence_rendering.py`
- `tests\test_phase158_r5_3_public_narrative_single_route.py`
- `tests\test_phase159_exactness_connector_normalization.py`
- `tests\test_phase159_exactness_map_property_public_dedup.py`
- `tests\test_phase159_generic_zero_exactness_map_property.py`
- `tests\test_phase159_pi3_2_exactness_reason_locality.py`
- `tests\test_phase159_pi3_2_final_locality_reapply.py`
- `tests\test_phase159_pi3_2_map_property_order.py`
- `tests\test_phase159_pi3_2_post_reference_locality_reapply.py`
- `tests\test_phase159_pi3_2_proofstep_premise_locality.py`
- `tests\test_phase159_pi3_2_public_definition_premise_locality.py`
- `tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py`
- `tests\test_phase159_pi3_2_visible_dependency_topological_order.py`
- `tests\test_phase159_pi4_3_exactness_reason_unification.py`
- `tests\test_phase159_pi4_3_exactness_surjectivity_unification.py`
- `tests\test_phase159_pi4_3_repair2g_reference_policy.py`
- `tests\test_phase159_pi6_3_zero_map_reason_order.py`
- `tests\test_phase159_r1_2_pi3_2_closure.py`
- `tests\test_phase159_r1_2_pi3_2_narrative_repair.py`
- `tests\test_phase159_r1_6a_foundational_reference_identity.py`
- `tests\test_phase159_r1_6c_source_faithful_reference_linkage.py`
- `tests\test_phase159_r1_6d_specialization_reference_linkage_finalization.py`
- `tests\test_phase159_r1_7b_repair15_subsumed_exactness.py`
- `tests\test_phase159_r1_7c_r3_repair4_reference_component_pruning.py`
- `tests\test_phase159_r1_7c_r4_equation_reference_order_repair1.py`
- `tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
- `tests\test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py`
- `tests\test_phase160_generic_stable_public_narrative.py`
- `tests\test_phase160_k2_public_narrative.py`
- `tests\test_phase160_remaining_stable_public_narrative.py`
- `tests\test_phase161_pi4_2_restored_reference_relink.py`
- `tests\test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py`
- `tests\test_phase161_r4_r5_repair11_effective_reference_source_component.py`
- `tests\test_phase161_r4_r5_repair13_reference_selection_source_binding.py`
- `tests\test_phase161_r4_r5_repair14_reference_locator_dedup.py`
- `tests\test_phase161_r4_r5_repair3_reference_self_marker_relink.py`
- `tests\test_phase161_r4_r5_repair9a_final_public_reference_relink.py`
- `tests\test_phase162_r3_2_reference_display.py`
- `tests\test_phase162_r3_narrative_connection.py`
- `tests\test_phase162_r3b_existing_renderer.py`
- `tests\test_phase162_r3c_root_reason.py`
- `tests\test_phase162_r3d_root_reason_audit.py`
- `tests\test_phase162_r3f_recursive_renderer.py`
- `tests\test_phase162_r3g_existing_reason_bridge.py`
- `tests\test_phase162_r3h_reason_inventory.py`
- `tests\test_phase162_r4_b3_common_renderer_audit.py`
- `tests\test_phase162_r4_b3_common_renderer_fix.py`
- `tests\test_phase162_r4_b_common_renderer_link.py`
- `tests\test_phase162_r4_narrative_refinement.py`
- `tests\test_phase162_r5_2_general_reference_schema.py`
- `tests\test_phase162_r5_3_reference_application_separation.py`
- `tests\test_phase162_r5_5_proof_narrative_composition.py`
- `tests\test_phase162_r5_6_final_reference_format.py`
- `tests\test_phase162_r5_6_narrative_final_format.py`
- `tests\test_phase162_r5_6_proof_relevance_reference_attribution.py`
- `tests\test_phase162_r5_6_repair2_direct_reference_attribution.py`
- `tests\test_phase162_r5_6_repair3_reference_application_prose.py`
- `tests\test_phase162_r5_6_repair5_reference_component_boundary.py`
- `tests\test_phase164_r5_r1_common_renderer.py`
- `tests\test_phase45_toda_prop42_exactness_compatibility.py`
- `tests\test_phase45_toda_prop42_exactness_instance.py`
- `tests\test_phase49_concrete_pi3_2_compatibility.py`
- `tests\test_phase50_pi3_2_whitehead_square.py`
- `tests\test_phase50_pi4_3_exactness_bridge.py`
- `tests\test_phase72r5_ordinary_ehp_211_exactness.py`
- `tests\test_phase76_delta_e_exactness_bridge.py`
- `tests\test_phase92_exactness_use_provenance.py`
- `tests\test_phase96_ehp_exactness_presentation.py`
- `tests\test_phase96_full_proof_report_renderer.py`
- `tests\test_phase96_human_readable_renderer.py`
- `tests\test_phase96_proof_step_mathematical_narrative.py`
- `tests\test_phase99_exploration_markdown_renderer.py`

## R49 / R50 の確認事項
- R49: DeltaZero および MapIsomorphism の ProofStep が Sidecar に入り、理由がどこで挿入/消失するかを表示段階ごとに確認。
- R50: 文献抽出 → 固定命題境界 → 使用判定 → body-consumer link → Reference section を段階ごとに確認。
- 実装変更前に同名再定義と後段の正規化で意味情報が消えるか検証。
- 旧 Phase の特化経路を消さずに一般経路への統合可否を判断。

## 制約
- AST call edges are syntactic; dynamic dispatch and branch feasibility are not proven.
- Function definitions earlier in the same scope may remain reachable through aliases.
- This report does not certify mathematical correctness or final Web output.
