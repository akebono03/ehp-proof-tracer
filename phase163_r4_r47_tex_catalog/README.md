# Phase 163 R4-R47 — Standalone Toda TeX Source Catalog

This package registers the 108 **previously extracted TeX environments** from Toda chapters 1–5 into an independent JSON catalog. It does not alter the production `UnifiedStatementRegistry`, existing assertion IDs, or proof search.

## Inputs

Run from the existing `ehp_proof` project root, with R4-R42 through R4-R44 already completed. Required inputs are:

- `phase163_r4_r42_output/extraction.json`
- `phase163_r4_r43_output/mapping.json`
- `phase163_r4_r44_output/crosswalk.json`
- `phase163_r4_r42_tex_extract/inputs/` containing the five original TeX files.

The runner checks the current GitHub-derived registry bridge at runtime and verifies SHA-256 hashes of the original TeX files. Existing Reference and Assertion IDs are read, not rewritten.

## Execution

```powershell
powershell -ExecutionPolicy Bypass -File .\phase163_r4_r47_tex_catalog\run.ps1
```

Focused tests only:

```powershell
$env:PYTHONPATH = ".\phase163_r4_r47_tex_catalog;."
python -m pytest -q .\phase163_r4_r47_tex_catalog\tests\test_phase163_r4_r47_tex_catalog.py
```

The runner writes `phase163_r4_r47_output/catalog.json`, `catalog.csv`, and `report.md`. The JSON contains exact R4-R42 extracted environment text, chapter order, reference links (where matched), and distinct `TEX_REGISTERED`, `STRUCTURED`, and `SOURCE_VERIFIED` statuses.

## Safeguards and limitations

- Existing Reference IDs are preserved; 66 **proposed** Reference IDs are not added to production.
- Nineteen environments without a resolved literary locator receive source-unit IDs, **not invented Toda numbers**.
- Source-unit IDs use chapter and ordinal. Re-execution with changed source, ordering, or registry snapshots is rejected; future insertion or correction needs explicit migration.
- `TEX_REGISTERED` means this independent source catalog contains the TeX environment. It does **not** mean that the production Statement Registry or proof search can use it.
- `STRUCTURED=false` and `SOURCE_VERIFIED=false` refer to this catalog's source units, not the pre-existing structured theorem facts or prior page-specific manual verification.
- This is **not** complete chapter-wide prose extraction: definitions or statements outside R4-R42 extracted environments, including parallel-column text and unnumbered standalone descriptions, remain future work. R4-R42 comment-stripped environment text is retained; TeX source files themselves are unchanged.
- No full pytest suite is executed. Run it only at the end of Phase 163.
