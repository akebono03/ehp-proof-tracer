# Phase 165 Renderer R1 監査結果

## 件数

- 本番コード: 428 Python files
- Renderer/Narrative 名称ファイル: 63
- トップレベル重複関数定義: 8
- 旧 Generic モジュールからの import: 40
- AST 解析失敗: 0

## 必須ファイルの存在

- YES: `web_group_proof.py`
- YES: `phase165_r52_r3_web_adapter.py`
- YES: `phase165_r52_partial_proof.py`
- YES: `phase165_r56_presentation_adapter.py`
- YES: `toda_group_proof_narrative_renderer.py`
- YES: `toda_group_proof_narrative_shared_components.py`
- NO: `toda_group_proof_generic_narrative_renderer.py`
- YES: `toda_group_proof_generic_narrative_renderer/__init__.py`
- YES: `toda_group_proof_outline_renderer.py`
- YES: `toda_group_proof_presentation.py`

## 重複関数定義

- `phase165_r55_nk_only_goal.py`: `registered_group_goal_candidates` lines [16, 85]
- `standard_production_applicability_catalog.py`: `build_standard_production_applicability_catalog` lines [742, 993, 1070, 1133, 1211, 1309, 1386, 1468, 1547, 1626, 1705, 1784, 1863, 1942, 2021, 2100, 2179, 2258, 2338, 2418, 2499, 2577, 2655, 2733, 2811, 2889, 2967, 3045, 3124, 3201, 3278, 3355, 3444]
- `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`: `render_toda_group_proof_narrative_markdown` lines [11533, 11581, 12243]
- `toda_group_proof_narrative_renderer.py`: `render_toda_group_proof_narrative_markdown` lines [11104, 11766]
- `toda_rules.py`: `toda_prop511_pi12_6_suspension_injective_inference_rule` lines [26043, 26382]
- `toda_rules.py`: `toda_514_delta_nu11_zero_inference_rule` lines [43454, 43946]
- `toda_rules.py`: `toda_514_first_short_exact_inference_rule` lines [43711, 44463]
- `toda_rules.py`: `toda_lemma510_corrected_exactness_core_inference_rule` lines [53184, 53339]

## 公開入口の定義

- `build_partial_web_group_proof_view`: `phase165_r52_r3_web_adapter.py:19`
- `build_standard_web_group_proof_view`: `web_group_proof.py:44`
- `render_completed_shared_narrative`: `phase165_r56_presentation_adapter.py:18`
- `render_partial_proof_markdown`: `phase165_r52_partial_proof.py:90`
- `render_toda_group_proof_generic_narrative_markdown`: 定義なし
- `render_toda_group_proof_narrative_markdown`: `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py:11533`, `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py:11581`, `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py:12243`, `toda_group_proof_narrative_renderer.py:11104`, `toda_group_proof_narrative_renderer.py:11766`
- `render_toda_partial_proof_narrative_markdown`: `toda_group_proof_narrative_renderer.py:11800`

## 旧 Generic モジュールへの依存

- `audit_phase144_6_r5_21.py:11` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_24.py:12` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_25.py:12` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_27.py:12` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_33.py:19` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_36.py:19` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_37.py:16` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_38.py:19` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_1.py:6` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_11.py:7` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_11a.py:8` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_11d.py:8` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_3.py:4` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_5.py:6` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_6.py:8` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_8.py:7` names=['_render_generic_narrative_step']
- `audit_phase144_6_r5_43_9.py:6` names=['_render_generic_narrative_step']
- `audit_phase162_r3b_existing_renderer.py:19` names=['_render_generic_narrative_step']
- `phase162_r3f_recursive_renderer.py:11` names=['_render_generic_narrative_step']
- `phase162_validated_proof_presentation.py:27` names=['_render_generic_narrative_step']
- `phase165_r14_r43_reference_reason.phase165_r44_removed.py:8` names=['_render_generic_narrative_step']
- `phase165_r57_r10_step_narrative.py:10` names=['_render_generic_narrative_step']
- `phase165_r57_r2_partial_narrative.py:12` names=['_render_generic_narrative_step']
- `test_phase165_r52_r11_common_renderer.py:9` names=['render_toda_partial_proof_narrative_markdown']
- `tests/test_phase143_49_dependency_label_narrative_policy.py:3` names=['_render_generic_narrative_proof_block']
- `tests/test_phase148_rc2_4_repair_r1_exposure_path_audit.py:4` names=['_render_generic_narrative_step']
- `tests/test_phase148_rc2_4_repair_r2.py:4` names=['_render_generic_narrative_step']
- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py:6` names=['_generic_short_exact_sequence_reason_prose']
- `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py:4` names=['_render_generic_narrative_step']
- `tests/test_phase157_r20_repair40_none_component_latex_fallback.py:7` names=['_render_phase153_r3_6_component_latex', '_render_phase153_r3_6_component_list_prose']
- `tests/test_phase159_pi4_3_exactness_reason_unification.py:6` names=['_render_generic_narrative_step']
- `tests/test_phase159_pi4_3_trailing_premise_order.py:4` names=['_render_generic_narrative_step']
- `toda_group_proof_narrative_argument_body_renderer.py:1` names=['_generic_narrative_dependency_labels', '_generic_narrative_sentence_lead', '_generic_short_exact_sequence_reason_prose', '_render_generic_narrative_proof_block', '_render_generic_narrative_step']
- `toda_group_proof_narrative_contribution_ordering.py:6` names=['_render_generic_narrative_step']
- `toda_group_proof_narrative_contribution_renderer.py:26` names=['_generic_short_exact_sequence_latex', '_generic_short_exact_sequence_reason_prose', '_render_generic_narrative_step']
- `toda_group_proof_narrative_equation_numbering.py:4` names=['_render_generic_narrative_step']
- `toda_group_proof_narrative_exactness_display_contributions.py:7` names=['_generic_short_exact_sequence_latex', '_render_generic_narrative_step']
- `toda_group_proof_narrative_reason_renderer.py:4` names=['_render_generic_narrative_expression_latex', '_render_generic_narrative_step']
- `toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py:37` names=['_render_generic_narrative_step', '_GENERIC_INJECTIVE_STATEMENT_TYPES', '_GENERIC_ISOMORPHISM_STATEMENT_TYPES', '_GENERIC_SURJECTIVE_STATEMENT_TYPES', '_render_generic_narrative_group_map_latex', '_generic_group_map_name', '_GENERIC_ZERO_MAP_STATEMENT_TYPES']
- `toda_group_proof_narrative_renderer.py:35` names=['_render_generic_narrative_step', '_GENERIC_INJECTIVE_STATEMENT_TYPES', '_GENERIC_ISOMORPHISM_STATEMENT_TYPES', '_GENERIC_SURJECTIVE_STATEMENT_TYPES', '_render_generic_narrative_group_map_latex', '_generic_group_map_name', '_GENERIC_ZERO_MAP_STATEMENT_TYPES']

## 判定上の注意

- AST calls/imports are static evidence only; monkeypatch, reflection and dynamic import can evade scanning.
- Root production sources are prioritized; historical phase packages and archived scripts are excluded.
- R1 never deletes, renames, or edits project source files.
- A single implementation cannot be declared solely from renderer filename counts.

## R2 以降の判断

この監査結果をもとに、完成・未完成の公開入口、内部依存、重複定義を整理する。R1 ではコードを変更しない。
