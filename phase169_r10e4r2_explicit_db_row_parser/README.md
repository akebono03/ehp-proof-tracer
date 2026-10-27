# Phase 169 R10E4-R2 — exact DB row parser repair

Fix one defect in the R10E4 DB admission parser: `data/sphere.csv` contains
separator rows with an empty `n` field. The previous `int(row["n"])` inside an
`any()` generator raised `ValueError`, which incorrectly made **every later
explicit DB row** appear absent.

This package changes only `_has_explicit_row()` in
`phase169_r10e4_ordered_db_prior/db_prior.py`. It preserves the `(k,n)`
precedence rule, source provenance and all proof trust checks. No other
production file, existing test or project document is modified.

To install on Windows from the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10e4r2_explicit_db_row_parser.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e4r2_explicit_db_row_parser\run.ps1"
```

The runner creates a byte-for-byte backup, emits a complete replacement
function and complete replacement module, runs focused pytest and audits real
stable base rows. On any failure, it restores only the module it changed.
The full pytest suite is not run. A source row is still a DB hypothesis,
not a fabricated literature theorem. The target is not declared complete
merely because its base group is present.
