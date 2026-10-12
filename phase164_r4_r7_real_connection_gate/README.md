# Phase 164 R4-R7 — Real typed-binding connection gate

This package exercises the real two Phase 164 R4-R6 typed bindings against the existing R2 citation check and R3 backward-proof adapter. It does not grant permission, create a fictional citing position, or change source mathematics.

## Installation and execution (PowerShell)

Run from the project root after extracting the ZIP to the project root:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase164_r4_r7_real_connection_gate.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase164_r4_r7_real_connection_gate\run.ps1"
```

## Outputs

`phase164_r4_r7_output/report.json` and `report.md` explain what can and cannot be authorized. The original seven-rule proof is reconstructed separately and must not be mistaken for registry-approved search.

## Boundary

R2 currently checks same-document ordering. The EHP Proof Tracer target is a separate work, so its Toda publication position is deliberately `None`. No full pytest is run here; it belongs to the final Phase 164 step.
