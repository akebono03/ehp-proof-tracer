# EHP Proof Tracer — Phase 174 R55R3R2R1

## Purpose

This is the CRLF-safe source-guard correction for the R55R3R2 removal of the bespoke proof Narrative introduced in R55R3. It does not change the mathematics, proof search, registered sources, or scope of the removal.

The R55R3R2 installer computed a Git blob hash after normalizing CRLF newlines to LF. This caused a false mismatch for `phase168_r3_27_typed_statement_projection.py` (a CRLF file on GitHub `develop`). This revision verifies the original committed **bytes** before normalizing text for reviewed code replacement. The installed file retains its original local line-ending convention.

## Review boundary

Reviewed GitHub `develop` HEAD: `d923ff2a34b6ba9d4c23d3da0221402f0b815f46`. The three existing production targets remain: `phase168_r3_5_model_renderer.py`, `phase168_r3_37c_reference_projection.py`, and `phase168_r3_27_typed_statement_projection.py`. The reviewed, generated R55R3 and optional R55R3R1 package directories are removed only after exact manifest validation. All other production code and documentation remains unchanged.

## Run

Extract this ZIP at the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R55R3R2R1 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R55R3R2R1 failed" }
```

The script runs only focused tests, then audits the real source-first `(n,k)=(7,5)` Group query and public HTTP output. The full pytest suite is reserved for the end of Phase 174. Read `CODE_FULL_JA.md` for complete modified function bodies.

## Fail-closed guarantee

The guard checks the branch, reviewed history, pinned Git object SHAs, local source contents, and legacy-file SHA-256 manifest before any changes or deletion. Unknown user edits are never silently overwritten or removed.
