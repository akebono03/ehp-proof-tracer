# Phase 165 Renderer R5 最終監査

判定: **STATIC_FAIL**

## 静的チェック

- PASS: `no_legacy_alias`
- FAIL: `no_legacy_imports`
- PASS: `one_public_complete_narrative_definition`
- PASS: `one_shared_model_dispatcher`
- PASS: `one_partial_narrative_definition`
- PASS: `partial_public_uses_model_dispatcher`
- PASS: `web_entry_uses_shared_adapter`
- PASS: `web_adapter_uses_public_narrative`
- PASS: `dispatcher_preserves_complete_and_incomplete`
- PASS: `model_preserves_proven_steps_and_open_goals`

## 件数

- scanned_python: 1175
- scan_scope: project_root_and_tests_only
- renderer_named_files: 120
- legacy_import_statements: 4
- canonical_public_complete_definitions: 1
- canonical_dispatchers: 1
- candidate_helper_renderers: 26

## 旧 import 残存

- `tests/test_phase162_r2_validated_proof_presentation.py:76`
- `tests/test_phase162_r2_validated_proof_presentation.py:159`
- `toda_group_proof_narrative_renderer.phase165_r43_backup.py:37`
- `toda_group_proof_narrative_renderer.phase165_r48_backup.py:37`

## 補助 Renderer 候補（存在だけで重複と判定しない）

- `phase162_r3_narrative_connection.py`: render_phase162_r3_narrative
- `phase165_r57_r10_step_narrative.py`: render_completed_from_proofsteps
- `phase165_r57_r2_partial_narrative.py`: render_incomplete_public_narrative
- `toda_full_proof_report_renderer.py`: render_toda_full_proof_report_markdown
- `toda_group_proof_aggregate_statement_renderer.py`: render_toda_group_proof_aggregate_statement_prose
- `toda_group_proof_generic_narrative_renderer.phase165_r42_backup.py`: render_toda_group_proof_generic_narrative_markdown, render_toda_group_proof_generic_proof_markdown
- `toda_group_proof_generic_narrative_renderer.phase165_r48_backup.py`: render_toda_group_proof_generic_narrative_markdown, render_toda_group_proof_generic_proof_markdown
- `toda_group_proof_generic_narrative_renderer.phase165_r48_sidecar_backup.py`: render_toda_group_proof_generic_narrative_markdown, render_toda_group_proof_generic_proof_markdown
- `toda_group_proof_narrative_argument_body_renderer.py`: render_toda_group_proof_narrative_argument_body_markdown
- `toda_group_proof_narrative_argument_discourse.py`: render_toda_group_proof_narrative_argument_discourse_marker
- `toda_group_proof_narrative_argument_multi_renderer.py`: render_toda_group_proof_narrative_multi_argument_markdown
- `toda_group_proof_narrative_argument_renderer.py`: render_toda_group_proof_narrative_argument_purpose_sentence, render_toda_group_proof_narrative_argument_header_method_section
- `toda_group_proof_narrative_argument_single_renderer.py`: render_toda_group_proof_narrative_single_argument_markdown
- `toda_group_proof_narrative_concrete_transport.py`: render_concrete_transport_proof_from_steps
- `toda_group_proof_narrative_contribution_renderer.py`: render_toda_group_proof_narrative_multi_argument_with_contributions_markdown
- `toda_group_proof_narrative_exactness_method_renderer.py`: render_toda_group_proof_narrative_exactness_method_transition, render_toda_group_proof_narrative_exactness_method_component_latex
- `toda_group_proof_narrative_proof_chain_renderer.py`: render_toda_group_proof_narrative_from_proof_chains_markdown
- `toda_group_proof_narrative_reason_renderer.py`: render_toda_group_proof_narrative_reason_sentence
- `toda_group_proof_narrative_references.py`: render_toda_group_proof_narrative_reference_entries_markdown
- `toda_group_proof_narrative_renderer.phase165_r43_backup.py`: render_toda_group_proof_narrative_markdown, render_toda_group_proof_narrative_markdown, render_toda_group_proof_narrative_markdown
- `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`: render_toda_group_proof_narrative_markdown, render_toda_group_proof_narrative_markdown, render_toda_group_proof_narrative_markdown
- `toda_group_proof_narrative_renderer.phase165_r48_backup.py`: render_toda_group_proof_narrative_markdown, render_toda_group_proof_narrative_markdown, render_toda_group_proof_narrative_markdown
- `toda_group_proof_narrative_transition_renderer.py`: render_toda_group_proof_narrative_transition_connector
- `toda_group_proof_outline_renderer.py`: render_toda_group_proof_outline_markdown
- `toda_group_result_proof_replay_renderer.py`: render_toda_group_result_proof_replay_markdown
- `toda_proof_narrative_renderer.py`: render_toda_proof_statement_latex, render_toda_proof_step_mathematical_markdown, render_toda_readable_proof_narrative_markdown

## 監査上の限界

- AST and source inspection alone cannot prove that no dynamic import, monkeypatch or untested path exists.
- Helper render functions are not necessarily separate public renderers; manual ownership classification remains required.
- This audit does not certify mathematical correctness or arbitrary-goal backward search completeness.
- Archived installer/backup directories are deliberately excluded; they can retain historical imports.
