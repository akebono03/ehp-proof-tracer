# Phase 165 R5-R9 旧 Narrative 経路の撤去可否監査

判定: **REVIEW_REQUIRED**

## 事前チェック

- PASS: `target_files_exist`
- PASS: `no_parse_errors`
- PASS: `normal_web_not_reaching_legacy`

## 関数・モジュール別の判定

### `phase162_web_narrative_integration.py`

- 判定: `RETAIN_DEPENDENT_MODULE`
- 本番側参照: 2 件
- テスト側参照: 11 件
- 本番側: `phase162_pi5_3_web_replay.py:8` — `from_import` / `_phase162_ehp_leaves`
- 本番側: `phase162_pi5_3_web_replay.py:50` — `call` / `_phase162_ehp_leaves`
- テスト側: `tests/test_phase162_r5_6_narrative_final_format.py:3` — `from_import` / `_compose_phase162_group_conclusion`
- テスト側: `tests/test_phase162_r5_6_narrative_final_format.py:3` — `from_import` / `_format_phase162_proof_sentences`
- テスト側: `tests/test_phase162_r5_6_narrative_final_format.py:3` — `from_import` / `build_phase162_web_validated_isomorphism_markdown`
- テスト側: `tests/test_phase162_r5_6_narrative_final_format.py:11` — `call` / `build_phase162_web_validated_isomorphism_markdown`
- テスト側: `tests/test_phase162_r5_6_narrative_final_format.py:34` — `call` / `_format_phase162_proof_sentences`
- テスト側: `tests/test_phase162_r5_6_narrative_final_format.py:50` — `call` / `_compose_phase162_group_conclusion`
- テスト側: `tests/test_phase162_r5_6_narrative_final_format.py:55` — `call` / `_compose_phase162_group_conclusion`
- テスト側: `tests/test_phase162_r5_web_integration.py:6` — `from_import` / `build_phase162_web_validated_isomorphism_markdown`
- テスト側: `tests/test_phase162_r5_web_integration.py:12` — `call` / `build_phase162_web_validated_isomorphism_markdown`
- テスト側: `tests/test_phase162_r5_web_integration.py:46` — `call` / `build_phase162_web_validated_isomorphism_markdown`
- テスト側: `tests/test_phase162_r5_web_integration.py:55` — `call` / `build_phase162_web_validated_isomorphism_markdown`

### `phase162_r3_narrative_connection.py`

- 判定: `RETAIN_DEPENDENT_MODULE`
- 本番側参照: 2 件
- テスト側参照: 8 件
- 本番側: `phase162_web_narrative_integration.py:29` — `from_import` / `render_phase162_r3_narrative`
- 本番側: `phase162_web_narrative_integration.py:297` — `call` / `render_phase162_r3_narrative`
- テスト側: `tests/test_phase162_r3_narrative_connection.py:6` — `from_import` / `render_phase162_r3_narrative`
- テスト側: `tests/test_phase162_r3_narrative_connection.py:85` — `from_import` / `render_phase162_r3_with_public_references`
- テスト側: `tests/test_phase162_r3_narrative_connection.py:41` — `call` / `render_phase162_r3_narrative`
- テスト側: `tests/test_phase162_r3_narrative_connection.py:52` — `call` / `render_phase162_r3_narrative`
- テスト側: `tests/test_phase162_r3_narrative_connection.py:100` — `call` / `render_phase162_r3_with_public_references`
- テスト側: `tests/test_phase162_r3_narrative_connection.py:62` — `call` / `render_phase162_r3_narrative`
- テスト側: `tests/test_phase162_r3_narrative_connection.py:73` — `call` / `render_phase162_r3_narrative`
- テスト側: `tests/test_phase162_r3_narrative_connection.py:81` — `call` / `render_phase162_r3_narrative`

### `toda_group_proof_narrative_proof_chain_renderer.py`

- 判定: `RETAIN_DEPENDENT_MODULE`
- 本番側参照: 8 件
- テスト側参照: 6 件
- 本番側: `audit_phase144_6_r5_20.py:7` — `from_import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 本番側: `audit_phase144_6_r5_20.py:397` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 本番側: `audit_phase144_6_r5_21.py:23` — `from_import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 本番側: `audit_phase144_6_r5_21.py:171` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 本番側: `audit_phase144_6_r5_23.py:20` — `from_import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 本番側: `audit_phase144_6_r5_23.py:148` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 本番側: `audit_phase144_6_r5_24.py:33` — `from_import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- 本番側: `audit_phase144_6_r5_24.py:190` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト側: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:8` — `from_import` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト側: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:41` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト側: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:116` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト側: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:145` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト側: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:177` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- テスト側: `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:201` — `call` / `render_toda_group_proof_narrative_from_proof_chains_markdown`

### `toda_group_proof_narrative_concrete_transport.py`

- 判定: `RETAIN_TEST_CONTRACT_REVIEW`
- 本番側参照: 0 件
- テスト側参照: 3 件
- テスト側: `tests/test_phase162_r4_b3_common_renderer_fix.py:6` — `from_import` / `render_concrete_transport_proof_from_steps`
- テスト側: `tests/test_phase162_r4_b3_common_renderer_fix.py:27` — `call` / `render_concrete_transport_proof_from_steps`
- テスト側: `tests/test_phase162_r4_b3_common_renderer_fix.py:37` — `call` / `render_concrete_transport_proof_from_steps`

## 動的参照の可能性がある文字列

- `tests/test_phase162_r5_web_integration.py:21`: `phase162_web_narrative_integration.build_phase162_web_validated_isomorphism_markdown`
- `tests/test_phase162_r5_web_integration.py:38`: `phase162_web_narrative_integration.build_phase162_web_validated_isomorphism_markdown`
- `tests/test_phase165_goal_only_cutover.py:33`: `phase162_web_narrative_integration`

## 制約と次の境界

- No source files were removed or modified.
- Root-module static imports and direct calls do not establish all runtime reachability.
- Reflection, dynamic imports, external consumers, and indirect callable aliases require separate review.
- Absence of import does not by itself authorize deletion of a public API.
- Historical Phase162 fixture failures (6) remain unresolved and are not marked passing.
- Full pytest must only run at the end of Phase 165.
