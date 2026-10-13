# Phase 165 R51 — R49 Common Reason Renderer Integration

This package migrates the existing R49 typed-reason ordering function **without modifying its body** into `toda_group_proof_narrative_reason_renderer.py`. It changes the contribution renderer's existing grouped import and the related R49 test import. Upon successful focused tests, it archives the redundant standalone helper; on test failure, it restores the pre-install sources.

## Files and functions

- `toda_group_proof_narrative_reason_renderer.py`: adds the whole existing `finalize_phase165_r49_typed_reason_order` function immediately before `insert_toda_group_proof_narrative_reason_prose`.
- `toda_group_proof_narrative_contribution_renderer.py`: changes only the import of that function; the rendering pipeline remains unchanged.
- `tests/test_phase165_r49_display_fix.py`: changes only the import of that function.
- `phase165_r49_display_order.py`: archived only if targeted tests pass.
- `test_phase165_r51_common_reason_integration.py`: adds one focused test.

`R49_FUNCTION_FULL.py` is generated during installation with the complete moved function for review. Backups are stored in `backup_before_apply/`. No full test suite is run.
