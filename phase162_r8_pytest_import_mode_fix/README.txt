Phase 162 R8: test module resolution repair

Only the PowerShell runner is changed. No production Python code or test assertions are changed.

Cause: default pytest import mode prepends the test directory to sys.path. This directory also contains phase162_pi5_3_web_replay.py, so it shadows the root production module.

Fix: invoke pytest with --import-mode=importlib so the test directory is not prepended.

Run from repository root in Windows PowerShell:

Expand-Archive -Path "$HOME\Downloads\phase162_r8_pytest_import_mode_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r8_pytest_import_mode_fix\run.ps1"

Only the four focused R8 tests are run; no full test suite.
