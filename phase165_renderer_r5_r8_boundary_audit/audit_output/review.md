# Phase 165 R5-R8 公開境界監査

判定: **REVIEW_REQUIRED**

## 静的チェック

- PASS: `legacy_phase162_web_has_no_public_import_route`
- PASS: `legacy_phase162_narrative_has_no_public_import_route`
- PASS: `web_group_proof_imports_canonical`
- PASS: `no_ast_errors`

## 公開入口と旧経路・正規 Renderer の import 経路

### `web_group_proof.py`
- `toda_group_proof_narrative_renderer.py`: `web_group_proof.py` → `phase165_r52_r3_web_adapter.py` → `phase165_r52_partial_proof.py` → `toda_group_proof_narrative_renderer.py`
- `phase162_web_narrative_integration.py`: 検出なし
- `phase162_r3_narrative_connection.py`: 検出なし
### `main.py`
- `toda_group_proof_narrative_renderer.py`: `main.py` → `toda_group_proof_narrative_renderer.py`
- `phase162_web_narrative_integration.py`: 検出なし
- `phase162_r3_narrative_connection.py`: 検出なし
### `cli.py`
- `toda_group_proof_narrative_renderer.py`: `cli.py` → `phase165_r52_partial_proof.py` → `toda_group_proof_narrative_renderer.py`
- `phase162_web_narrative_integration.py`: 検出なし
- `phase162_r3_narrative_connection.py`: 検出なし
### `web_generator_proof.py`
- `toda_group_proof_narrative_renderer.py`: 検出なし
- `phase162_web_narrative_integration.py`: 検出なし
- `phase162_r3_narrative_connection.py`: 検出なし
### `web_generator_exploration.py`
- `toda_group_proof_narrative_renderer.py`: 検出なし
- `phase162_web_narrative_integration.py`: 検出なし
- `phase162_r3_narrative_connection.py`: 検出なし
### `web_generator_execution.py`
- `toda_group_proof_narrative_renderer.py`: 検出なし
- `phase162_web_narrative_integration.py`: 検出なし
- `phase162_r3_narrative_connection.py`: 検出なし
### `web_operation_query_proof.py`
- `toda_group_proof_narrative_renderer.py`: 検出なし
- `phase162_web_narrative_integration.py`: 検出なし
- `phase162_r3_narrative_connection.py`: 検出なし

## 旧 Phase 162 関連の直接 import 呼び出し

- `phase162_pi5_3_web_replay.py:50` → `phase162_web_narrative_integration.py` / `_phase162_ehp_leaves`
- `phase162_web_narrative_integration.py:297` → `phase162_r3_narrative_connection.py` / `render_phase162_r3_narrative`

## 境界関数に対する直接呼出元

### `build_phase162_web_validated_isomorphism_markdown`
- 検出なし
### `render_phase162_r3_narrative`
- `phase162_web_narrative_integration.py:297` → `phase162_r3_narrative_connection.py`
### `render_toda_group_proof_outline_markdown`
- 検出なし
### `render_toda_group_result_proof_replay_markdown`
- 検出なし

## 公開・旧関数の内部で呼ばれる名前（関数単位の補助証拠）

- `cli.py:_run_group_command:74`: `_write_markdown`, `build_standard_toda_partial_result`, `print`, `render_partial_proof_markdown`
- `cli.py:_run_element_command:94`: `_write_markdown`, `len`, `print`, `render_toda_proof_statement_latex`, `repr`, `resolve_generator_input`, `search_typed_generator_statements`, `strip`
- `main.py:_run_show_proof_command:874`: `ValueError`, `build_show_proof_argument_parser`, `error`, `isinstance`, `len`, `print`, `render_toda_proof_statement_latex`, `search_typed_generator_statements`, `str`
- `main.py:_run_group_proof_command:910`: `TodaGroupQuery`, `ValueError`, `classify_toda_group_query_domain`, `isinstance`, `print`, `render_partial_proof_markdown`, `render_toda_group_query_domain_cli_message`, `search_group_structure_automatically`
- `phase162_web_narrative_integration.py:build_phase162_web_validated_isomorphism_markdown:288`: `ValueError`, `_build_phase162_existing_group_connection`, `_build_phase162_legacy_validated_isomorphism_markdown`, `render_phase162_r3_narrative`
- `phase165_r52_partial_proof.py:render_partial_proof_markdown:90`: `TypeError`, `build_narrative_proof_model`, `isinstance`, `render_narrative_proof_model`
- `phase165_r52_r3_web_adapter.py:build_partial_web_group_proof_view:19`: `TypeError`, `ValueError`, `WebGroupProofStepView`, `WebGroupProofView`, `_build_group_proof_rendered_lines`, `_group_proof_rule_name`, `_group_proof_statement_latex`, `append`, `isinstance`, `render_partial_proof_markdown`, `tuple`
- `toda_group_proof_outline_renderer.py:render_toda_group_proof_outline_markdown:126`: `TypeError`, `_append_outline_children`, `_render_group_proof_outline_statement`, `isinstance`, `join`, `set`
- `toda_group_result_proof_replay_renderer.py:render_toda_group_result_proof_replay_markdown:54`: `TypeError`, `_group_result_proof_replay_rule_name`, `_render_group_result_proof_replay_statement`, `enumerate`, `extend`, `isinstance`, `join`
- `web_group_proof.py:build_standard_web_group_proof_view:44`: `TodaGroupQuery`, `TypeError`, `ValueError`, `build_partial_web_group_proof_view`, `classify_toda_group_query_domain`, `isinstance`, `search_group_from_registered_goal`

## 限界

- Import connectivity is an overapproximation of execution, not a runtime function-level proof.
- No import path does not exclude dynamic imports, imports through packages, monkeypatching or reflection.
- Public root list covers known Web/CLI entry modules only; all possible callers are not enumerated.
- A function name with no detected imported calls may be used indirectly or externally.
- The historical Phase 162 fixture failures are not resolved by this audit.
- No mathematical validation and no full pytest are performed.
