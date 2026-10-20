# Phase 166 R3-R — Read-only proof ancestry audit

This bundle audits the local implementation of the R3-Q `GeneratorImage` to `Relation` transformation using real proof-search observations. It does not patch production modules or delete existing facts.

## Modified files and functions

No existing files, classes, functions, or imports are modified. New files: `audit.py` (`ancestors`, `audit_relation_steps`, `main`); `test_audit.py` (four isolated tests); `run.ps1` (PowerShell runner). All function and class definitions are contained in the supplied source files.

## Usage

From the EHP Proof Tracer repository root, unpack this directory and execute:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3r_proof_tree_audit.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3r_proof_tree_audit\run.ps1"
```

Targeted pytest runs only. The audit writes `r3r_audit.json` in this bundle directory. Exit code 2 means the requested chain was not verified, not that a mathematical theorem is false.

## Limits

The audit follows `ProofStep.premises` by identity, and checks direct registry links to `GeneratorImage` evidence. It does not authorize deletion of unrelated `GIVEN` entries. Full pytest is deferred until the end of the phase. This audit checks pi3^2; pi4^3 and pi5^4 reconstruction are separate follow-up steps.
