# Phase 165 R13 — Stop false legacy proof success for pi_3^2

This focused guard prevents `build_phase164_r5_r2_common_replay(2,1,...)` from returning a legacy repository proof. It does **not** assert that a new typed-statement proof has been built.

Run the `run.ps1` script in this directory after extracting into the repository root. The script changes only the selector and an existing selector test. The targeted test in this package verifies that trace, outline and narrative modes fail closed for pi_3^2, without invoking the legacy selector. The full test suite is intentionally not executed.

The next step is to replace this temporary `ValueError` guard with a verified typed-statement backward-search result; do not reinstate the legacy fallback.
