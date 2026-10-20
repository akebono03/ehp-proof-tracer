# Phase 166 R3-C Stage 2 Test Correction

This package fixes two incorrectly labeled test cases. The target reference is at position 78: sources at 76 or 77 precede it and must be allowed. Sources at 78, 79, or unknown do not strictly precede it.

Run from the EHP Proof Tracer repository root after extracting the ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File '.\phase166_r3c_stage2_test_fix\run.ps1'
```

The script backs up and edits only `phase166_r3c_stage2/test_stage2.py`, then runs the existing focused tests. No production Python file or database is modified, and full pytest is not run.
