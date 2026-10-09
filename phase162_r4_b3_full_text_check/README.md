# Phase 162 R4-B3 Full-Text Inspection

This read-only inspection creates actual Markdown outputs from the **derived** proof trees and the **common baseline** narrative renderer for pi_5^4 and pi_6^5. It does not invoke the public stable-specific renderer or render a previously saved answer.

Run from the project root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase162_r4_b3_full_text_check.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r4_b3_full_text_check\run_phase162_r4_b3_full_text_check.ps1"
```

Outputs under `phase162_r4_b3_full_text_check/audit_output`:
- `pi_5^4_derived_common.md`
- `pi_6^5_derived_common.md`
- `check.json`

All files are outputs of the current repository runtime. The script changes no production code. The current phase boundary excludes publication-switch work and full-suite tests.
