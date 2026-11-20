# Phase 176 R3R28 — Public Toda (5.5) Quadruple Bridge

This installation appends the independently source-verified second clause of Toda (5.5) to the default typed bridge and wires its isolated backward inference into the shared provider.

The source is registered once and the generated relation remains an **inference goal**, never a direct GIVEN group conclusion. Existing default source IDs are kept stable by appending the new reference after all previous sources.

## Run

Extract at the repository root on the `develop` branch, with Phase 176 R3R27R1 and R3R27R1R1 already installed.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r28_toda55_quadruple_public\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r28_toda55_quadruple_public\run.ps1
```

Reports and the complete **post-change function bodies** (`CHANGED_FUNCTIONS_FULL_JA.md`) are generated under `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r28_toda55_quadruple_public`.

The entire pytest suite is not run.
