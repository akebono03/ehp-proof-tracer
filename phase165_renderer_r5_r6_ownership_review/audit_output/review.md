# Phase 165 R5-R6 所有経路の分類監査

判定: **REVIEW_REQUIRED**

## 件数

- candidates: 26
- historical_backups: 6
- owned_subroutine_review: 2
- component_review: 11
- other_presentation_review: 4
- legacy_chain_review: 3

## 26候補の分類（未認定）

### `phase162_r3_narrative_connection.py`
- 分類: `LEGACY_OR_SPECIALIZED_CHAIN_REVIEW`
- 関数: `render_phase162_r3_narrative`
- 本番呼出元: `phase162_web_narrative_integration.py`
- 正規 Renderer から直接呼び出し: False

### `phase165_r57_r10_step_narrative.py`
- 分類: `CANONICAL_OWNED_SUBROUTINE_REVIEW`
- 関数: `render_completed_from_proofsteps`
- 本番呼出元: `phase165_r56_presentation_adapter.py`, `toda_group_proof_narrative_renderer.py`
- 正規 Renderer から直接呼び出し: True

### `phase165_r57_r2_partial_narrative.py`
- 分類: `CANONICAL_OWNED_SUBROUTINE_REVIEW`
- 関数: `render_incomplete_public_narrative`
- 本番呼出元: `toda_group_proof_narrative_renderer.py`
- 正規 Renderer から直接呼び出し: True

### `toda_full_proof_report_renderer.py`
- 分類: `OTHER_PRESENTATION_SURFACE_REVIEW`
- 関数: `render_toda_full_proof_report_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_aggregate_statement_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_aggregate_statement_prose`
- 本番呼出元: `toda_group_proof_narrative_shared_components.py`
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_generic_narrative_renderer.phase165_r42_backup.py`
- 分類: `HISTORICAL_BACKUP`
- 関数: `render_toda_group_proof_generic_narrative_markdown`, `render_toda_group_proof_generic_proof_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_generic_narrative_renderer.phase165_r48_backup.py`
- 分類: `HISTORICAL_BACKUP`
- 関数: `render_toda_group_proof_generic_narrative_markdown`, `render_toda_group_proof_generic_proof_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_generic_narrative_renderer.phase165_r48_sidecar_backup.py`
- 分類: `HISTORICAL_BACKUP`
- 関数: `render_toda_group_proof_generic_narrative_markdown`, `render_toda_group_proof_generic_proof_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_argument_body_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_argument_body_markdown`
- 本番呼出元: `toda_group_proof_narrative_argument_multi_renderer.py`, `toda_group_proof_narrative_argument_single_renderer.py`
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_argument_discourse.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_argument_discourse_marker`
- 本番呼出元: `toda_group_proof_narrative_argument_multi_renderer.py`, `toda_group_proof_narrative_argument_renderer.py`, `toda_group_proof_narrative_contribution_renderer.py`
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_argument_multi_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_multi_argument_markdown`
- 本番呼出元: `toda_group_proof_narrative_contribution_ordering.py`, `toda_group_proof_narrative_contribution_renderer.py`, `toda_group_proof_narrative_proof_chain_renderer.py`
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_argument_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_argument_purpose_sentence`, `render_toda_group_proof_narrative_argument_header_method_section`
- 本番呼出元: `toda_group_proof_narrative_argument_multi_renderer.py`, `toda_group_proof_narrative_argument_single_renderer.py`, `toda_group_proof_narrative_contribution_renderer.py`
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_argument_single_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_single_argument_markdown`
- 本番呼出元: `toda_group_proof_narrative_argument_multi_renderer.py`
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_concrete_transport.py`
- 分類: `LEGACY_OR_SPECIALIZED_CHAIN_REVIEW`
- 関数: `render_concrete_transport_proof_from_steps`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_contribution_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`
- 本番呼出元: `toda_group_proof_narrative_renderer.py`
- 正規 Renderer から直接呼び出し: True

### `toda_group_proof_narrative_exactness_method_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_exactness_method_transition`, `render_toda_group_proof_narrative_exactness_method_component_latex`
- 本番呼出元: `toda_group_proof_narrative_argument_renderer.py`, `toda_group_proof_narrative_renderer.py`
- 正規 Renderer から直接呼び出し: True

### `toda_group_proof_narrative_proof_chain_renderer.py`
- 分類: `LEGACY_OR_SPECIALIZED_CHAIN_REVIEW`
- 関数: `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_reason_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_reason_sentence`
- 本番呼出元: `phase162_r3g_existing_reason_bridge.py`, `phase162_r3h_reason_inventory.py`, `phase162_r3i_semantic_sidecar_audit.py`, `toda_group_proof_narrative_contribution_renderer.py`, `toda_group_proof_narrative_reason_renderer.py`
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_references.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_reference_entries_markdown`
- 本番呼出元: `phase162_r4_b3_renderer_audit.py`, `phase162_validated_proof_presentation.py`, `phase165_r14_r43_reference_reason.phase165_r44_removed.py`, `toda_group_proof_narrative_concrete_transport.py`, `toda_group_proof_narrative_contribution_renderer.py`, `toda_group_proof_narrative_renderer.py`
- 正規 Renderer から直接呼び出し: True

### `toda_group_proof_narrative_renderer.phase165_r43_backup.py`
- 分類: `HISTORICAL_BACKUP`
- 関数: `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`
- 分類: `HISTORICAL_BACKUP`
- 関数: `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_renderer.phase165_r48_backup.py`
- 分類: `HISTORICAL_BACKUP`
- 関数: `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`, `render_toda_group_proof_narrative_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_narrative_transition_renderer.py`
- 分類: `SECTION_OR_MATH_COMPONENT_REVIEW`
- 関数: `render_toda_group_proof_narrative_transition_connector`
- 本番呼出元: `toda_group_proof_narrative_argument_multi_renderer.py`
- 正規 Renderer から直接呼び出し: False

### `toda_group_proof_outline_renderer.py`
- 分類: `OTHER_PRESENTATION_SURFACE_REVIEW`
- 関数: `render_toda_group_proof_outline_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_group_result_proof_replay_renderer.py`
- 分類: `OTHER_PRESENTATION_SURFACE_REVIEW`
- 関数: `render_toda_group_result_proof_replay_markdown`
- 本番呼出元: 静的検出なし
- 正規 Renderer から直接呼び出し: False

### `toda_proof_narrative_renderer.py`
- 分類: `OTHER_PRESENTATION_SURFACE_REVIEW`
- 関数: `render_toda_proof_statement_latex`, `render_toda_proof_step_mathematical_markdown`, `render_toda_readable_proof_narrative_markdown`
- 本番呼出元: `cli.py`, `main.py`, `phase162_r3e_structured_root_renderer.py`, `toda_full_proof_report_renderer.py`, `toda_group_proof_aggregate_statement_renderer.py`, `toda_group_proof_narrative_concrete_transport.py`, `toda_group_proof_narrative_contribution_renderer.py`, `toda_group_proof_narrative_exactness_method_renderer.py`, `toda_group_proof_narrative_reason_renderer.py`, `toda_group_proof_narrative_renderer.py`, `toda_group_proof_narrative_shared_components.py`, `toda_group_proof_outline_renderer.py`, `toda_group_result_proof_replay_renderer.py`, `toda_group_structure_transport_reason.py`, `web_generator_execution.py`, `web_generator_exploration.py`, `web_generator_proof.py`, `web_group_proof_common.py`, `web_operation_query.py`, `web_operation_query_proof.py`
- 正規 Renderer から直接呼び出し: True

## 主要な公開経路の import 証拠

### `cli.py`
- `82`: `phase165_r52_partial_proof.render_partial_proof_markdown`
- `102`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`

### `main.py`
- `1`: `phase165_r52_partial_proof.ProofSearchStatus`
- `1`: `phase165_r52_partial_proof.render_partial_proof_markdown`
- `53`: `toda_group_proof_narrative_renderer.render_toda_group_proof_narrative_markdown`
- `59`: `toda_group_proof_outline_renderer.render_toda_group_proof_outline_markdown`
- `71`: `toda_group_result_proof_replay_renderer.render_toda_group_result_proof_replay_markdown`
- `810`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`
- `830`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`
- `876`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`
- `949`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`
- `993`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`
- `1017`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`

### `phase162_validated_proof_presentation.py`
- `22`: `toda_group_proof_narrative_references.TodaGroupProofNarrativeReferenceEntry`
- `22`: `toda_group_proof_narrative_references.extract_toda_group_proof_step_literature_reference`
- `22`: `toda_group_proof_narrative_references.render_toda_group_proof_narrative_reference_entries_markdown`
- `30`: `toda_group_proof_narrative_renderer._render_group_proof_narrative_latex`

### `phase162_web_narrative_integration.py`
- `29`: `phase162_r3_narrative_connection.render_phase162_r3_narrative`

### `phase165_r52_partial_proof.py`
- `95`: `toda_group_proof_narrative_renderer.render_narrative_proof_model`

### `phase165_r52_r3_web_adapter.py`
- `9`: `phase165_r52_partial_proof.PartialProofResult`
- `9`: `phase165_r52_partial_proof.ProofSearchStatus`
- `9`: `phase165_r52_partial_proof.render_partial_proof_markdown`

### `phase165_r56_presentation_adapter.py`
- `9`: `phase165_r52_partial_proof.PartialProofResult`
- `9`: `phase165_r52_partial_proof.ProofSearchStatus`
- `15`: `toda_group_proof_narrative_renderer.render_toda_group_proof_narrative_markdown`
- `59`: `toda_group_proof_narrative_renderer._phase160_r7_render_stable_finite_cyclic_transport_narrative`
- `62`: `phase165_r57_r10_step_narrative.has_transport_proof_ancestry`
- `62`: `phase165_r57_r10_step_narrative.render_completed_from_proofsteps`

### `phase165_r57_r2_partial_narrative.py`
- `7`: `phase165_r52_partial_proof.GroupStructureStatus`
- `7`: `phase165_r52_partial_proof.PartialProofResult`
- `7`: `phase165_r52_partial_proof.ProofSearchStatus`

### `toda_group_proof_narrative_renderer.py`
- `47`: `toda_group_proof_narrative_argument_multi_renderer.render_toda_group_proof_narrative_multi_argument_markdown`
- `50`: `toda_group_proof_narrative_contribution_renderer._toda_group_proof_narrative_reference_statement_lines_by_number`
- `50`: `toda_group_proof_narrative_contribution_renderer.build_toda_group_proof_narrative_reference_reuse_marker_by_step_id`
- `50`: `toda_group_proof_narrative_contribution_renderer.link_toda_group_proof_narrative_reference_body_consumers`
- `50`: `toda_group_proof_narrative_contribution_renderer.render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`
- `50`: `toda_group_proof_narrative_contribution_renderer.suppress_toda_group_proof_narrative_dangling_connectors`
- `50`: `toda_group_proof_narrative_contribution_renderer.suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry`
- `50`: `toda_group_proof_narrative_contribution_renderer.suppress_toda_group_proof_narrative_reference_body_duplicates`
- `50`: `toda_group_proof_narrative_contribution_renderer.suppress_toda_group_proof_narrative_reference_body_restatements`
- `67`: `toda_group_proof_narrative_exactness_method_renderer.render_toda_group_proof_narrative_exactness_method_component_latex`
- `79`: `toda_group_proof_narrative_references.build_toda_group_proof_narrative_reference_entries`
- `79`: `toda_group_proof_narrative_references.exclude_toda_group_proof_narrative_root_reference`
- `79`: `toda_group_proof_narrative_references.filter_toda_group_proof_narrative_reference_entries_by_body_usage`
- `79`: `toda_group_proof_narrative_references.filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary`
- `79`: `toda_group_proof_narrative_references.render_toda_group_proof_narrative_reference_entries_markdown`
- `102`: `toda_proof_narrative_renderer.render_toda_primary_group_latex`
- `102`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`
- `102`: `toda_proof_narrative_renderer.render_toda_raw_group_structure_latex`
- `3722`: `toda_proof_narrative_renderer.render_toda_primary_group_latex`
- `3722`: `toda_proof_narrative_renderer.render_toda_raw_group_structure_latex`
- `11770`: `phase165_r52_partial_proof.PartialProofResult`
- `11770`: `phase165_r52_partial_proof.ProofSearchStatus`
- `11773`: `phase165_r56_presentation_adapter.render_completed_shared_narrative`
- `11775`: `phase165_r57_r2_partial_narrative.render_incomplete_public_narrative`
- `11808`: `phase165_r52_partial_proof.PartialProofResult`
- `11808`: `phase165_r52_partial_proof.ProofSearchStatus`
- `11853`: `phase165_r57_r10_step_narrative.ordered_proof_ancestry`
- `11936`: `phase165_r52_partial_proof.ProofSearchStatus`
- `11945`: `phase165_r56_presentation_adapter.render_completed_shared_narrative`

### `web_group_proof.py`
- `18`: `toda_proof_narrative_renderer.render_toda_proof_statement_latex`

## 次に手動で判断する境界

- Group Proof の Web 公開入口と、旧 Phase162 Web 入口が並行して有効か
- 完成証明の Provenance を維持したまま単一 Dispatcher が所有できるか
- CLI / Generator / Outline / Replay の表示を Group Proof Narrative と混同していないか
- 候補以外の独立 Narrative 関数が未検出のまま残っていないか
- 旧 Phase162 fixture 失敗6件は今回未解決

## 限界

- Static imports do not certify runtime control flow or absence of dynamic imports.
- The Phase162 fixture regression remains unresolved.
- No source code is changed; full pytest is not run.
- Categories are investigative ownership buckets, not integration certification.
