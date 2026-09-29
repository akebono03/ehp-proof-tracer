Phase 145 Final Regression Diagnosis R5

目的
----
Phase 145 Final Regression Repair R4 後も残った 43 collection errors の
直接原因となっている3つの canonical test dependency の所在を確定する。

対象
----
- tests/test_phase143_19_method_evidence.py
- tests/test_phase75_515_pi15_8_final_group.py
- tests/test_phase144_6_r5_18_production_generic_proof_chain_foundation.py

確認内容
--------
- 現在の worktree に物理ファイルが存在するか
- git index ではどこにあるか
- HEAD ではどこにあるか
- Git history にどの path 名で存在したか
- archive/phases 配下に実体があるか
- canonical tests/ path に存在するか
- 現在の tests がどこから import しているか
- tests/archive の git status

変更
----
なし。

この診断では production code、tests、archive のいずれも変更しない。
repository-wide pytest も実行しない。
