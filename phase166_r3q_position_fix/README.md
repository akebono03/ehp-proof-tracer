# Phase 166 R3-Q — Component Position Correction

This package attaches existing, reviewed Proposition 5.1 positions to the matching component assertions created by the shared typed bridge. It does not change proof search, source links, reference IDs, or the renderer. It does not invent positions for unresolved sources.

Run from the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3q_position_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3q_position_fix\run.ps1"
```

The installer backs up `phase166_r3p_position_binding.py` before replacing it. A failing targeted test run restores that backup. It does not run the full test suite.

The package cannot by itself guarantee that ordinary Web proof search is now publication-order-only. References with missing position metadata remain a separate issue.
