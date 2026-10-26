# Phase 169 R3A — EHP and Prior-Proof Frontier Audit

This package **does not modify** the production application, tests, or documentation.

## Purpose

Diagnose why the current canonical backward search cannot derive the finite cyclic structure of `pi_5^3`, although `pi_4^2` has a complete proof. The report compares the legacy, typed EHP goal expansion with the currently connected shared expansion provider. It also examines the first EHP premise frontier and exact, screened GIVEN leaves.

A caller-local, **experimental** search may be performed with the actually completed `pi_4^2` inference root supplied as an explicitly ordered prior proof. That experiment is not published ordering metadata, not a production proof, and is never persisted. It is used solely to distinguish missing prior-proof reuse from missing inference rules.

## Usage (Windows PowerShell)

Extract the ZIP to the repository root, then run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase169_r3a_ehp_reuse_frontier_audit\run.ps1"
```

## Outputs

- `output/ehp_reuse_frontier.txt`
- `output/ehp_reuse_frontier.json`
- `output/audit_error.txt` if an unexpected error occurs.

The runner executes five existing focused pytest modules, not the full suite.

## Boundaries

- No new GIVEN facts or source approvals.
- No legacy proof replay.
- No modifications to the shared search, proof order, citation boundary, or renderer.
- A proposed expansion is not a verified ProofStep.
- A successful experimental ordered reuse must **not** be reported as Web completion.
