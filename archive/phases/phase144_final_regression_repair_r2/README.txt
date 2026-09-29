Phase 144 Final Regression Repair R2

変更対象:
- main.py / _run_group_proof_command()
- tests/test_phase133_10_sigma_label_wording.py
- tests/test_phase143_47_multi_argument_shared_contribution_dedup.py
- tests/test_phase143_50_generic_statement_prose_renderer.py
- tests/test_phase143_58a_negative_scalar_sum.py
- tests/test_phase143_59b_group_structure_duplicate_suppression.py
- tests/test_phase143_61b_direct_premise_narrative.py

Production repair:
明示 depth=0 の Narrative が complete replay に置換されていたため、
depth=0 の場合だけ bounded replay を保持する。
正の明示 depth は Phase144 の complete-replay 経路を維持する。

Test maintenance:
Phase143 の旧 intermediate-evidence 表示期待を、Phase144-6 で確定した
ownership/frontier 境界と矛盾しない semantic/final-result regression に更新する。

Phase145 の default Narrative/depth=2 は先取りしない。
全体 pytest は実行しない。
