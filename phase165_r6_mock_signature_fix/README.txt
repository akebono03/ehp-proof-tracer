Phase 165 R6 focused test maintenance: mock signature only.

Modified file: test_phase165_r52_r2_search_adapter.py
Modified functions (only their parameter lists):
 - test_r52_r2_partial_preserves_proved_leaf / nested fake_reconstruct
 - test_r52_r2_no_steps_is_failed / nested fake_reconstruct
 - test_r52_r2_canonical_success_is_complete_only_for_target / nested fake_reconstruct

The installer validates exact old function signatures (three occurrences) and current
production call contract, preserves a timestamped backup, and runs only three targeted tests.
No production Python file or math rule is changed.
If local test file differs from the audited version the installer refuses to modify it.

PowerShell:
 cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
 Expand-Archive -Path "$HOME\Downloads\phase165_r6_mock_signature_fix.zip" -DestinationPath '.' -Force
 powershell -ExecutionPolicy Bypass -File '.\phase165_r6_mock_signature_fix\run.ps1'

Do not rerun the 4223-test full audit yet. Remaining failures are still outstanding.
