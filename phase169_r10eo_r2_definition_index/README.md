# Phase 169 R10EO-R2 — Generic Definition Index Audit

This read-only package builds a generator-independent index of literal Toda suspension definitions. It identifies candidates using the `latex`, `n`, and `k` fields of `data/HyoujiGen.csv` and the adopted TeX transcriptions in `sources/toda/`.

**No new `GIVEN`, proof step, inference rule, or production source change is made.** This index is a textual discovery aid, not an independently authorized literature attestation. Previously reviewed source records remain authoritative.

## Run on Windows

Extract the ZIP into the repository root and run:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10eo_r2_definition_index.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10eo_r2_definition_index\run.ps1"
```

The runner accepts exactly two previously compared `develop` commits: `57f8079` and `40813d2`. They have the same inspected production code and differ in R1 audit artifacts and `.pytest_cache`. For other commits, stop and re-audit. It rejects pre-existing edits to watched source files, uses `pytest -p no:cacheprovider`, runs focused tests only, and ensures tracked diffs do not change.

Reports are saved as `output/run_*/audit.json` and `audit.md`. Inspect the per-family `occurrences` and `status` fields before any source is authorized. The index intentionally reports `TEXT_ONLY_NOT_CITED` for every literal match.

## Scope

No change to the CSV, original source excerpts, current cited source records, the proof tree, group transport, presentation, or Trust Boundary. The full test suite is reserved for the end of Phase 169.
