# Phase 168 R3-2: Runtime Boundary Audit

This package performs a read-only audit of the actual shared proof search, `PartialProofResult`, provenance attached to proved steps, and Web narrative adapter for pi_4^2, pi_3^2, pi_4^3, and pi_5^4.

Run from the project repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase168_r3_2_proof_tree_runtime_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_2_proof_tree_runtime_audit\run.ps1"
```

Outputs: `output/runtime_boundary.json` and `output/runtime_boundary.md`. Upload both for the next step.

No production files, documents, or tests are changed. This audit does not run pytest, infer missing source citations, or certify the mathematical proof. Runtime results are local to the user's current working tree. Only the first 400 profiled call events are retained per goal. The output includes representations of proof objects and may be large.
