Phase 165 R6: archive ONLY two historical Phase144 renderer tests that import removed tests.test_phase143_19_method_evidence.
Run from repo root using run.ps1 after Expand-Archive. Script verifies prerequisites, backs up originals byte-for-byte in phase165_r6_audit_results/retired_phase144_tests/<UTC timestamp>/, then removes these TWO files from tests/.
Does NOT touch production code, change pytest config, rerun tests, or imply any lost mathematical coverage is restored. To restore, copy both saved .py files back to tests/.
