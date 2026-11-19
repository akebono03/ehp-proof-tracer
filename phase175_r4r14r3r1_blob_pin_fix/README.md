# R4R14R3R1 Git Blob Pin Correction

This package corrects one malformed 42-character SHA in the read-only R4R14R3 audit. The reviewed Git blob for `phase174_r3_r7_r7_composite_zero_audit/rule.py` is `d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6` (40 characters). The previous value had two extra trailing characters. No production source, mathematical rule, GIVEN, or existing test is changed.

Run from the repository root after extraction:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r14r3r1_blob_pin_fix\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r14r3r1_blob_pin_fix\run.ps1
```

The wrapper installs only the corrected read-only audit script into the existing `phase175_r4r14r3_binary_composition_audit` directory and then delegates to the established `run.ps1`. Use the original R4R14R3 ZIP first. Whole-suite pytest is not run.
