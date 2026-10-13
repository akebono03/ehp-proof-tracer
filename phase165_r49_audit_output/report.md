# Phase 165 R49 構造監査

現行コードの定義・呼出し箇所を収集した読み取り専用監査です。実装修正、数学的検証、pytest は行っていません。

## toda_group_proof_narrative_reasons.py
存在: True

構文エラー: None
### 関連行
- 24: `TodaDeltaZeroStatement,`
- 30: `TodaDeltaInjectiveStatement,`
- 56: `EXACTNESS_TO_MAP_PROPERTY = (`
- 205: `class TodaGroupProofNarrativeReasonSidecar:`
- 304: `TodaDeltaInjectiveStatement,`
- 314: `TodaDeltaZeroStatement,`
- 350: `or type(conclusion).__name__ == "MapInjective"`
- 355: `or type(conclusion).__name__ == "MapSurjective"`
- 491: `.EXACTNESS_TO_MAP_PROPERTY`
- 956: `def build_toda_group_proof_narrative_reason_sidecar(`
- 959: `) -> TodaGroupProofNarrativeReasonSidecar:`
- 1098: `return TodaGroupProofNarrativeReasonSidecar(`

### 定義
- ClassDef TodaGroupProofNarrativeReasonKind: 50
- ClassDef TodaGroupProofNarrativeReason: 83
- ClassDef TodaGroupProofNarrativeReasonSidecar: 205
- FunctionDef _exactness_to_map_property_reason: 298
- FunctionDef _exactness_to_kernel_reason: 501
- FunctionDef _injective_image_order_reason: 593
- FunctionDef _multiple_relation_to_order_reason: 688
- FunctionDef _final_group_structure_reason: 752
- FunctionDef _aggregate_derivation_reason: 919
- FunctionDef _final_result_derivation_reason: 938
- FunctionDef build_toda_group_proof_narrative_reason_sidecar: 956

## toda_group_proof_narrative_reason_renderer.py
存在: True

構文エラー: None
### 関連行
- 15: `TodaGroupProofNarrativeReasonSidecar,`
- 68: `.EXACTNESS_TO_MAP_PROPERTY`
- 294: `reason_sidecar: TodaGroupProofNarrativeReasonSidecar,`
- 305: `reason_sidecar,`
- 306: `TodaGroupProofNarrativeReasonSidecar,`
- 309: `"reason_sidecar must be a "`
- 310: `"TodaGroupProofNarrativeReasonSidecar"`
- 483: `for reason in reason_sidecar.reasons:`
- 634: `for node in reason_sidecar.presentation.nodes:`
- 659: `for reason in reason_sidecar.reasons:`
- 743: `for reason in reason_sidecar.reasons:`
- 919: `for reason in reason_sidecar.reasons:`
- 923: `.EXACTNESS_TO_MAP_PROPERTY`
- 1037: `for node in reason_sidecar.presentation.nodes:`
- 1193: `reason_sidecar: TodaGroupProofNarrativeReasonSidecar,`
- 1204: `for edge in reason_sidecar.presentation.edges:`
- 1256: `.EXACTNESS_TO_MAP_PROPERTY`
- 1619: `reason_sidecar: TodaGroupProofNarrativeReasonSidecar,`
- 1624: `reason_sidecar,`
- 1625: `TodaGroupProofNarrativeReasonSidecar,`
- 1628: `"reason_sidecar must be a "`
- 1629: `"TodaGroupProofNarrativeReasonSidecar"`
- 1635: `for reason in reason_sidecar.reasons:`
- 1658: `reason_sidecar,`
- 1677: `for reason in reason_sidecar.reasons:`
- 1685: `for reason in reason_sidecar.reasons:`

### 定義
- FunctionDef render_toda_group_proof_narrative_reason_sentence: 23
- FunctionDef order_toda_group_proof_narrative_injective_image_order_reason: 292
- FunctionDef _toda_group_proof_narrative_reason_insertion_index: 1190
- FunctionDef _normalize_exactness_to_map_property_reason_prose: 1249
- FunctionDef _normalize_exactness_to_kernel_reason_prose: 1509
- FunctionDef insert_toda_group_proof_narrative_reason_prose: 1617

## web_group_proof.py
存在: True

構文エラー: None
### 関連行

### 定義
- ClassDef WebGroupProofStepView: 38
- ClassDef WebGroupProofInlineSegmentView: 135
- ClassDef WebGroupProofRenderedLineView: 168
- ClassDef WebGroupProofView: 257
- FunctionDef _group_proof_rule_name: 431
- FunctionDef _group_proof_statement_latex: 440
- FunctionDef _split_group_proof_rendered_line: 487
- FunctionDef _build_group_proof_inline_segments: 531
- FunctionDef _build_group_proof_rendered_lines: 619
- FunctionDef build_standard_web_group_proof_view: 692

## phase165_goal_only_search.py
存在: True

構文エラー: None
### 関連行

### 定義
- ClassDef GoalSearchIncompleteError: 14
- FunctionDef construct_registered_group_proof: 18

## 関連テスト候補
- `tests\test_phase150_rc4_4_reasons.py`
- `tests\test_phase150_rc4_5_visible_reasons.py`
- `tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests\test_phase150_rc4_5f_2_final_group_structure_reason.py`
- `tests\test_phase150_rc4_7d_generic_reason_vocabulary.py`
- `tests\test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`
- `tests\test_phase150_rc4_closure_reason_visibility.py`
- `tests\test_phase156_r6_3_reason_prose_canonicalization.py`
- `tests\test_phase157_r11_reference_reason_punctuation.py`
- `tests\test_phase157_r20_repair47_injective_image_order_reason.py`
- `tests\test_phase157_r20_repair48_injective_image_reason_ordering.py`
- `tests\test_phase159_pi3_2_exactness_reason_locality.py`
- `tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py`
- `tests\test_phase159_pi4_3_exactness_reason_unification.py`
- `tests\test_phase159_pi6_3_zero_map_reason_order.py`
- `tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
- `tests\test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py`
- `tests\test_phase162_r3c_root_reason.py`
- `tests\test_phase162_r3d_root_reason_audit.py`
- `tests\test_phase162_r3g_existing_reason_bridge.py`
- `tests\test_phase162_r3h_reason_inventory.py`
