# Phase 165 R27-R59 — Bulk retirement gate

This package retires the legacy Group Calculation implementation **only when** its root-level callers have already been migrated. It never silently rewrites callers or treats a typed partial proof as a complete result.

## Production changes on a READY result

- `toda_calculation_facade.py`: remove the complete definitions of `build_toda_report` and `build_standard_toda_report`, and remove now-unused imports. Typed partial-result functions remain unchanged.
- Delete `toda_calculation.py` and `toda_calculation_report.py` when present.
- Delete the four remaining legacy specialization modules when present.
- Remove only test files that explicitly mention the deleted modules or retired public legacy functions. All removed files and the original facade are preserved in `phase165_r27_r59_retirement_backup.zip` before any deletion.

## Safety behavior

A production source file that imports the retired modules or contains a reference to the retired legacy facade functions blocks the change. The protected typed entry points are checked separately. A `BLOCKED` result means no production source or tests have been deleted or modified. The audit JSON records the blocking source paths. Dynamic import strings built at runtime cannot be fully identified by static analysis; review these separately before phase completion.

The installer operates on the parent folder of this package. A backup filename collision prevents destructive changes. Changes are idempotent. A full pytest suite is **not** run by this package.

## Usage

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r59.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r59\run.ps1"
```

The installer runs six focused tests. It writes `phase165_r27_r59_audit.json` with a status of `BLOCKED`, `CHANGED`, or `ALREADY_RETIRED`.

## Phase boundary

This step concerns removal of obsolete code paths. Mathematical proof completeness, broad compatibility, and the full regression suite must be verified separately before Phase 165 is closed.
