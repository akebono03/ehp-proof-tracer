# Phase 165 R6-2 R4-A-R5 失敗理由・pi4^3 接続監査

- 状態: `OK`
- Goal 検査数: 201
- 証明成功の検証件数: 0（この監査では実行しない）

## 観測された失敗・成功理由

| 理由 | 観測回数 |
|---|---:|
| `NO_CONCLUSION_MATCH` | 5212 |
| `NO_CONCLUSION_PATTERN` | 5829 |
| `PREMISE_ERROR:TypeError` | 7 |
| `UNBOUND_VARIABLE` | 7 |

## pi4^3 Adapter

- status: `FOUND`
- shared provider: `STATIC_REFERENCED`
- 直接参照された規則 factory: 4
- AST で検出した GoalExpansion return: 4

| factory | 行 |
|---|---:|
| `rules.toda_pi4_3_finite_cyclic_inference_rule` | 86 |
| `rules.toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule` | 98 |
| `rules.toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule` | 115 |
| `finite_cyclic_generator_substitution_rule` | 78 |

## 規則別の理由

| Rule ID | R8 実行候補 | 理由の集計 |
|---|---:|---|
| `ehp_rules.ehp_exactness_image_implies_kernel_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `ehp_rules.ehp_exactness_implies_zero_composition_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `ehp_rules.ehp_exactness_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `ehp_rules.ehp_exactness_kernel_implies_image_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `ehp_rules.ehp_zero_composition_implies_zero_relation_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `stable_rules.freudenthal_boundary_epimorphism_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `stable_rules.freudenthal_stable_isomorphism_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `stable_rules.suspension_injectivity_reflects_equality_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `stable_rules.suspension_injectivity_reflects_zero_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `stable_rules.suspension_isomorphism_implies_injective_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `set_rules.coset_equality_implies_modulo_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `set_rules.difference_membership_implies_modulo_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `set_rules.equality_implies_modulo_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `set_rules.exactness_implies_subgroup_equality_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `set_rules.kernel_membership_implies_mapped_zero_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `set_rules.mapped_zero_implies_kernel_membership_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `set_rules.membership_subset_propagation_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `set_rules.modulo_implies_coset_equality_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `set_rules.modulo_implies_difference_membership_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `set_rules.mutual_subset_implies_subgroup_equality_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `set_rules.subgroup_equality_implies_subset_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `set_rules.subgroup_equality_membership_propagation_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `set_rules.subgroup_equality_modulo_propagation_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `set_rules.subgroup_equality_symmetry_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `set_rules.subgroup_equality_transitivity_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `set_rules.subset_transitivity_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `set_rules.zero_implies_modulo_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `hopf_rules.ehp_h_preserves_equality_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `hopf_rules.ehp_zero_composition_implies_suspended_hopf_zero_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `hopf_rules.hopf_composition_formula_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `hopf_rules.hopf_composition_law_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `hopf_rules.hopf_invariant_statement_to_ehp_h_equality_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `hopf_rules.hopf_invariant_value_zero_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `hopf_rules.hopf_left_composition_formula_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `hopf_rules.hopf_left_composition_law_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `hopf_rules.toda_prop22_left_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `hopf_rules.toda_prop22_right_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `scalar_rules.even_scalar_evaluates_minus_one_power_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `scalar_rules.even_scalar_implies_mod_two_congruence_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `scalar_rules.mod_two_one_scalar_preserves_order_two_element_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `scalar_rules.odd_scalar_evaluates_minus_one_power_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `scalar_rules.odd_scalar_implies_mod_two_congruence_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `scalar_rules.scalar_sign_evaluation_applies_to_multiple_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.additive_inverse_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.composition_equality_to_zero_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `relation_rules.double_equals_repeated_sum_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.equality_preserved_under_left_composition_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.equality_preserved_under_multiple_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.equality_preserved_under_right_composition_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.equality_symmetry_inference_rule` | 7 | NO_CONCLUSION_MATCH: 194, PREMISE_ERROR:TypeError: 7 |
| `relation_rules.equality_transitivity_inference_rule` | 0 | NO_CONCLUSION_MATCH: 194, UNBOUND_VARIABLE: 7 |
| `relation_rules.iterated_suspension_one_bridge_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.nested_integer_multiple_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.order_implies_zero_multiple_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `relation_rules.sum_associativity_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.sum_commutativity_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `relation_rules.suspension_composition_functoriality_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `relation_rules.suspension_preserves_equality_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `relation_rules.suspension_preserves_zero_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `relation_rules.suspension_preserves_zero_multiple_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `relation_rules.zero_composition_equality_implies_zero_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `relation_rules.zero_composition_reverse_equality_implies_zero_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `relation_rules.zero_equality_implies_zero_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `map_property_rules.injective_map_reflects_equality_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `map_property_rules.isomorphism_implies_injective_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `homomorphism_rules.homomorphism_preserves_addition_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `homomorphism_rules.homomorphism_preserves_inverse_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `homomorphism_rules.homomorphism_preserves_known_zero_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `homomorphism_rules.homomorphism_preserves_multiple_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `homomorphism_rules.homomorphism_preserves_zero_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `homomorphism_rules.suspension_additivity_bridge_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `homomorphism_rules.suspension_is_homomorphism_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `homomorphism_rules.suspension_multiple_bridge_inference_rule` | 0 | REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE: 1 |
| `indeterminacy_rules.coset_membership_implies_modulo_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |
| `indeterminacy_rules.equality_implies_sign_indeterminacy_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `indeterminacy_rules.modulo_implies_coset_membership_inference_rule` | 0 | NO_CONCLUSION_MATCH: 201 |
| `indeterminacy_rules.symbolic_odd_equality_implies_coefficient_indeterminacy_inference_rule` | 0 | NO_CONCLUSION_PATTERN: 201 |

## 解釈上の制約

- NO_CONCLUSION_MATCH means only that no selected registered Goal matches.
- UNBOUND_VARIABLE does not prove witness unavailability.
- PREMISE_REJECTED_OR_GUARD_UNKNOWN does not identify a failing guard.
- STATIC_R8_PATH is not recursive execution proof.
- R8 factory family only; other providers and source witnesses remain outside the counts.
- The adapter branch source is inspected, not executed.
