# Phase 166 R3-T: pi_5^4 diagnostic

Read-only diagnostic for the registered group goal, Toda (4.5) backward expansion, symbolic eta specialization, and public narrative rendering.

## Files

- `audit.py`: functions `inspect()` and `main()`; no existing production functions replaced.
- `test_audit.py`: three targeted tests.
- `run.ps1`: invokes only targeted pytest and the read-only diagnostic.

## Run

From the EHP Proof Tracer project root, expand the ZIP into the project root and run `powershell -ExecutionPolicy Bypass -File .\phase166_r3t_pi54_diagnostic\run.ps1`.

## Scope and completion

This diagnostic does not claim to repair partial proofs. A nonzero `direct_toda45_expansion_count` or `eta_specialization_count` does not alone establish a complete proof. The next implementation step must be determined from the generated `r3t_audit.json` and the actual proof tree. No full pytest is run.
