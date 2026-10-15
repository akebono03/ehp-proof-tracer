# Phase 165 R5-R13 — Legacy Narrative Compatibility Gate

This read-only package checks whether the historical Phase 162 Web Narrative and the canonical Phase 165 group-proof narrative can both render the same group query, without claiming mathematical or textual equivalence.

## Usage (Windows PowerShell)

Unzip in the EHP Proof Tracer repository root and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r5_r13_parity_gate\run.ps1"
```

The runner executes nine focused audit tests and two runtime rendering probes. It writes `audit_output/audit.json` and `audit_output/review.md`. It does not edit application code. The historical Phase 162 fixture regression is not skipped or deemed resolved; this package does not run that test suite. No full pytest is run.

A `REVIEW_REQUIRED` result means that the preconditions hold but compatibility and mathematical equivalence have not been proven. `PRECONDITION_FAILED` identifies a structural blocker. An exception from either renderer is captured as evidence without removing existing code.
