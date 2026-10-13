Phase 165 R52-R8 test fixture correction

Changed file: test_phase165_r52_r8_show_proof_route.py
Changed function: test_r8_registered_proof_does_not_fall_back
Change: supply required nonempty diagnostics for SEARCH_FAILED fixture.

No production code, imports, other tests or Web UI changed.
Installer checks expected old version and retains backup.
Only targeted pytest is executed; not full pytest.

Installation:
Expand-Archive -Path "$HOME\Downloads\phase165_r52_r8_test_fixture_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r8_test_fixture_fix\run.ps1"
