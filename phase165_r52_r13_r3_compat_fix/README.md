# Phase 165 R52-R13-R3 compatibility repair

This patch restores the four-field legacy Proposition 5.1 composite schema while preserving explicit component declarations for future composite references.

From the repository root, extract the ZIP and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase165_r52_r13_r3_compat_fix\run.ps1
```

The guarded installer changes only `phase165_typed_component_lookup.py` and adds `test_phase165_r52_r13_r3_compat_fix.py`. It fails without modifying code if the expected R2 implementation is missing. The original file is backed up. The existing R12 tests and R2 tests are rerun. Full pytest is not run.

Completion requires the targeted tests to pass. Conditional specialization of the symbolic `n >= 3` statement remains outside this patch.
