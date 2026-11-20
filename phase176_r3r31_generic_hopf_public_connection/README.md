# Phase 176 R3R31 — Generic Hopf Substitution Public Connection

Adds one public backward-search provider call for the type-checked, isolated R3R30 rule.

The existing cited Proposition 2.2 source guard is reused. The new provider proposes two independent proof obligations; it neither creates a new GIVEN nor asserts that either obligation has been proved.

## Run

Extract at repository root on `develop` with a clean `phase165_r52_r9_shared_math.py`, then:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r31_generic_hopf_public_connection\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r31_generic_hopf_public_connection\run.ps1
```

The installer generates `CHANGED_FUNCTION_FULL_JA.md` containing the complete updated function in `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r31_generic_hopf_public_connection`.

Only focused tests run. It does not change the root group assertion or complete the unresolved group proof.
