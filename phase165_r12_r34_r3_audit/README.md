# Phase 165 R12-R34-R3: GeneratorSuspension audit

Read-only, targeted provenance inspection for the foundational identity suspension leaf.

## Scope

The package inspects the canonical `GeneratorSuspension` with arguments `ι₁`, `ι₂`, checks the `GIVEN` ProofStep's foundational citation, and runs focused tests. It does **not** claim that the displayed `π₄³` tree uses this exact leaf or that its ancestry belongs to `π₃²`; checking the production runtime tree requires a separate trace capture. It changes no production files and does not run the full test suite.

## Run from project root (PowerShell)

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r12_r34_r3_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r12_r34_r3_audit\run.ps1"
```

Expected output: `phase165_r12_r34_r3_audit/audit_result.json` and focused pytest results.

Completion of this package's tests certifies only the construction and provenance of the foundational leaf, not production tree ancestry. Renderer restructuring is outside this R3 audit and belongs to R4.
