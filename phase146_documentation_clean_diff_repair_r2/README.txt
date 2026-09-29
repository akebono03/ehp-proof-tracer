Phase 146 Documentation Clean-Diff Repair R2

Purpose
-------
Repair only the verification harness from R1.

R1 already succeeded in restoring:
- docs/design.md
- docs/development_log.md
- docs/roadmap.md
- docs/proof_records.md

to canonical HEAD. Its output reached:
  Documentation clean diff: PASS

The later failure was caused by the Japanese marker embedded in the
PowerShell script being decoded incorrectly. The displayed mojibake marker
was not evidence of corrupted documentation.

R2 changes no repository documentation, production code, or test code.
It verifies the Japanese and ASCII markers in Python using explicit UTF-8
strict decoding.

Run
---
powershell -ExecutionPolicy Bypass `
  -File ".\phase146_documentation_clean_diff_repair_r2\run_phase146_documentation_clean_diff_repair_r2.ps1"

Expected
--------
- Documentation clean diff: PASS
- UTF-8 strict decode PASS for all four documents
- Phase 146 documentation markers: PASS
- Documentation unchanged by R2: PASS

No pytest is run because R2 is verification-only.
