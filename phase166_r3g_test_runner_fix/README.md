# Phase 166 R3-G targeted-test runner correction

This package corrects the original test-runner invocation after retired Phase 49 test paths caused pytest collection to stop.

Run from the repository root, after the original R3-G package was extracted and installed:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3g_test_runner_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3g_test_runner_fix\run.ps1"
```

The runner never invokes `install.py` and never writes production Python files. It runs only the remaining existing R3-G, registry, Toda (4.5), and shared-proof regression tests. The entire test suite is not run.
