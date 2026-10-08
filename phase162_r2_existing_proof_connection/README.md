# Phase 162 R2 — Existing Proof Connection

This bundle connects a group-structure backward goal to already established source-group proofs and eta-family definitions. It does not create synthetic GIVEN proofs or consume a precomputed target-group proof. The EHP isomorphism is reconstructed using the existing seven Phase 161 inferences.

## Files

- `phase162_group_structure_backward.py`: Complete replacement of the Phase 162 group-goal module. Accepts the repository-native `Suspension` expression for the generator-image bridge, while retaining support for `MapApplication` as an input.
- `phase162_r2_existing_proof_connection.py`: New connector; place at repository root.
- `tests/test_phase162_r2_existing_proof_connection.py`: New focused tests.
- `run_phase162_r2_existing_proof_connection.ps1`: Copy files and execute focused pytest.

## Usage

Extract the archive into the EHP Proof Tracer repository root and run the PowerShell script under its extracted directory. The full test suite is intentionally not run.

## Boundary

This is a proof reconstruction and provenance-validation connection. It does not alter web narrative rendering. The test fixture explicitly supplies trusted GIVEN roots; it does not validate literature truth outside that trust boundary.
