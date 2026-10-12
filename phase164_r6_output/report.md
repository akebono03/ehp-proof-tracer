# Phase 164 R6 全経路監査（読み取り専用）

この報告は静的な候補の棚卸しであり、削除安全性・数学的意味・実行経路の証明ではありません。

## 概況
- Production Python modules: 333
- Test files: 1925
- Parse errors: 0

## GitHub とローカル（Git blob SHA による照合）
- `proof.py`: 一致
- `web_group_proof.py`: 一致
- `web_generator_proof.py`: 一致
- `web_operation_query_proof.py`: 一致
- `toda_group_proof_narrative_renderer.py`: 一致
- `phase162_web_narrative_integration.py`: 一致

## 9分野の候補ファイル数
- 01_statement_registry: 137
- 02_proofstep: 31
- 03_proof_engine: 37
- 04_replay: 12
- 05_presentation: 31
- 06_renderer: 71
- 07_references: 43
- 08_web: 20
- 09_legacy_phase: 124

## 入口と関連テスト（ファイル内の名称出現で抽出）
- web_group_proof.py: 30候補 / phase148_rc2_4_repair_r3_web_unit_rendering_path_parity_audit/test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py, phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py, phase148_rc2_4_repair_r4_web_narrative_depth_parity/test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py, phase150_finalization_repair_r1/local_snapshot/tests/test_phase132_9_web_group_proof_modes.py, phase150_finalization_repair_r2/backup_before_r2/tests/test_phase132_9_web_group_proof_modes.py, phase150_finalization_repair_r2/reference_updated_tests/test_phase132_9_web_group_proof_modes.py, phase150_finalization_repair_r3/backup_before_r3/test_phase132_9_web_group_proof_modes.py, phase150_finalization_repair_r3/reference_updated_tests/test_phase132_9_web_group_proof_modes.py, phase150_rc4_7d_3_public_narrative_generic_route_integration_r1/test_phase150_rc4_7d_3_public_narrative_generic_route.py, phase150_rc4_7d_3_public_narrative_generic_route_integration_r1_repack/test_phase150_rc4_7d_3_public_narrative_generic_route.py, phase155_r4_2_canonical_boundary_validation/test_audit_phase155_r4_2.py, phase156_r6_canonical_connector_local_ordering/backup_before_apply/tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py
- web_generator_proof.py: 2候補 / tests/test_phase120_2_web_generator_proof.py, tests/test_phase122_4_web_generator_proof_scope.py
- web_operation_query_proof.py: 2候補 / tests/test_phase118_4_depth_browser_usability.py, tests/test_phase118_web_operation_query_proof.py
- web_app.py: 23候補 / phase148_rc2_4_repair_r4_web_narrative_depth_parity/test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py, phase150_finalization_repair_r1/local_snapshot/tests/test_phase132_9_web_group_proof_modes.py, phase150_finalization_repair_r2/backup_before_r2/tests/test_phase132_9_web_group_proof_modes.py, phase150_finalization_repair_r2/reference_updated_tests/test_phase132_9_web_group_proof_modes.py, phase150_finalization_repair_r3/backup_before_r3/test_phase132_9_web_group_proof_modes.py, phase150_finalization_repair_r3/reference_updated_tests/test_phase132_9_web_group_proof_modes.py, phase162_r4_b3_web_common_display/files/tests/test_phase162_r4_b3_web_common_display.py, tests/test_phase117_web_app.py, tests/test_phase118_4_depth_browser_usability.py, tests/test_phase118_web_app.py, tests/test_phase120_2_web_app_generator_proof.py, tests/test_phase123_4_web_generator_applicability.py

## 次段階への判定
- 削除許可: **なし**（依存・実行・テストを追加確認するまで保留）
- 全体 pytest: **未実行**
- 変更した既存プロジェクトコード: **なし**
- 詳細: `audit.json` の definitions / calls / imports / test_files / github_baseline_comparison を参照
