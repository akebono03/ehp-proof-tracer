# Phase 165 Renderer R5-R3: two remaining test imports

This is a targeted test-only compatibility import migration. Run `run.ps1` from Windows PowerShell after extracting the ZIP in the project root. No production module or mathematical rule is modified. It migrates exactly two imports in `tests/test_phase162_r2_validated_proof_presentation.py`, checks targeted pytest, and reruns the previously installed R5-R2 static audit. Use `restore.ps1` if needed. No full pytest is executed.
