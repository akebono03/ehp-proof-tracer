# Phase157 R11-R11 change summary

変更対象:
- toda_group_proof_narrative_semantics.py
  - imports
  - build_toda_group_proof_narrative_semantic_closure_presentation()
- toda_group_proof_narrative_contribution_renderer.py
  - renderer-side Reference H-value insertion call を削除
- tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py
- tests/test_phase157_r11_reference_reason_punctuation.py
- tests/test_phase157_r5_r9_fixed_definition_body_suppression.py

完了条件:
- H(nu') = E^2 eta_3 と E^2 eta_3 = eta_5 が closure に入る。
- derived H(nu') = eta_5 が H-surjectivity より前に出る。
- (5.3) 利用は実際の Reference 番号 [R2] で表示。
- semantic closure に group/rule-name hard-code を入れない。
- full pytest はまだ実行しない。
