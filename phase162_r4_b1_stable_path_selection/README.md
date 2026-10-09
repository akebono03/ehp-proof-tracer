# Phase 162 R4-B1 — Stable Proof Path Selection

This package adds a strategy selector without replacing a proof tree or changing renderers.

## Scope

For a concrete stable target above the canonical base, select Toda (4.5) transport. At the canonical base and outside the stable range, retain the existing proof ancestry. No inferred references, specialization steps, or textual proof are manufactured by this selection.

## Files

- `files/toda_stable_proof_path_selection.py`: new selection enum, immutable selection record, and function.
- `files/tests/test_phase162_r4_b1_stable_path_selection.py`: new focused tests.
- `run_phase162_r4_b1_stable_path_selection.ps1`: installs the two files and runs focused tests.

## Run

From the project root, extract the ZIP, then run `powershell -ExecutionPolicy Bypass -File .\phase162_r4_b1_stable_path_selection\run_phase162_r4_b1_stable_path_selection.ps1`.

## Boundary

R4-B1 chooses the *intended proof path*. R4-B2 must construct and validate a concrete ProofStep chain and connect it to the selected root; R4-B3 renders it. Selecting a route alone does not establish a proof.
