# Phase 165 R5-R10 旧 Narrative 依存の用途別監査

状態: **REVIEW_REQUIRED**

## 事前条件

- PASS: `all_target_modules_present`
- PASS: `no_ast_errors`
- PASS: `shared_leaf_dependency_retained`
- PASS: `all_four_targets_classified`

## ファイル別依存と撤去判定

### `phase162_web_narrative_integration.py`

- 判定: `RETAIN_UNTIL_APPLICATION_DEPENDENCIES_MIGRATED`
- 実行側の直接呼出件数: 1
- 実行側参照ファイル: phase162_pi5_3_web_replay.py
- アプリケーション: `phase162_pi5_3_web_replay.py:50` — `call` / `_phase162_ehp_leaves`
- アプリケーション: `phase162_pi5_3_web_replay.py` — `import` / `_phase162_ehp_leaves`
- テスト: `tests/test_phase162_r5_6_narrative_final_format.py:11` — `call` / `build_phase162_web_validated_isomorphism_markdown`
- テスト: `tests/test_phase162_r5_6_narrative_final_format.py:34` — `call` / `_format_phase162_proof_sentences`
- テスト: `tests/test_phase162_r5_6_narrative_final_format.py:50` — `call` / `_compose_phase162_group_conclusion`
- テスト: `tests/test_phase162_r5_6_narrative_final_format.py:55` — `call` / `_compose_phase162_group_conclusion`
- テスト: `tests/test_phase162_r5_6_narrative_final_format.py` — `import` / `_compose_phase162_group_conclusion`
- テスト: `tests/test_phase162_r5_6_narrative_final_format.py` — `import` / `_format_phase162_proof_sentences`
- テスト: `tests/test_phase162_r5_6_narrative_final_format.py` — `import` / `build_phase162_web_validated_isomorphism_markdown`
- テスト: `tests/test_phase162_r5_web_integration.py:12` — `call` / `build_phase162_web_validated_isomorphism_markdown`
- テスト: `tests/test_phase162_r5_web_integration.py:46` — `call` / `build_phase162_web_validated_isomorphism_markdown`
- テスト: `tests/test_phase162_r5_web_integration.py:55` — `call` / `build_phase162_web_validated_isomorphism_markdown`
- テスト: `tests/test_phase162_r5_web_integration.py` — `import` / `build_phase162_web_validated_isomorphism_markdown`

### `phase162_r3_narrative_connection.py`

- 判定: `RETAIN_UNTIL_APPLICATION_DEPENDENCIES_MIGRATED`
- 実行側の直接呼出件数: 1
- 実行側参照ファイル: phase162_web_narrative_integration.py
- アプリケーション: `phase162_web_narrative_integration.py:297` — `call` / `render_phase162_r3_narrative`
- アプリケーション: `phase162_web_narrative_integration.py` — `import` / `render_phase162_r3_narrative`
- テスト: `tests/test_phase162_r3_narrative_connection.py:41` — `call` / `render_phase162_r3_narrative`
- テスト: `tests/test_phase162_r3_narrative_connection.py:52` — `call` / `render_phase162_r3_narrative`
- テスト: `tests/test_phase162_r3_narrative_connection.py:100` — `call` / `render_phase162_r3_with_public_references`
- テスト: `tests/test_phase162_r3_narrative_connection.py:62` — `call` / `render_phase162_r3_narrative`
- テスト: `tests/test_phase162_r3_narrative_connection.py:73` — `call` / `render_phase162_r3_narrative`
- テスト: `tests/test_phase162_r3_narrative_connection.py:81` — `call` / `render_phase162_r3_narrative`
- テスト: `tests/test_phase162_r3_narrative_connection.py` — `import` / `render_phase162_r3_narrative`
- テスト: `tests/test_phase162_r3_narrative_connection.py` — `import` / `render_phase162_r3_with_public_references`

### `toda_group_proof_narrative_proof_chain_renderer.py`

- 判定: `NO_APPLICATION_IMPORT_FOUND_TEST_OR_EXTERNAL_API_REVIEW`
- 実行側の直接呼出件数: 0
- 実行側参照ファイル: 検出なし
- 監査: `audit_phase144_6_r5_20.py:397` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 監査: `audit_phase144_6_r5_20.py` — `import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 監査: `audit_phase144_6_r5_21.py:171` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 監査: `audit_phase144_6_r5_21.py` — `import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 監査: `audit_phase144_6_r5_23.py:148` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 監査: `audit_phase144_6_r5_23.py` — `import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 監査: `audit_phase144_6_r5_24.py:190` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 監査: `audit_phase144_6_r5_24.py` — `import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:41` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:116` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:145` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:177` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:201` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py` — `import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`

### `toda_group_proof_narrative_concrete_transport.py`

- 判定: `NO_APPLICATION_IMPORT_FOUND_TEST_OR_EXTERNAL_API_REVIEW`
- 実行側の直接呼出件数: 0
- 実行側参照ファイル: 検出なし
- テスト: `tests/test_phase162_r4_b3_common_renderer_fix.py:27` — `call` / `render_concrete_transport_proof_from_steps`
- テスト: `tests/test_phase162_r4_b3_common_renderer_fix.py:37` — `call` / `render_concrete_transport_proof_from_steps`
- テスト: `tests/test_phase162_r4_b3_common_renderer_fix.py` — `import` / `render_concrete_transport_proof_from_steps`

## 結論の境界

- Ownership classifies scripts by filename, not by Git tracking or runtime invocation.
- A static import or call is not evidence of live runtime execution.
- Dynamic imports, external consumers, monkeypatching and reflection may be missed.
- This stage does not remove any existing module or change proof rendering.
- Historical Phase 162 fixture failures remain unresolved.
- Full pytest is deferred until the end of Phase 165.
