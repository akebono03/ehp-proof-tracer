# Phase 165 Renderer R5-R4: Legacy Test Import Audit

Updates precisely two import statements in one Phase 162 test module. It leaves production renderer, search rules, and all fixture construction unchanged. The six historical Phase 162 tests failed upstream in `build_phase59_3_data()` due to an empty `prop51_steps` tuple. They are **not claimed as passing** by this package; the fixture issue is tracked separately from the R5 import migration. Runs scoped installer tests, current Phase 165 renderer tests, and the existing R5 static audit. No full-suite pytest.

The installer preserves the backup under `.phase165_renderer_r5_r3_test_backup` and reverts on scoped regression. To undo manually: `python .\phase165_renderer_r5_r4_fixture_isolation\install.py --restore`.
