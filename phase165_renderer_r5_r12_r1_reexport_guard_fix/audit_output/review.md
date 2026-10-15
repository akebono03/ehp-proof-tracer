# Phase 165 R5-R12 旧 Narrative 関数単位の撤去判定

判定: **REVIEW_REQUIRED**

## R5-R11 前提条件
- PASS: `r5_r11_shared_file_exists`
- PASS: `replay_imports_shared_leaves`
- PASS: `legacy_web_reexports_shared_leaves`
- PASS: `all_old_entry_symbols_defined_or_shared_reexported`
- PASS: `parse_errors_empty`

## 関数別の依存と暫定判定

### `phase162_web_narrative_integration:build_phase162_web_validated_isomorphism_markdown`
- 判定: `RETAIN_TEST_CONTRACT_REVIEW`
- 定義行: [251]
- 共通再公開: なし
- 同一ファイル内の呼出: 検出なし
- アプリケーション側の参照:
  - 検出なし
- テスト側の参照:
  - `tests/test_phase162_r5_6_narrative_final_format.py`: [{'line': 3, 'kind': 'import'}, {'line': 11, 'kind': 'call'}]
  - `tests/test_phase162_r5_web_integration.py`: [{'line': 6, 'kind': 'import'}, {'line': 12, 'kind': 'call'}, {'line': 46, 'kind': 'call'}, {'line': 55, 'kind': 'call'}]

### `phase162_web_narrative_integration:_build_phase162_legacy_validated_isomorphism_markdown`
- 判定: `RETAIN_INTERNAL_DEPENDENCY_REVIEW`
- 定義行: [100]
- 共通再公開: なし
- 同一ファイル内の呼出: [{'function': 'build_phase162_web_validated_isomorphism_markdown', 'line': 259}]
- アプリケーション側の参照:
  - 検出なし
- テスト側の参照:
  - 検出なし

### `phase162_web_narrative_integration:_build_phase162_existing_group_connection`
- 判定: `RETAIN_INTERNAL_DEPENDENCY_REVIEW`
- 定義行: [166]
- 共通再公開: なし
- 同一ファイル内の呼出: [{'function': 'build_phase162_web_validated_isomorphism_markdown', 'line': 258}]
- アプリケーション側の参照:
  - 検出なし
- テスト側の参照:
  - 検出なし

### `phase162_web_narrative_integration:_format_phase162_proof_sentences`
- 判定: `RETAIN_TEST_CONTRACT_REVIEW`
- 定義行: [39]
- 共通再公開: なし
- 同一ファイル内の呼出: [{'function': '_build_phase162_legacy_validated_isomorphism_markdown', 'line': 161}]
- アプリケーション側の参照:
  - 検出なし
- テスト側の参照:
  - `tests/test_phase162_r5_6_narrative_final_format.py`: [{'line': 3, 'kind': 'import'}, {'line': 34, 'kind': 'call'}]

### `phase162_web_narrative_integration:_compose_phase162_group_conclusion`
- 判定: `RETAIN_TEST_CONTRACT_REVIEW`
- 定義行: [69]
- 共通再公開: なし
- 同一ファイル内の呼出: [{'function': '_build_phase162_legacy_validated_isomorphism_markdown', 'line': 162}]
- アプリケーション側の参照:
  - 検出なし
- テスト側の参照:
  - `tests/test_phase162_r5_6_narrative_final_format.py`: [{'line': 3, 'kind': 'import'}, {'line': 50, 'kind': 'call'}, {'line': 55, 'kind': 'call'}]

### `phase162_web_narrative_integration:_phase162_ehp_leaves`
- 判定: `RETAIN_SHARED_REEXPORT`
- 定義行: []
- 共通再公開: [{'module': 'phase162_ehp_leaf_inputs', 'line': 248}]
- 同一ファイル内の呼出: [{'function': '_build_phase162_existing_group_connection', 'line': 221}]
- アプリケーション側の参照:
  - 検出なし
- テスト側の参照:
  - 検出なし

### `phase162_r3_narrative_connection:render_phase162_r3_narrative`
- 判定: `RETAIN_APPLICATION_DEPENDENCY`
- 定義行: [166]
- 共通再公開: なし
- 同一ファイル内の呼出: [{'function': 'render_phase162_r3_with_public_references', 'line': 290}]
- アプリケーション側の参照:
  - `phase162_web_narrative_integration.py`: [{'line': 29, 'kind': 'import'}, {'line': 260, 'kind': 'call'}]
- テスト側の参照:
  - `tests/test_phase162_r3_narrative_connection.py`: [{'line': 6, 'kind': 'import'}, {'line': 41, 'kind': 'call'}, {'line': 52, 'kind': 'call'}, {'line': 62, 'kind': 'call'}, {'line': 73, 'kind': 'call'}, {'line': 81, 'kind': 'call'}]

### `phase162_r3_narrative_connection:render_phase162_r3_with_public_references`
- 判定: `RETAIN_TEST_CONTRACT_REVIEW`
- 定義行: [278]
- 共通再公開: なし
- 同一ファイル内の呼出: 検出なし
- アプリケーション側の参照:
  - 検出なし
- テスト側の参照:
  - `tests/test_phase162_r3_narrative_connection.py`: [{'line': 85, 'kind': 'import'}, {'line': 100, 'kind': 'call'}]

### `phase162_r3_narrative_connection:_phase162_legacy_ehp_body`
- 判定: `RETAIN_INTERNAL_DEPENDENCY_REVIEW`
- 定義行: [123]
- 共通再公開: なし
- 同一ファイル内の呼出: [{'function': 'render_phase162_r3_narrative', 'line': 231}]
- アプリケーション側の参照:
  - 検出なし
- テスト側の参照:
  - 検出なし

## 判断の境界

本監査は関数単位の静的な依存関係を分類するもので、旧関数の削除は実施しません。

旧 Phase 162 の fixture 不整合6件は引き続き未解決です。

全体 pytest は実施していません。
