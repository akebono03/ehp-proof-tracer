# Phase 163 R4-R44: TeX-to-Assertion Crosswalk Audit

This is a **read-only**, source-preserving audit. It links the 108 R4-R43 TeX environment rows to existing literature references and enumerates all existing assertions under those references. It **does not** claim that a named assertion corresponds to a verified subspan of the TeX body.

## Run

From the repository root in PowerShell, after extracting this ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r44_assertion_audit\run.ps1"
```

Dependencies from previous phases:
- `phase163_r4_r42_output/extraction.json`
- `phase163_r4_r43_output/mapping.json`
- `phase163_r4_r42_tex_extract/inputs/` (five original, unchanged TeX files)
- The current repository's `phase163_r4_registry_bridge.py` and its imports.

The script checks all five file fingerprints, mapping and extraction consistency, reference coverage and assertion-ID coverage. It runs only R4-R44 focused pytest tests. It does not run the full suite.

Output in `phase163_r4_r44_output/`:
- `crosswalk.json`: all whole-environment source texts plus per-assertion crosswalk
- `assertions.csv`: one row per existing Assertion ID; semantic review remains required
- `reference_units.csv`: one row per extracted TeX environment
- `report.md`: counts and next-step boundaries

An existing component position is preserved when present, but is **not** interpreted as a position derived from TeX. Missing component positions are not invented. New reference candidates and symbolic/unnumbered environments do not receive IDs. No `TEX_REGISTERED`, `STRUCTURED`, or `SOURCE_VERIFIED` status is asserted. Neither original sources nor existing code are modified.
