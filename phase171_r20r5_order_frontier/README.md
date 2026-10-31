# Phase 171 R20R5 — Public order-four proof frontier audit

This is a read-only audit, not a proof implementation. It compares independently inferred R4-R7 ProofStep ancestry to the public `shared_expansion_provider` proposal registry. It checks matching rule names, exact ordered subgoals, and an actual inference match with the original parents. No completed proof is passed into the public engine and no new GIVEN fact is created.

## Run

Extract the ZIP to the repository root (`ehp_proof`). From PowerShell, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase171_r20r5_order_frontier\run.ps1 -DryRun` followed by the same command without `-DryRun`.

The script runs only three relevant existing pytest cases, with the pytest cache disabled. It invokes the audit as a module, so repository-level imports resolve correctly. Read the generated `output/<UTC timestamp>/audit.json` for all checked obligations.

The audit validates reviewed source blob hashes rather than requiring a fixed HEAD. It stops without changing source if a reviewed source has changed.
