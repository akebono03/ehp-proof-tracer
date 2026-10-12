# Phase 164 R7-R2 命題取得経路の静的監査

これは import 到達性と AST 呼出候補の調査です。実行時の到達性・証明の正当性・削除安全性は未確認です。

- 対象ルート直下の Python ファイル: 277
- 構文エラー: 0
- 既存本番コード変更: なし
- 全体 pytest: 未実行

## Group

- 静的到達モジュール: 146
- 要確認候補: 51

| 深さ | モジュール | 直接 import | 呼出候補 | 判定 |
|---:|---|---|---:|---|
| 0 | `toda_group_proof_presentation.py` | proof_repository | 0 | candidate-needs-manual-review |
| 0 | `toda_group_result_proof_replay.py` | proof_repository | 0 | candidate-needs-manual-review |
| 1 | `proof_repository.py` | - | 0 | repository-provider |
| 1 | `toda_calculation_facade.py` | proof_repository, standard_production_repository | 1 | candidate-needs-manual-review |
| 1 | `toda_group_proof_narrative_renderer.py` | - | 13 | candidate-needs-manual-review |
| 1 | `toda_group_result.py` | proof_repository | 0 | candidate-needs-manual-review |
| 1 | `toda_human_readable_renderer.py` | - | 1 | candidate-needs-manual-review |
| 2 | `phase164_r5_web_registry_connection.py` | proof_repository | 0 | candidate-needs-manual-review |
| 2 | `repository_element_exploration.py` | proof_repository | 0 | candidate-needs-manual-review |
| 2 | `repository_element_lookup.py` | proof_repository | 2 | candidate-needs-manual-review |
| 2 | `standard_production_repository.py` | proof_repository, standard_repository | 1 | repository-provider |
| 2 | `toda_calculation_goal.py` | proof_repository | 0 | candidate-needs-manual-review |
| 2 | `toda_calculation_report.py` | proof_repository | 2 | candidate-needs-manual-review |
| 2 | `toda_end_to_end_presentation.py` | proof_repository | 0 | candidate-needs-manual-review |
| 2 | `toda_group_proof_narrative_argument_multi_renderer.py` | - | 3 | candidate-needs-manual-review |
| 2 | `toda_group_proof_narrative_arguments.py` | - | 2 | candidate-needs-manual-review |
| 2 | `toda_group_proof_narrative_classifier.py` | - | 1 | candidate-needs-manual-review |
| 2 | `toda_group_proof_narrative_contribution_renderer.py` | - | 20 | candidate-needs-manual-review |
| 2 | `toda_group_proof_narrative_reasons.py` | - | 2 | candidate-needs-manual-review |
| 2 | `toda_group_proof_narrative_references.py` | - | 8 | candidate-needs-manual-review |
| 2 | `toda_group_proof_narrative_semantics.py` | - | 9 | candidate-needs-manual-review |
| 2 | `toda_proof_presentation.py` | proof_repository | 0 | candidate-needs-manual-review |
| 2 | `toda_stable_eta_proof_replay.py` | proof_repository | 0 | candidate-needs-manual-review |
| 3 | `phase162_pi5_3_web_replay.py` | proof_repository | 0 | candidate-needs-manual-review |
| 3 | `phase164_r4_r1_source_crosswalk.py` | - | 2 | candidate-needs-manual-review |
| 3 | `phase164_r4_r8_registry_reconstruction.py` | phase163_r4_registry_bridge, unified_statement_registry | 2 | candidate-needs-manual-review |
| 3 | `standard_repository.py` | proof_repository | 0 | repository-provider |
| 3 | `toda_calculation.py` | proof_repository | 3 | candidate-needs-manual-review |
| 3 | `toda_group_lookup.py` | proof_repository | 1 | candidate-needs-manual-review |
| 3 | `toda_group_proof_narrative_aggregate_semantics.py` | - | 1 | candidate-needs-manual-review |
| 3 | `toda_group_proof_narrative_argument_body_renderer.py` | - | 7 | candidate-needs-manual-review |
| 3 | `toda_group_proof_narrative_argument_local_body.py` | - | 1 | candidate-needs-manual-review |
| 3 | `toda_group_proof_narrative_contribution_ordering.py` | - | 12 | candidate-needs-manual-review |
| 3 | `toda_group_proof_narrative_equation_numbering.py` | - | 5 | candidate-needs-manual-review |
| 3 | `toda_group_proof_narrative_method_evidence.py` | - | 1 | candidate-needs-manual-review |
| 3 | `toda_group_proof_narrative_reason_renderer.py` | - | 2 | candidate-needs-manual-review |
| 3 | `toda_literature_statement_boundary.py` | - | 3 | candidate-needs-manual-review |
| 3 | `toda_proof_flow_presentation.py` | proof_repository | 1 | candidate-needs-manual-review |
| 4 | `phase162_r3_narrative_connection.py` | - | 1 | candidate-needs-manual-review |
| 4 | `phase162_validated_proof_presentation.py` | - | 3 | candidate-needs-manual-review |
| 4 | `phase163_r3_registry_validation.py` | unified_statement_registry | 5 | candidate-needs-manual-review |
| 4 | `phase163_r4_registry_bridge.py` | theorem_facts, unified_statement_registry | 2 | bridge-provider |
| 4 | `phase164_r4_r6_typed_binding.py` | phase163_r4_registry_bridge, unified_statement_registry | 11 | candidate-needs-manual-review |
| 4 | `repository_foundational_group_specialization.py` | proof_repository | 0 | candidate-needs-manual-review |
| 4 | `repository_proof_scope.py` | proof_repository | 2 | candidate-needs-manual-review |
| 4 | `toda_calculation_goal_discovery.py` | proof_repository | 1 | candidate-needs-manual-review |
| 4 | `toda_calculation_goal_normalization.py` | proof_repository | 0 | candidate-needs-manual-review |
| 4 | `unified_statement_registry.py` | - | 0 | registry-provider |
| 5 | `phase164_r4_r3_independent_semantic_audit.py` | - | 6 | candidate-needs-manual-review |
| 5 | `toda_calculation_goal_extraction.py` | proof_repository | 0 | candidate-needs-manual-review |
| 6 | `phase164_r4_r2_semantic_structure.py` | - | 1 | candidate-needs-manual-review |

### 関連 tests/ の候補

- `tests/test_phase131_3_group_result_proof_replay.py`
- `tests/test_phase131_5_web_group_proof.py`
- `tests/test_phase132_4_group_proof_presentation.py`
- `tests/test_phase132_5_group_proof_outline_renderer.py`
- `tests/test_phase132_6_group_proof_narrative_renderer.py`
- `tests/test_phase132_8_group_proof_narrative_dedup.py`
- `tests/test_phase132_9_web_group_proof_modes.py`
- `tests/test_phase134_11_classifier.py`
- `tests/test_phase134_14_presentation_helpers.py`
- `tests/test_phase134_16_classifier_regression.py`
- `tests/test_phase134_20_classifier_audit_scope.py`
- `tests/test_phase134_21_pi15_8_roles.py`
- `tests/test_phase134_24_pi15_8_narrative.py`
- `tests/test_phase134_24_v2_raw_group_renderer.py`
- `tests/test_phase134_9_group_proof_narrative_classifier.py`
- `tests/test_phase135_1_web_narrative_display_math.py`
- `tests/test_phase135_2_web_narrative_inline_formatting.py`
- `tests/test_phase141_4_narrative_semantics.py`
- `tests/test_phase141_5_narrative_blocks_semantics.py`
- `tests/test_phase141_6_block_audit.py`
- `tests/test_phase141_8_general_roles.py`
- `tests/test_phase141_9_final_audit.py`
- `tests/test_phase141_narrative_blocks.py`
- `tests/test_phase142_2_generic_narrative_renderer.py`
- `tests/test_phase142_3_generic_proof_text.py`
- `tests/test_phase143_10_fix1_compatibility.py`
- `tests/test_phase143_10_local_argument_boundaries.py`
- `tests/test_phase143_12_purpose_subject.py`
- `tests/test_phase143_19_method_evidence.py`
- `tests/test_phase143_1_generic_proof_order.py`
- `tests/test_phase143_1a_semantic_dependency.py`
- `tests/test_phase143_1b_semantic_proof_order.py`
- `tests/test_phase143_2_generic_short_exact_sequence.py`
- `tests/test_phase143_3_generic_eta_normalization.py`
- `tests/test_phase143_75c_generic_semantic_rendering.py`

## Generator

- 静的到達モジュール: 59
- 要確認候補: 15

| 深さ | モジュール | 直接 import | 呼出候補 | 判定 |
|---:|---|---|---:|---|
| 0 | `repository_generator_known_group_identity_lookup.py` | proof_repository, standard_production_repository | 1 | candidate-needs-manual-review |
| 1 | `generator_input.py` | - | 3 | candidate-needs-manual-review |
| 1 | `proof_repository.py` | - | 0 | repository-provider |
| 1 | `repository_proof_scope.py` | proof_repository | 2 | candidate-needs-manual-review |
| 1 | `standard_production_repository.py` | proof_repository, standard_repository | 1 | repository-provider |
| 1 | `toda_group_lookup.py` | proof_repository | 1 | candidate-needs-manual-review |
| 1 | `toda_human_readable_renderer.py` | - | 1 | candidate-needs-manual-review |
| 2 | `repository_element_exploration.py` | proof_repository | 0 | candidate-needs-manual-review |
| 2 | `repository_element_lookup.py` | proof_repository | 2 | candidate-needs-manual-review |
| 2 | `standard_repository.py` | proof_repository | 0 | repository-provider |
| 2 | `toda_end_to_end_presentation.py` | proof_repository | 0 | candidate-needs-manual-review |
| 2 | `toda_group_result.py` | proof_repository | 0 | candidate-needs-manual-review |
| 2 | `toda_proof_presentation.py` | proof_repository | 0 | candidate-needs-manual-review |
| 3 | `toda_calculation_goal.py` | proof_repository | 0 | candidate-needs-manual-review |
| 3 | `toda_proof_flow_presentation.py` | proof_repository | 1 | candidate-needs-manual-review |

### 関連 tests/ の候補

- `tests/test_phase109_10_existing_fact_known_group_identity_validation.py`
- `tests/test_phase109_12_nu5_proof_derived_ambient_fallback.py`
- `tests/test_phase109_14_decorated_sigma_finite_cyclic_fallback.py`
- `tests/test_phase109_16_sigma8_direct_sum_fallback.py`
- `tests/test_phase109_18_sigma9_indexed_finite_cyclic_fallback.py`
- `tests/test_phase109_20_sigma10_concrete_specialization.py`
- `tests/test_phase109_22_generic_indexed_sigma_specialization.py`
- `tests/test_phase109_24_generic_indexed_sigma_proof_scope_integration.py`
- `tests/test_phase109_29_known_group_proof_replay_cli.py`
- `tests/test_phase109_31_known_group_replay_narrow_rendering.py`
- `tests/test_phase109_3_recursive_known_group_identity_lookup.py`
- `tests/test_phase109_4_known_group_identity_presentation_renderer.py`
- `tests/test_phase111_10_proof_replay_depth_cli.py`
- `tests/test_phase111_12_deep_show_proof_safe_fallback.py`
- `tests/test_phase120_2_web_generator_proof.py`
- `tests/test_phase122_4_web_generator_proof_scope.py`

## Operation

- 静的到達モジュール: 66
- 要確認候補: 20

| 深さ | モジュール | 直接 import | 呼出候補 | 判定 |
|---:|---|---|---:|---|
| 0 | `repository_operation_query_facade.py` | proof_repository, standard_production_repository | 1 | candidate-needs-manual-review |
| 0 | `repository_operation_query_lookup.py` | proof_repository | 0 | candidate-needs-manual-review |
| 1 | `proof_repository.py` | - | 0 | repository-provider |
| 1 | `repository_nu5_eta8_suspension_zero_specialization.py` | proof_repository | 0 | candidate-needs-manual-review |
| 1 | `repository_nu5_stable_bridge_specialization.py` | proof_repository | 0 | candidate-needs-manual-review |
| 1 | `repository_nu_prime_suspension_membership_specialization.py` | proof_repository | 0 | candidate-needs-manual-review |
| 1 | `repository_proof_scope.py` | proof_repository | 2 | candidate-needs-manual-review |
| 1 | `repository_sigma11_suspension_specialization.py` | proof_repository | 0 | candidate-needs-manual-review |
| 1 | `standard_production_repository.py` | proof_repository, standard_repository | 1 | repository-provider |
| 2 | `generator_input.py` | - | 3 | candidate-needs-manual-review |
| 2 | `standard_repository.py` | proof_repository | 0 | repository-provider |
| 2 | `toda_human_readable_renderer.py` | - | 1 | candidate-needs-manual-review |
| 3 | `repository_element_exploration.py` | proof_repository | 0 | candidate-needs-manual-review |
| 3 | `repository_element_lookup.py` | proof_repository | 2 | candidate-needs-manual-review |
| 3 | `toda_calculation_goal.py` | proof_repository | 0 | candidate-needs-manual-review |
| 3 | `toda_end_to_end_presentation.py` | proof_repository | 0 | candidate-needs-manual-review |
| 3 | `toda_group_result.py` | proof_repository | 0 | candidate-needs-manual-review |
| 3 | `toda_proof_presentation.py` | proof_repository | 0 | candidate-needs-manual-review |
| 4 | `toda_group_lookup.py` | proof_repository | 1 | candidate-needs-manual-review |
| 4 | `toda_proof_flow_presentation.py` | proof_repository | 1 | candidate-needs-manual-review |

### 関連 tests/ の候補

- `tests/test_phase110_10_operation_query_proof_replay.py`
- `tests/test_phase110_10_operation_query_proof_replay_cli.py`
- `tests/test_phase110_12_operation_query_proof_replay_statement_presentation.py`
- `tests/test_phase110_5_minimal_operation_query_core.py`
- `tests/test_phase110_8_operation_query_result_presentation.py`
- `tests/test_phase111_10_proof_replay_depth_cli.py`
- `tests/test_phase111_9_three_term_composition_query.py`
- `tests/test_phase114_3_nu5_operation_query_handoff.py`
- `tests/test_phase115_sigma11_operation_query_handoff.py`
- `tests/test_phase118_4_depth_browser_usability.py`
- `tests/test_phase118_web_operation_query_proof.py`
- `tests/test_phase128_nu5_eta8_operation_query_handoff.py`
- `tests/test_phase129_nu_prime_operation_query_handoff.py`

## R7-R3 に向けた分類

1. Group／Generator／Operation の Web 入口から深さ順に import 依存を確認する。
2. 命題取得と ProofStep 取得を分離し、文献固定命題は既存の引用適格性判定を必ず維持する。
3. `ProofRepository` は証明木の保存・検索として残し、文献の真偽を Repository の存在から推論しない。
4. `source_archive` と `metadata_only` は proof eligible に昇格させない。
5. 共通 API 経由への切替は利用箇所と対応するテストが確認できてから一箇所ずつ実施する。

## 結論

R7-R2 静的経路棚卸し終了。旧経路削除・本番 API 切替は未許可。
