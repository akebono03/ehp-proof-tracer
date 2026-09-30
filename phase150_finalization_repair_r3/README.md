# Phase 150 Finalization Repair R3

目的:
- R2 で更新した10テストファイルを正常な UTF-8 版で再配置する。
- R2 focused pytest で残った5 failure の historical Narrative contract を generic baseline contract に更新する。
- production code は変更しない。
- Phase 151/152 で扱う raw fallback の改善を先取りしない。
- full regression は実行しない。

変更対象:
- tests/test_phase132_6_group_proof_narrative_renderer.py
- tests/test_phase132_7_group_proof_cli_modes.py
- tests/test_phase132_8_group_proof_narrative_dedup.py
- tests/test_phase132_9_web_group_proof_modes.py
- tests/test_phase133_10_sigma_label_wording.py
- tests/test_phase133_6_group_proof_narrative_labels.py
- tests/test_phase133_9_group_proof_narrative_labels.py
- tests/test_phase144_6_r3_production_references.py
- tests/test_phase144_6_r3_structured_references.py
- tests/test_phase144_6_r4_supporting_fact_filtering.py

完了条件:
- syntax preflight PASS
- focused pytest 60 passed
- production files unchanged
