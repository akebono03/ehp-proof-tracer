# Phase 169 R4A: Proposition 4.4 / EHP Route Audit

A read-only inspection of the historical Toda proof for `pi_6^4` and its current typed search connections. This package does **not** alter application code, registry entries, existing tests, or project documentation. It does not synthesize proof leaves or override the Toda (4.5) stable-range condition.

## Run

From the root of the repository on Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r4a_prop44_ehp_route_audit.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r4a_prop44_ehp_route_audit\run.ps1"
```

Requires the existing repository's Python dependencies and a checked-out `develop` branch. Only the four new focused tests and the seven existing R3O focused tests are executed. The full suite is not executed.

Reports are written to `phase169_r4a_prop44_ehp_route_audit/output/audit.json` and `audit.md`.

The goal is to diagnose whether Proposition 4.4's suspension-injectivity consequence and Proposition 4.2 / (5.1) surjectivity can be connected to a proof tree in a later implementation. No completion status is inferred from the presence of a cited source or a candidate expansion.
