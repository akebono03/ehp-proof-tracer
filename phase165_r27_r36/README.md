# Phase 165 R27-R36 — Typed Generator entrypoint cutover

This package replaces the four Web Generator entrypoints (Proof, Proof Scope, Applicability, Execution) and the two CLI entrypoints (`show-proof`, `explore-proof`) with calls to the typed Generator statement search introduced in R27-R34.

## Important semantic limits

- Proof: only proven statements become proof steps; an empty proof is labeled unproved.
- Proof Scope: exposes proven-statement count and search status; it does **not** claim that old Toda-membership/map-relation scope analysis has been reconstructed.
- Applicability: rule applicability is **not evaluated**. The result reports `not_evaluated`, with no claimed candidates.
- Execution: no inference rule is actually executed. The result reports `not_executed` and `NONE`. This is not a substitute for eventual typed execution functionality.
- The installer does not delete old Repository modules. That depends on removing other actual imports in a subsequent phase.
- No full pytest is performed.

## Changed files

- `web_generator_proof.py`: `WebGeneratorProofView` and `build_standard_web_generator_proof_view`
- `web_generator_proof_scope.py`: `WebGeneratorProofScopeView` and `build_standard_web_generator_proof_scope_view`
- `web_generator_applicability.py`: `WebGeneratorApplicabilityView` and `build_standard_web_generator_applicability_view`
- `web_generator_execution.py`: `WebGeneratorExecutionView` and `build_standard_web_generator_execution_view`
- `main.py`: `_run_show_proof_command`, `_run_explore_proof_command`

Each Web class receives optional `search_status`, `diagnostics`, and `open_goal_count` fields. All changes are planned with AST parsing before writing any file, and original files are backed up to `backup/`.

## Windows

Run from the repository root after extracting the archive:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r36\run.ps1"
```

Targeted pytest runs 11 tests in the package. The user's local repository is the authority for runtime behavior; static and installer tests cannot establish complete end-to-end correctness.
