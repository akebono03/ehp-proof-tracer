# R3-2 Provider と規則の静的対応監査

- 状態: `STATIC_MAPPING_ONLY`
- R8 factory: 77
- 共通接続参照: 13
- その他 expand_ 候補: 22
- 証明検証: なし

## 共通接続

| 参照名 | 解決した Provider ID | 接続種別 |
|---|---|---|
| `expand_registered_toda45_finite_cyclic_goal` | `phase165_r57_r7_stable_expansion.expand_registered_toda45_finite_cyclic_goal` | `DIRECT_OPTIONS_EXTEND` |
| `expand_registered_eta_specialization` | `phase165_r57_r8_eta_specialization.expand_registered_eta_specialization` | `DIRECT_OPTIONS_EXTEND` |
| `expand_registered_delta_image_goal` | `phase165_r57_r19_delta_image_backward.expand_registered_delta_image_goal` | `DIRECT_OPTIONS_EXTEND` |
| `expand_cited_general_specialization` | `phase165_r57_r20_general_specialization.expand_cited_general_specialization` | `DIRECT_OPTIONS_EXTEND` |
| `expand_delta_zero_from_suspension_iso` | `phase165_r14_r11_delta_zero.expand_delta_zero_from_suspension_iso` | `PROVIDER_LOOP_MEMBER` |
| `expand_diagonal_suspension` | `phase165_r14_r14_diagonal_and_prop42.expand_diagonal_suspension` | `PROVIDER_LOOP_MEMBER` |
| `expand_generic_ehp_hopf_goal` | `phase165_r14_r9_ehp_exactness.expand_generic_ehp_hopf_goal` | `PROVIDER_LOOP_MEMBER` |
| `expand_generic_iso_goal` | `phase165_r14_r6_generic_iso.expand_generic_iso_goal` | `PROVIDER_LOOP_MEMBER` |
| `extra_providers` | `extra_providers` | `PROVIDER_LOOP_DYNAMIC` |
| `provider(goal)` | `provider(goal)` | `PROVIDER_LOOP` |
| `witness_options` | `phase165_r52_r9_shared_math.witness_options` | `MERGE_PATH` |
| `generic_provider` | `phase165_r52_r9_shared_math.generic_provider` | `MERGE_PATH` |
| `seeded_options` | `phase165_r52_r9_shared_math.seeded_options` | `MERGE_PATH` |

## Provider と Rule factory の対応

| Provider ID | 状態 | 直接参照する規則 |
|---|---|---|
| `phase161_backward_goal_schema.expand_phase161_r2_suspension_isomorphism_goal` | `SOURCE_INSPECTED` | `toda_rules.toda_53_n3_suspension_isomorphism_inference_rule` (OUTSIDE_R8_OR_UNRESOLVED_FACTORY) |
| `phase161_r3_backward_goal_schema.expand_phase161_r3_ehp_goal` | `SOURCE_INSPECTED` | 未特定 |
| `phase161_r3_backward_goal_schema.expand_phase161_r3_goal` | `SOURCE_INSPECTED` | 未特定 |
| `phase161_r4_literature_premise_matching.expand_phase161_r4_literature_goal` | `SOURCE_INSPECTED` | 未特定 |
| `phase162_group_structure_backward.expand_group_structure_goal` | `SOURCE_INSPECTED` | `phase162_group_structure_backward.group_structure_transport_inference_rule` (OUTSIDE_R8_OR_UNRESOLVED_FACTORY) |
| `phase162_pi5_3_backward_selection.expand_phase162_pi5_3_group_goal` | `SOURCE_INSPECTED` | `toda_rules.toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule` (OUTSIDE_R8_OR_UNRESOLVED_FACTORY) |
| `phase165_r14_r11_delta_zero.expand_delta_zero_from_suspension_iso` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r14_r14_diagonal_and_prop42.expand_diagonal_suspension` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r14_r5_ehp_connection.expand_registered_ehp_goal` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r14_r6_generic_iso.expand_generic_iso_goal` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r14_r7_map_discovery.expand_discovered_group_goal` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r14_r8_source_link.expand_source_mapped_group_goal` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r14_r9_ehp_exactness.expand_generic_ehp_hopf_goal` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r52_r12_component_bridge.expand_cited_given_components` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r52_r9_shared_math.generic_provider` | `FUNCTION_NOT_FOUND` | 未特定 |
| `phase165_r52_r9_shared_math.phase165_r52_r23_backup.shared_expansion_provider` | `SOURCE_NOT_FOUND` | 未特定 |
| `phase165_r52_r9_shared_math.seeded_options` | `FUNCTION_NOT_FOUND` | 未特定 |
| `phase165_r52_r9_shared_math.shared_expansion_provider` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r52_r9_shared_math.witness_options` | `FUNCTION_NOT_FOUND` | 未特定 |
| `phase165_r57_r19_delta_image_backward.expand_registered_delta_image_goal` | `SOURCE_INSPECTED` | `toda_delta_image_rules.free_cyclic_generator_delta_image_inference_rule` (OUTSIDE_R8_OR_UNRESOLVED_FACTORY) |
| `phase165_r57_r20_general_specialization.expand_cited_general_specialization` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r57_r26_generic_search_connection.build_generic_backward_expansion_provider` | `SOURCE_INSPECTED` | 未特定 |
| `phase165_r57_r7_stable_expansion.expand_registered_toda45_finite_cyclic_goal` | `SOURCE_INSPECTED` | `toda_stable_group_transport.toda_45_generic_finite_cyclic_transport_inference_rule` (OUTSIDE_R8_OR_UNRESOLVED_FACTORY) |
| `phase165_r57_r8_eta_specialization.expand_registered_eta_specialization` | `SOURCE_INSPECTED` | `phase165_r57_r8_eta_specialization.eta_specialization_inference_rule` (OUTSIDE_R8_OR_UNRESOLVED_FACTORY) |
| `phase165_r8_rule_provider.create_rule_expansion_provider` | `SOURCE_INSPECTED` | 未特定 |

## 注意

直接参照の一致は数学的に同等であることを意味しない。
Provider から Provider への間接呼び出しは実行検証していない。
本番コードは変更しない。
