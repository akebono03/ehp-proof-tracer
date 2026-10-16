# Phase 165 R6-2 R4-A-R3 規則識別子監査

- 状態: `OK`
- 対象: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`

| 指標 | 件数 |
|---|---:|
| factories | 77 |
| instantiated | 55 |
| pattern_backward_candidates | 25 |
| goal_verified | 0 |
| proof_verified | 0 |

## 規則別の識別結果

| Rule ID | status | rule.name | 逆向き構造候補 | Goal 実証 |
|---|---|---|---|---|
| ehp_rules.ehp_exactness_image_implies_kernel_inference_rule | INSTANTIATED | EHP exactness transfers image structure to kernel | 候補 | NOT_TESTED |
| ehp_rules.ehp_exactness_implies_zero_composition_inference_rule | INSTANTIATED | EHP exactness implies zero composition | 候補 | NOT_TESTED |
| ehp_rules.ehp_exactness_inference_rule | INSTANTIATED | EHP exactness from image and kernel | 候補 | NOT_TESTED |
| ehp_rules.ehp_exactness_kernel_implies_image_inference_rule | INSTANTIATED | EHP exactness transfers kernel structure to image | 候補 | NOT_TESTED |
| ehp_rules.ehp_zero_composition_implies_zero_relation_inference_rule | INSTANTIATED | EHP zero composition implies zero relation | 候補 | NOT_TESTED |
| stable_rules.freudenthal_boundary_epimorphism_inference_rule | INSTANTIATED | Freudenthal boundary range implies suspension epimorphism | 未確認 | NOT_TESTED |
| stable_rules.freudenthal_stable_isomorphism_inference_rule | INSTANTIATED | Freudenthal stable range implies suspension isomorphism | 未確認 | NOT_TESTED |
| stable_rules.suspension_injectivity_reflects_equality_inference_rule | INSTANTIATED | Suspension injectivity reflects equality | 未確認 | NOT_TESTED |
| stable_rules.suspension_injectivity_reflects_zero_inference_rule | INSTANTIATED | Suspension injectivity reflects zero | 未確認 | NOT_TESTED |
| stable_rules.suspension_isomorphism_implies_injective_inference_rule | INSTANTIATED | Suspension isomorphism implies injectivity | 未確認 | NOT_TESTED |
| set_rules.coset_equality_implies_modulo_inference_rule | INSTANTIATED | coset equality implies modulo | 未確認 | NOT_TESTED |
| set_rules.difference_membership_implies_modulo_inference_rule | INSTANTIATED | difference membership implies modulo | 未確認 | NOT_TESTED |
| set_rules.equality_implies_modulo_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| set_rules.exactness_implies_subgroup_equality_inference_rule | INSTANTIATED | exactness implies subgroup equality | 未確認 | NOT_TESTED |
| set_rules.kernel_membership_implies_mapped_zero_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| set_rules.mapped_zero_implies_kernel_membership_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| set_rules.membership_subset_propagation_inference_rule | INSTANTIATED | membership subset propagation | 候補 | NOT_TESTED |
| set_rules.modulo_implies_coset_equality_inference_rule | INSTANTIATED | modulo implies coset equality | 候補 | NOT_TESTED |
| set_rules.modulo_implies_difference_membership_inference_rule | INSTANTIATED | modulo implies difference membership | 候補 | NOT_TESTED |
| set_rules.mutual_subset_implies_subgroup_equality_inference_rule | INSTANTIATED | mutual subset implies subgroup equality | 候補 | NOT_TESTED |
| set_rules.subgroup_equality_implies_subset_inference_rule | INSTANTIATED | subgroup equality implies subset | 候補 | NOT_TESTED |
| set_rules.subgroup_equality_membership_propagation_inference_rule | INSTANTIATED | subgroup equality membership propagation | 未確認 | NOT_TESTED |
| set_rules.subgroup_equality_modulo_propagation_inference_rule | INSTANTIATED | subgroup equality modulo propagation | 未確認 | NOT_TESTED |
| set_rules.subgroup_equality_symmetry_inference_rule | INSTANTIATED | subgroup equality symmetry | 候補 | NOT_TESTED |
| set_rules.subgroup_equality_transitivity_inference_rule | INSTANTIATED | subgroup equality transitivity | 候補 | NOT_TESTED |
| set_rules.subset_transitivity_inference_rule | INSTANTIATED | subset transitivity | 候補 | NOT_TESTED |
| set_rules.zero_implies_modulo_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| hopf_rules.ehp_h_preserves_equality_inference_rule | INSTANTIATED | EHP H preserves equality | 未確認 | NOT_TESTED |
| hopf_rules.ehp_zero_composition_implies_suspended_hopf_zero_inference_rule | INSTANTIATED | EHP E-H zero composition implies suspended Hopf zero | 未確認 | NOT_TESTED |
| hopf_rules.hopf_composition_formula_inference_rule | INSTANTIATED | generalized Hopf composition formula | 未確認 | NOT_TESTED |
| hopf_rules.hopf_composition_law_inference_rule | INSTANTIATED | generalized Hopf invariant enables composition law | 未確認 | NOT_TESTED |
| hopf_rules.hopf_invariant_statement_to_ehp_h_equality_inference_rule | INSTANTIATED | generalized Hopf invariant to EHP H equality | 未確認 | NOT_TESTED |
| hopf_rules.hopf_invariant_value_zero_inference_rule | INSTANTIATED | generalized Hopf invariant value is zero | 未確認 | NOT_TESTED |
| hopf_rules.hopf_left_composition_formula_inference_rule | INSTANTIATED | generalized Hopf left composition formula | 未確認 | NOT_TESTED |
| hopf_rules.hopf_left_composition_law_inference_rule | INSTANTIATED | generalized Hopf invariant enables left composition law | 未確認 | NOT_TESTED |
| hopf_rules.toda_prop22_left_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| hopf_rules.toda_prop22_right_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| scalar_rules.even_scalar_evaluates_minus_one_power_inference_rule | INSTANTIATED | Even exponent evaluates minus-one power to one | 未確認 | NOT_TESTED |
| scalar_rules.even_scalar_implies_mod_two_congruence_inference_rule | INSTANTIATED | Even scalar implies congruence to zero modulo two | 未確認 | NOT_TESTED |
| scalar_rules.mod_two_one_scalar_preserves_order_two_element_inference_rule | INSTANTIATED | Scalar congruent to one modulo two preserves order-two element | 候補 | NOT_TESTED |
| scalar_rules.odd_scalar_evaluates_minus_one_power_inference_rule | INSTANTIATED | Odd exponent evaluates minus-one power to minus one | 未確認 | NOT_TESTED |
| scalar_rules.odd_scalar_implies_mod_two_congruence_inference_rule | INSTANTIATED | Odd scalar implies congruence to one modulo two | 未確認 | NOT_TESTED |
| scalar_rules.scalar_sign_evaluation_applies_to_multiple_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.additive_inverse_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.composition_equality_to_zero_inference_rule | INSTANTIATED | composition equality to zero | 候補 | NOT_TESTED |
| relation_rules.double_equals_repeated_sum_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.equality_preserved_under_left_composition_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.equality_preserved_under_multiple_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.equality_preserved_under_right_composition_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.equality_symmetry_inference_rule | INSTANTIATED | equality symmetry | 候補 | NOT_TESTED |
| relation_rules.equality_transitivity_inference_rule | INSTANTIATED | equality transitivity | 候補 | NOT_TESTED |
| relation_rules.iterated_suspension_one_bridge_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.nested_integer_multiple_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.order_implies_zero_multiple_inference_rule | INSTANTIATED | order implies zero multiple | 候補 | NOT_TESTED |
| relation_rules.sum_associativity_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.sum_commutativity_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| relation_rules.suspension_composition_functoriality_inference_rule | INSTANTIATED | suspension composition functoriality | 未確認 | NOT_TESTED |
| relation_rules.suspension_preserves_equality_inference_rule | INSTANTIATED | suspension preserves equality | 候補 | NOT_TESTED |
| relation_rules.suspension_preserves_zero_inference_rule | INSTANTIATED | suspension preserves zero | 候補 | NOT_TESTED |
| relation_rules.suspension_preserves_zero_multiple_inference_rule | INSTANTIATED | suspension preserves zero multiple | 未確認 | NOT_TESTED |
| relation_rules.zero_composition_equality_implies_zero_inference_rule | INSTANTIATED | zero composition equality implies zero | 候補 | NOT_TESTED |
| relation_rules.zero_composition_reverse_equality_implies_zero_inference_rule | INSTANTIATED | zero composition reverse equality implies zero | 候補 | NOT_TESTED |
| relation_rules.zero_equality_implies_zero_inference_rule | INSTANTIATED | zero equality implies zero | 候補 | NOT_TESTED |
| map_property_rules.injective_map_reflects_equality_inference_rule | INSTANTIATED | injective map reflects equality | 未確認 | NOT_TESTED |
| map_property_rules.isomorphism_implies_injective_inference_rule | INSTANTIATED | isomorphism implies injectivity | 未確認 | NOT_TESTED |
| homomorphism_rules.homomorphism_preserves_addition_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| homomorphism_rules.homomorphism_preserves_inverse_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| homomorphism_rules.homomorphism_preserves_known_zero_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| homomorphism_rules.homomorphism_preserves_multiple_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| homomorphism_rules.homomorphism_preserves_zero_inference_rule | INSTANTIATED | homomorphism preserves zero | 未確認 | NOT_TESTED |
| homomorphism_rules.suspension_additivity_bridge_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| homomorphism_rules.suspension_is_homomorphism_inference_rule | INSTANTIATED | suspension is homomorphism | 未確認 | NOT_TESTED |
| homomorphism_rules.suspension_multiple_bridge_inference_rule | REQUIRES_INPUT | — | 未確認 | NOT_TESTED |
| indeterminacy_rules.coset_membership_implies_modulo_inference_rule | INSTANTIATED | coset membership implies modulo | 未確認 | NOT_TESTED |
| indeterminacy_rules.equality_implies_sign_indeterminacy_inference_rule | INSTANTIATED | equality implies sign indeterminacy | 候補 | NOT_TESTED |
| indeterminacy_rules.modulo_implies_coset_membership_inference_rule | INSTANTIATED | modulo implies coset membership | 候補 | NOT_TESTED |
| indeterminacy_rules.symbolic_odd_equality_implies_coefficient_indeterminacy_inference_rule | INSTANTIATED | Symbolic odd equality implies coefficient indeterminacy | 未確認 | NOT_TESTED |

## R8 との一致

- `ehp_rules`: 一致
- `stable_rules`: 一致
- `set_rules`: 一致
- `hopf_rules`: 一致
- `scalar_rules`: 一致
- `relation_rules`: 一致
- `map_property_rules`: 一致
- `homomorphism_rules`: 一致
- `indeterminacy_rules`: 一致

## 制約

- Source factory ID is module.function; it is stable only while the source location and name remain unchanged.
- R8 and this probe instantiate factories separately; rule-name multisets are compared, not object identity.
- A conclusion/premise pattern is not evidence of a successful Goal match.
- No registered Goal application is performed in this conservative pass; goal_verified remains zero.
- STATIC_R8_DEFAULT_PATH_ONLY is not a runtime proof of common search reachability.
- Imports and factory execution can have production side effects; the probe itself writes only its report.

## 次段階

実際の既存 Goal と出典証人を用いる適用テストと、共通探索の再帰到達性検証は R4-A-R4 に分離する。
