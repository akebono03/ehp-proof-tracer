Phase157-R5-R5 — 112-group cross-audit re-audit

目的:
R5-R4 の generic Literature Statement Boundary filter を接続した後、
112群の Reference selection を再監査する。

範囲:
- n=2..15
- k=0..7
- 112 groups
- proof replay depth=2
- semantic closure
- full Narrative rendering は行わない

実行経路:
1. build_standard_toda_report
2. build_toda_group_result_proof_replay(max_depth=2)
3. build_toda_group_proof_presentation
4. build_toda_group_proof_narrative_semantic_closure_presentation
5. build_toda_group_proof_narrative_reference_entries
6. filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary
7. select_toda_group_proof_narrative_reference_statement_steps
8. structured boundary classification

監査分類:
- FIXED_STATEMENT
- PROOF_INTERNAL
- UNTRACKED
- FIXED_STATEMENT_INELIGIBLE
- FIXED_STATEMENT_WITHOUT_COMPONENT
- FIXED_STATEMENT_MISSING_COMPONENT

R5-R1 baseline:
- selected Reference steps: 234
- FIXED_STATEMENT: 34
- PROOF_INTERNAL: 46
- UNTRACKED: 128
- FIXED_STATEMENT_INELIGIBLE: 2
- FIXED_STATEMENT_WITHOUT_COMPONENT: 24
- FIXED_STATEMENT_MISSING_COMPONENT: 0
- confirmed defects: 72

完了条件:
- groups = 112
- exceptions = 0
- confirmed defects = 0
- UNTRACKED selected steps = 0

production code:
- 変更なし

existing tests:
- 変更なし

pytest:
- 実行しない

出力:
phase157_r5_r5_audit_output/
- phase157_r5_r5_summary.txt
- phase157_r5_r5_result.json
- phase157_r5_r5_selected_steps.csv
- phase157_r5_r5_confirmed_defects.csv
- phase157_r5_r5_group_inventory.csv
- phase157_r5_r5_locator_summary.csv
- phase157_r5_r5_exceptions.csv

注意:
audit が完了条件を満たさない場合、exit code 1 で終了する。
これは production error と断定するものではなく、R5-R5 の追加確認が必要という意味。
全体 pytest は Phase157 closure まで実行しない。
