# Phase 155-R4-4 — canonical command / residual boundary decision

## Residual decision

- module-global promotions: 1
- residual validation lane: 750

Residual tests are retained. They are not marked removable.
R5/R6 will decide historical/heavy/runtime treatment.

## Canonical set

- canonical source test IDs: 9069
- canonical files: 768

Canonical execution command:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase155_r4_4_audit_output\run_phase155_canonical_regression.ps1
```

Canonical collect-only command:

```powershell
python .\phase155_r4_4_audit_output\run_phase155_canonical_regression.py --collect-only
```

## Production-module boundary

- root production modules: 200
- direct/global owned modules: 191
- indirect-only modules: 4
- unowned after transitive imports: 5

## Boundary

No production code or existing test was changed.
The canonical regression itself was NOT executed.
Repository-wide pytest was NOT run.
