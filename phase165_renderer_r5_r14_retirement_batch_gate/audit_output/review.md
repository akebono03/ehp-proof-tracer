# Phase 165 R5-R14 一括撤去準備監査

判定: **REVIEW_REQUIRED**

## 前提条件

- shared_leaf_module: PASS
- replay_uses_shared_module: PASS
- web_reexports_leaf: PASS
- public_web_entry_present: PASS
- no_parse_errors: PASS

## 関数別の撤去ゲート

### `phase162_web_narrative_integration:_format_phase162_proof_sentences`
- 定義: `DEFINED`
- 判定: `KEEP_TEST_API_PENDING_MIGRATION`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_web_narrative_integration.py:161`
- テスト直接呼出: 1
  - `tests/test_phase162_r5_6_narrative_final_format.py:34`
- 監査直接呼出: 0

### `phase162_web_narrative_integration:_compose_phase162_group_conclusion`
- 定義: `DEFINED`
- 判定: `KEEP_TEST_API_PENDING_MIGRATION`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_web_narrative_integration.py:162`
- テスト直接呼出: 2
  - `tests/test_phase162_r5_6_narrative_final_format.py:50`
  - `tests/test_phase162_r5_6_narrative_final_format.py:55`
- 監査直接呼出: 0

### `phase162_web_narrative_integration:_build_phase162_legacy_validated_isomorphism_markdown`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_web_narrative_integration.py:259`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_web_narrative_integration:_build_phase162_existing_group_connection`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_web_narrative_integration.py:258`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_web_narrative_integration:build_phase162_web_validated_isomorphism_markdown`
- 定義: `DEFINED`
- 判定: `KEEP_TEST_API_PENDING_MIGRATION`
- 本番直接呼出: 0
- 内部直接呼出: 0
- テスト直接呼出: 4
  - `tests/test_phase162_r5_6_narrative_final_format.py:11`
  - `tests/test_phase162_r5_web_integration.py:12`
  - `tests/test_phase162_r5_web_integration.py:46`
  - `tests/test_phase162_r5_web_integration.py:55`
- 監査直接呼出: 0

### `phase162_web_narrative_integration:_phase162_ehp_leaves`
- 定義: `REEXPORTED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_web_narrative_integration.py:221`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:_element_latex`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 6
  - `phase162_r3_narrative_connection.py:217`
  - `phase162_r3_narrative_connection.py:218`
  - `phase162_r3_narrative_connection.py:39`
  - `phase162_r3_narrative_connection.py:40`
  - `phase162_r3_narrative_connection.py:79`
  - `phase162_r3_narrative_connection.py:58`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:_group_latex`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 3
  - `phase162_r3_narrative_connection.py:213`
  - `phase162_r3_narrative_connection.py:214`
  - `phase162_r3_narrative_connection.py:77`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:_structure_latex`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 2
  - `phase162_r3_narrative_connection.py:215`
  - `phase162_r3_narrative_connection.py:216`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:_ordered_ancestry`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_r3_narrative_connection.py:190`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:_reference_section`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_r3_narrative_connection.py:219`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:_phase162_legacy_ehp_body`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_r3_narrative_connection.py:231`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:_phase162_web_display_math_delimiters`
- 定義: `DEFINED`
- 判定: `KEEP_INTERNAL_PENDING_REMOVAL`
- 本番直接呼出: 0
- 内部直接呼出: 1
  - `phase162_r3_narrative_connection.py:269`
- テスト直接呼出: 0
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:render_phase162_r3_narrative`
- 定義: `DEFINED`
- 判定: `KEEP_APPLICATION_CALLER`
- 本番直接呼出: 1
  - `phase162_web_narrative_integration.py:260`
- 内部直接呼出: 1
  - `phase162_r3_narrative_connection.py:290`
- テスト直接呼出: 5
  - `tests/test_phase162_r3_narrative_connection.py:41`
  - `tests/test_phase162_r3_narrative_connection.py:52`
  - `tests/test_phase162_r3_narrative_connection.py:62`
  - `tests/test_phase162_r3_narrative_connection.py:73`
  - `tests/test_phase162_r3_narrative_connection.py:81`
- 監査直接呼出: 0

### `phase162_r3_narrative_connection:render_phase162_r3_with_public_references`
- 定義: `DEFINED`
- 判定: `KEEP_TEST_API_PENDING_MIGRATION`
- 本番直接呼出: 0
- 内部直接呼出: 0
- テスト直接呼出: 1
  - `tests/test_phase162_r3_narrative_connection.py:100`
- 監査直接呼出: 0

### `toda_group_proof_narrative_proof_chain_renderer:render_toda_group_proof_narrative_from_proof_chains_markdown`
- 定義: `DEFINED`
- 判定: `KEEP_TEST_API_PENDING_MIGRATION`
- 本番直接呼出: 0
- 内部直接呼出: 0
- テスト直接呼出: 5
  - `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:41`
  - `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:116`
  - `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:145`
  - `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:177`
  - `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py:201`
- 監査直接呼出: 4
  - `audit_phase144_6_r5_20.py:397`
  - `audit_phase144_6_r5_21.py:171`
  - `audit_phase144_6_r5_23.py:148`
  - `audit_phase144_6_r5_24.py:190`

### `toda_group_proof_narrative_concrete_transport:render_concrete_transport_proof_from_steps`
- 定義: `DEFINED`
- 判定: `KEEP_TEST_API_PENDING_MIGRATION`
- 本番直接呼出: 0
- 内部直接呼出: 0
- テスト直接呼出: 2
  - `tests/test_phase162_r4_b3_common_renderer_fix.py:27`
  - `tests/test_phase162_r4_b3_common_renderer_fix.py:37`
- 監査直接呼出: 0

## R5-R15 に向けた条件

- アプリケーションの呼出元を先に共通モジュールへ移すか、保存する互換 API を明示する。
- 旧 Narrative の出力関数は、テスト・外部 API 契約を確認するまで無条件には削除しない。
- 旧 Phase 162 fixture の6件の失敗は別途記録し、成功扱いにしない。
- Group Proof の完成・未完成 Narrative の一致を R5-R15 の限定回帰テストで保持する。
