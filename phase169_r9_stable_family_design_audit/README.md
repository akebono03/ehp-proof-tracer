# Phase 169 R9: HyoujiGen Stable-Family Design Audit

This audit-only package inspects the `kinds=0` metadata in the existing `data/HyoujiGen.csv`, the definitions of the related typed generator and narrative functions, and the distinction between a family's first named dimension and the Freudenthal stable range. It changes no production code, existing tests, or project documentation.

Unpack into the repository root, then run from PowerShell:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r9_stable_family_design_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r9_stable_family_design_audit\run.ps1"
```

The report and data are written into this package's `output/` directory. The runner executes four focused audit tests only. No full test suite is run, and no proof completion is inferred.

## Proposed implementation boundary

A typed family candidate is identified by DB family ID, stem, minimum dimension and indexed generator symbol; group stable-range checks are separate. A cited definition (or equivalent verified source) is required before a candidate generator-image statement may be treated as a proved equality. The standard renderer should collapse a verified series of element-image steps into one `E^r` statement while keeping every ProofStep and citation in the model.
