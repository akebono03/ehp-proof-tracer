Phase 165 R6 - completion contract expectation fix
Target: test_phase165_r52_r2_search_adapter.py
Function: test_r52_r2_canonical_success_is_complete_only_for_target
Change: replace obsolete expectation of QED for SyntheticStatement with assertion that the public narrative rejects an unsupported group structure.
Only this test function is edited. Imports stay unchanged. Mathematical search and renderer code are untouched. Backup is made first.
Run from repository root:
  powershell -ExecutionPolicy Bypass -File .\phase165_r6_mock_completion_contract_fix\run.ps1
Runs only test_phase165_r52_r2_search_adapter.py, not full pytest.
Completion condition: all targeted tests pass. This is not Phase 165 closure.
