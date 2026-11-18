# Phase 175 R4R12R5R1 — Reviewed HEAD Pin Correction

This is a full replacement of the R4R12R5 audit package, with only its
`installer.EXPECTED_HEAD` changed to the reviewed develop commit
`9203e1a8c077320a58214bda40d9bfeb17704f58` and one pin regression
check added. The previous commit `6cdf40e089cb2950d2ae9a6aadb2a36188ca0e7d`
is its direct ancestor. The R4R3 source blob pin and all other fail-closed
checks remain unchanged.

Extract the ZIP at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r5_iterated_suspension_endpoints\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r5_iterated_suspension_endpoints\run.ps1
```

The standard runner tests the installer first and, after a successful real
installation, runs focused endpoint/rule/provider tests. Project-wide pytest
is not run. The quotient proposal remains unproved.
