# Phase 168 R2-10 Reference pipeline 静的監査

監査対象: ローカル作業ツリー。**コードは変更しない**。この監査は AST に基づき、実行時の件数を確定するものではない。

## Renderer に現れる参照関数呼び出し（行番号順）

| 行 | 所属関数 | 呼び出し |
|---:|---|---|
| 723 | `_insert_toda_group_proof_narrative_argument_contributions` | `_is_toda_group_proof_narrative_reference_statement_candidate` |
| 1009 | `_phase157_r20_reference_scalar_value` | `_phase157_r20_reference_scalar_value` |
| 1016 | `_phase157_r20_reference_scalar_value` | `_phase157_r20_reference_scalar_value` |
| 1053 | `_phase157_r20_specialize_reference_value` | `_phase157_r20_specialize_reference_value` |
| 1060 | `_phase157_r20_specialize_reference_value` | `_phase157_r20_specialize_reference_value` |
| 1090 | `_phase157_r20_specialize_reference_value` | `_phase157_r20_specialize_reference_value` |
| 1103 | `_phase157_r20_specialize_reference_value` | `_phase157_r20_specialize_reference_value` |
| 1117 | `_phase157_r20_specialize_reference_value` | `_phase157_r20_specialize_reference_value` |
| 1144 | `_phase157_r20_specialize_reference_value` | `_phase157_r20_specialize_reference_value` |
| 1379 | `_phase157_r20_specialize_reference_relation` | `_phase157_r20_reference_descendants` |
| 1414 | `_phase157_r20_specialize_reference_relation` | `_phase157_r20_reference_scalar_value` |
| 1421 | `_phase157_r20_specialize_reference_relation` | `_phase157_r20_reference_scalar_value` |
| 1437 | `_phase157_r20_specialize_reference_relation` | `_phase157_r20_reference_range_allows` |
| 1446 | `_phase157_r20_specialize_reference_relation` | `_phase157_r20_specialize_reference_value` |
| 1534 | `_phase153_r6_reference_aggregate_component` | `extract_toda_group_proof_step_literature_reference` |
| 1573 | `_phase153_r6_reference_aggregate_component` | `_phase157_r20_specialize_reference_relation` |
| 1626 | `_phase153_r6_render_reference_statement` | `_phase153_r6_reference_aggregate_component` |
| 1636 | `_phase153_r6_render_reference_statement` | `project_reference_component_step` |
| 1674 | `build_toda_group_proof_narrative_reference_reuse_marker_by_step_id` | `_is_toda_group_proof_narrative_reference_statement_candidate` |
| 1692 | `build_toda_group_proof_narrative_reference_reuse_marker_by_step_id` | `select_toda_group_proof_narrative_reference_statement_steps` |
| 1870 | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | `_phase157_r20_canonical_fixed_reference_line` |
| 1877 | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | `_is_toda_group_proof_narrative_reference_statement_candidate` |
| 1903 | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | `select_toda_group_proof_narrative_reference_statement_steps` |
| 1916 | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | `_phase153_r6_reference_aggregate_component` |
| 1950 | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | `_phase153_r6_reference_aggregate_component` |
| 2029 | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | `_phase157_r20_canonical_fixed_reference_line` |
| 2031 | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | `_phase153_r6_render_reference_statement` |
| 2047 | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | `_phase157_r5_r7_order_and_connect_fixed_definition_reference_lines` |
| 2080 | `_toda_group_proof_narrative_reference_statement_lines_by_number` | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` |
| 2191 | `suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry` | `_phase153_r6_reference_aggregate_component` |
| 2212 | `suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry` | `aggregate_reference_labels.add` |
| 2357 | `_phase154_r5_reference_source_steps_by_number` | `select_toda_group_proof_narrative_reference_statement_steps` |
| 2372 | `_phase154_r5_reference_source_steps_by_number` | `_phase153_r6_reference_aggregate_component` |
| 2626 | `link_toda_group_proof_narrative_reference_body_consumers` | `_phase154_r5_reference_source_steps_by_number` |
| 2966 | `suppress_toda_group_proof_narrative_reference_body_restatements` | `statement_lines_by_reference_number.items` |
| 3111 | `suppress_toda_group_proof_narrative_repeated_reference_restatements` | `statement_lines_by_reference_number.items` |
| 3150 | `suppress_toda_group_proof_narrative_repeated_reference_restatements` | `reference_keys.add` |
| 3151 | `suppress_toda_group_proof_narrative_repeated_reference_restatements` | `_phase157_r11_reference_statement_match_key` |
| 3195 | `suppress_toda_group_proof_narrative_repeated_reference_restatements` | `_phase157_r11_reference_statement_match_key` |
| 3209 | `suppress_toda_group_proof_narrative_repeated_reference_restatements` | `seen_reference_keys.add` |
| 3306 | `suppress_toda_group_proof_narrative_reference_body_duplicates` | `statement_lines_by_reference_number.items` |
| 3358 | `suppress_toda_group_proof_narrative_reference_body_duplicates` | `_phase157_r11_reference_statement_match_key` |
| 3363 | `suppress_toda_group_proof_narrative_reference_body_duplicates` | `_phase157_r11_reference_statement_match_key` |
| 3617 | `_toda_group_proof_narrative_reference_owned_step_ids` | `extract_toda_group_proof_step_literature_reference` |
| 3834 | `_toda_group_proof_narrative_reference_internal_step_ids` | `_is_toda_group_proof_narrative_reference_statement_candidate` |
| 3852 | `_toda_group_proof_narrative_reference_internal_step_ids` | `select_toda_group_proof_narrative_reference_statement_steps` |
| 3870 | `_toda_group_proof_narrative_reference_internal_step_ids` | `_toda_group_proof_narrative_reference_owned_step_ids` |
| 3916 | `_phase157_r5_r9_selected_fixed_definition_step_ids` | `_is_toda_group_proof_narrative_reference_statement_candidate` |
| 3937 | `_phase157_r5_r9_selected_fixed_definition_step_ids` | `select_toda_group_proof_narrative_reference_statement_steps` |
| 4021 | `suppress_toda_group_proof_narrative_reference_internal_body` | `_toda_group_proof_narrative_reference_internal_step_ids` |
| 4154 | `_toda_group_proof_narrative_reference_externally_used_step_ids` | `_toda_group_proof_narrative_reference_internal_step_ids` |
| 4208 | `_toda_group_proof_narrative_reference_frontier_step_ids` | `extract_toda_group_proof_step_literature_reference` |
| 4258 | `_toda_group_proof_narrative_reference_frontier_step_ids` | `extract_toda_group_proof_step_literature_reference` |
| 4686 | `normalize_toda_group_proof_narrative_zero_map_exactness_reason` | `_phase157_r11_reference_statement_match_key` |
| 4686 | `paragraph_match_key` | `_phase157_r11_reference_statement_match_key` |
| 4927 | `order_toda_group_proof_narrative_visible_step_dependencies` | `_phase157_r11_reference_statement_match_key` |
| 4927 | `paragraph_match_key` | `_phase157_r11_reference_statement_match_key` |
| 4948 | `order_toda_group_proof_narrative_visible_step_dependencies` | `_phase157_r11_reference_statement_match_key` |
| 5267 | `order_toda_group_proof_narrative_visible_relation_dependencies` | `_phase157_r11_reference_statement_match_key` |
| 5267 | `paragraph_match_key` | `_phase157_r11_reference_statement_match_key` |
| 5285 | `order_toda_group_proof_narrative_visible_relation_dependencies` | `_phase157_r11_reference_statement_match_key` |
| 5285 | `paragraph_index_for_step` | `_phase157_r11_reference_statement_match_key` |
| 5399 | `suppress_toda_group_proof_narrative_repeated_unique_step_statements` | `_phase157_r11_reference_statement_match_key` |
| 5399 | `normalized_step_key` | `_phase157_r11_reference_statement_match_key` |
| 5727 | `order_toda_group_proof_narrative_order_support` | `_phase157_r11_reference_statement_match_key` |
| 5727 | `paragraph_match_key` | `_phase157_r11_reference_statement_match_key` |
| 5745 | `order_toda_group_proof_narrative_order_support` | `_phase157_r11_reference_statement_match_key` |
| 5745 | `paragraph_index_for_step` | `_phase157_r11_reference_statement_match_key` |
| 6022 | `suppress_toda_group_proof_narrative_reflexive_equalities` | `_phase157_r11_reference_statement_match_key` |
| 6053 | `suppress_toda_group_proof_narrative_reflexive_equalities` | `_phase157_r11_reference_statement_match_key` |
| 6155 | `order_toda_group_proof_narrative_surjectivity_support` | `_phase157_r11_reference_statement_match_key` |
| 6155 | `paragraph_match_key` | `_phase157_r11_reference_statement_match_key` |
| 6156 | `order_toda_group_proof_narrative_surjectivity_support` | `strip_reference_prefix` |
| 6156 | `paragraph_match_key` | `strip_reference_prefix` |
| 6175 | `order_toda_group_proof_narrative_surjectivity_support` | `_phase157_r11_reference_statement_match_key` |
| 6175 | `paragraph_index_for_step` | `_phase157_r11_reference_statement_match_key` |
| 6305 | `order_toda_group_proof_narrative_surjectivity_support` | `strip_reference_prefix` |
| 6345 | `order_toda_group_proof_narrative_surjectivity_support` | `strip_reference_prefix` |
| 6369 | `order_toda_group_proof_narrative_surjectivity_support` | `statement_lines_by_reference_number.get` |
| 6383 | `order_toda_group_proof_narrative_surjectivity_support` | `reference_matches.append` |
| 6425 | `order_toda_group_proof_narrative_surjectivity_support` | `strip_reference_prefix` |
| 6490 | `order_toda_group_proof_narrative_surjectivity_support` | `strip_reference_prefix` |
| 6601 | `order_toda_group_proof_narrative_short_exact_support` | `_phase157_r11_reference_statement_match_key` |
| 6601 | `match_key` | `_phase157_r11_reference_statement_match_key` |
| 6885 | `insert_toda_group_proof_narrative_reference_map_values_before_surjectivity` | `statement_lines_by_reference_number.items` |
| 7266 | `insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges` | `_phase157_r11_reference_statement_match_key` |
| 7266 | `match_key` | `_phase157_r11_reference_statement_match_key` |
| 7291 | `insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges` | `extract_toda_group_proof_step_literature_reference` |
| 7291 | `reference_entry_for_step` | `extract_toda_group_proof_step_literature_reference` |
| 7332 | `insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges` | `reference_entry_for_step` |
| 7332 | `display_line` | `reference_entry_for_step` |
| 7338 | `insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges` | `_phase153_r6_render_reference_statement` |
| 7338 | `display_line` | `_phase153_r6_render_reference_statement` |
| 7346 | `insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges` | `_phase157_r20_canonical_fixed_reference_line` |
| 7346 | `display_line` | `_phase157_r20_canonical_fixed_reference_line` |
| 7603 | `insert_toda_group_proof_narrative_map_property_dependencies` | `_phase157_r11_reference_statement_match_key` |
| 7603 | `match_key` | `_phase157_r11_reference_statement_match_key` |
| 7628 | `insert_toda_group_proof_narrative_map_property_dependencies` | `extract_toda_group_proof_step_literature_reference` |
| 7628 | `reference_entry_for_step` | `extract_toda_group_proof_step_literature_reference` |
| 7660 | `insert_toda_group_proof_narrative_map_property_dependencies` | `reference_entry_for_step` |
| 7660 | `reference_number_for_step` | `reference_entry_for_step` |
| 7681 | `insert_toda_group_proof_narrative_map_property_dependencies` | `reference_entry_for_step` |
| 7681 | `display_line` | `reference_entry_for_step` |
| 7687 | `insert_toda_group_proof_narrative_map_property_dependencies` | `_phase153_r6_render_reference_statement` |
| 7687 | `display_line` | `_phase153_r6_render_reference_statement` |
| 7695 | `insert_toda_group_proof_narrative_map_property_dependencies` | `_phase157_r20_canonical_fixed_reference_line` |
| 7695 | `display_line` | `_phase157_r20_canonical_fixed_reference_line` |
| 7702 | `insert_toda_group_proof_narrative_map_property_dependencies` | `reference_number_for_step` |
| 7702 | `display_line` | `reference_number_for_step` |
| 7953 | `insert_toda_group_proof_narrative_hidden_zero_map_premises` | `_phase157_r11_reference_statement_match_key` |
| 7953 | `match_key` | `_phase157_r11_reference_statement_match_key` |
| 8676 | `link_toda_group_proof_narrative_unmarked_reference_consumers` | `extract_toda_group_proof_step_literature_reference` |
| 8814 | `order_toda_group_proof_narrative_local_equation_derivations` | `_toda_group_proof_narrative_two_equation_reference_numbers` |
| 8937 | `_phase159_r1_7c_r3_specialize_primary_group` | `_phase157_r20_reference_scalar_value` |
| 8944 | `_phase159_r1_7c_r3_specialize_primary_group` | `_phase157_r20_reference_scalar_value` |
| 9047 | `_phase159_r1_7c_r3_aggregate_zero_specializes_to` | `_phase157_r20_reference_scalar_value` |
| 9054 | `_phase159_r1_7c_r3_aggregate_zero_specializes_to` | `_phase157_r20_reference_scalar_value` |
| 9364 | `_phase159_r1_7c_r3_specialized_zero_paragraph` | `_phase159_r1_7c_r3_reference_marker` |
| 9395 | `_phase159_r1_7c_r3_specialized_decomposition_paragraph` | `_phase159_r1_7c_r3_reference_marker` |
| 9710 | `_phase159_r1_7c_r3_repair4_aggregate_zero_component_line` | `_phase157_r20_reference_scalar_value` |
| 9715 | `_phase159_r1_7c_r3_repair4_aggregate_zero_component_line` | `_phase157_r20_reference_scalar_value` |
| 9820 | `prune_toda_group_proof_narrative_root_zero_direct_premise_references` | `extract_toda_group_proof_step_literature_reference` |
| 9828 | `prune_toda_group_proof_narrative_root_zero_direct_premise_references` | `required_by_reference.setdefault` |
| 9849 | `prune_toda_group_proof_narrative_root_zero_direct_premise_references` | `required_by_reference.get` |
| 9896 | `prune_toda_group_proof_narrative_root_zero_direct_premise_references` | `_toda_group_proof_narrative_reference_statement_lines_by_number` |
| 9904 | `prune_toda_group_proof_narrative_root_zero_direct_premise_references` | `required_by_reference.get` |
| 10461 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `build_toda_group_proof_narrative_reference_entries` |
| 10466 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary` |
| 10475 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` |
| 10490 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `exclude_toda_group_proof_narrative_root_reference` |
| 10498 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `_toda_group_proof_narrative_reference_owned_step_ids` |
| 10530 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `suppress_toda_group_proof_narrative_reference_internal_body` |
| 10546 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `suppress_toda_group_proof_narrative_reference_body_duplicates` |
| 10552 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `link_toda_group_proof_narrative_reference_body_consumers` |
| 10618 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `link_toda_group_proof_narrative_unmarked_reference_consumers` |
| 10645 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `suppress_toda_group_proof_narrative_repeated_reference_restatements` |
| 10750 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `filter_toda_group_proof_narrative_reference_entries_by_body_usage` |
| 10761 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage` |
| 10773 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `link_toda_group_proof_narrative_unmarked_reference_consumers` |
| 10781 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `_toda_group_proof_narrative_reference_frontier_step_ids` |
| 10796 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `filter_toda_group_proof_narrative_reference_entries_by_step_usage` |
| 10810 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `filter_toda_group_proof_narrative_reference_entries_by_body_usage` |
| 10821 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `prune_toda_group_proof_narrative_root_zero_direct_premise_references` |
| 10842 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `link_toda_group_proof_narrative_reference_body_consumers` |
| 10850 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `render_toda_group_proof_narrative_reference_entries_markdown` |
| 10867 | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | `public_reference_section.startswith` |

## テキスト依存・再判定候補

| ファイル:行 | 関数 | 分類・条件 |
|---|---|---|
| `toda_group_proof_narrative_contribution_renderer.py:9335` | `_phase159_r1_7c_r3_reference_marker` | text-dependent citation decision: `not stripped.startswith(
    "[R"
  )` |
| `toda_group_proof_narrative_contribution_renderer.py:10744` | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | text-dependent citation decision: `"[R" in rendered` |
| `toda_group_proof_narrative_contribution_renderer.py:10804` | `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown` | text-dependent citation decision: `"[R" in rendered` |
| `toda_group_proof_narrative_contribution_renderer.py:3168` | `suppress_toda_group_proof_narrative_repeated_reference_restatements` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:4436` | `numbered_connector_numbers` | text-dependent citation decision: `not stripped.startswith(
        "("
      )
      or not stripped.endswith(
        "より,"
      )
      or "$" in stripped
      or "[R" in stripped` |
| `toda_group_proof_narrative_contribution_renderer.py:4870` | `strip_leading_prose` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:5240` | `paragraph_match_key` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:5711` | `paragraph_match_key` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:5880` | `suppress_toda_group_proof_narrative_literal_reflexive_equalities` | text-dependent citation decision: `comparable.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:6037` | `suppress_toda_group_proof_narrative_reflexive_equalities` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:6120` | `strip_reference_prefix` | text-dependent citation decision: `not stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:6574` | `match_key` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:7250` | `match_key` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:7587` | `match_key` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:7937` | `match_key` | text-dependent citation decision: `stripped.startswith(
      "[R"
    )` |
| `toda_group_proof_narrative_contribution_renderer.py:1673` | `build_toda_group_proof_narrative_reference_reuse_marker_by_step_id` | text-dependent citation decision: `not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      )` |
| `toda_group_proof_narrative_contribution_renderer.py:1876` | `_select_toda_group_proof_narrative_reference_entries_and_statement_lines` | text-dependent citation decision: `not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      )` |
| `toda_group_proof_narrative_contribution_renderer.py:2697` | `link_toda_group_proof_narrative_reference_body_consumers` | text-dependent citation decision: `existing.startswith("[R")` |
| `toda_group_proof_narrative_contribution_renderer.py:2877` | `link_toda_group_proof_narrative_reference_body_consumers` | text-dependent citation decision: `earlier_line.strip().startswith("[R")` |
| `toda_group_proof_narrative_contribution_renderer.py:3833` | `_toda_group_proof_narrative_reference_internal_step_ids` | text-dependent citation decision: `not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      )` |
| `toda_group_proof_narrative_contribution_renderer.py:3915` | `_phase157_r5_r9_selected_fixed_definition_step_ids` | text-dependent citation decision: `not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      )` |
| `toda_group_proof_narrative_contribution_renderer.py:4577` | `suppress_toda_group_proof_narrative_dangling_connectors` | text-dependent citation decision: `stripped.startswith(
          prefix
          + "[R"
        )` |
| `toda_group_proof_narrative_references.py:958` | `filter_toda_group_proof_narrative_reference_entries_by_step_usage` | candidate proof/text reconciliation (review manually): `` |
| `toda_group_proof_narrative_references.py:1104` | `filter_toda_group_proof_narrative_reference_entries_by_body_usage` | candidate proof/text reconciliation (review manually): `` |
| `toda_group_proof_narrative_references.py:1260` | `restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage` | candidate proof/text reconciliation (review manually): `` |
| `toda_group_proof_narrative_references.py:1717` | `restore_phase157_r4_representative_fixed_reference_entries_after_body_usage` | candidate proof/text reconciliation (review manually): `` |

## 関連テスト

- `tests/test_phase167_r2_unified_reference.py` — test_phase167_r2_pi32_reference_uses_general_form, test_phase167_r2_pi43_reference_uses_general_form
- `tests/test_phase167_r2_shared_reference.py` — test_phase167_r2_pi43_reference_has_two_general_results, test_phase167_r2_other_references_keep_common_statement_lines
- `tests/test_phase157_r4_r3_reference_selection_integration.py` — test_phase157_r4_r3_filter_keeps_only_earlier_fixed_same_theorem_group_result, test_phase157_r4_r3_filter_removes_proof_internal_prop511_step, test_phase157_r4_r3_filter_is_noop_outside_representative_targets
- `tests/test_phase157_r4_r3_repair1_reference_retention.py` — test_phase157_r4_r3_restore_uses_step_identity_without_hashing_recursive_proof_graph, test_phase157_r4_r3_restore_does_not_add_unused_fixed_reference
- `tests/test_phase153_r3_3_reference_statement_selection.py` — test_phase153_r3_3_single_candidate_is_selected, test_phase153_r3_3_proof_used_candidate_is_preferred, test_phase153_r3_3_keeps_all_distinct_proof_used_candidates_in_entry_order, test_phase153_r3_3_falls_back_to_first_candidate_when_none_is_proof_used
- `tests/test_phase164_r2_citation_eligibility.py` — test_reviewed_structured_earlier_statement_is_allowed, test_registration_is_not_verification, test_non_external_origins_denied_even_when_allowlisted, test_boundary_metadata_denied_even_when_allowlisted, test_self_citation_denied, test_later_or_simultaneous_completion_denied, test_unknown_order_fails_closed, test_missing_migration_record_fails_closed, test_unresolved_record_fails_closed, test_back_reference_dependency_denied, test_missing_dependency_fails_closed, test_unreviewed_dependency_fails_closed, test_unstructured_dependency_fails_closed_even_when_reviewed, test_invalid_parameters_rejected

## 判定原則（設計提案、現状事実ではない）

1. Proof Tree の実依存から GIVEN と INFERENCE の文献出典を収集する。
2. 掲載順・自己参照の妥当性は Search 側で保証する。
3. 同一文献を統合後、番号・本文引用・Reference セクションを一貫生成する。
4. `"[R" in rendered` 等の Markdown 文字列から採否を逆判定しない。
5. 実動作の確認には同じ presentation と同じ呼び出しで段階ごとの ID/件数を観測する。

## 制限

- AST 静的検査であり、分岐の実行条件・参照の正当性は自動確定しない。
- GitHub の develop とローカルツリーが異なる場合、結果はローカル側に基づく。
- π₄² の Reference 2件は目標値であり、実測として宣言しない。
