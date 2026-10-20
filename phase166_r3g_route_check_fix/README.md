# Phase 166 R3-G route check — audit-script fix

## Scope

Only the read-only audit script is corrected. No production source or existing tests are modified.

- `audit.py`: `inspect()` uses `tuple(statements) + tuple(base_candidates)` rather than concatenating a list and tuple.
- `run.ps1`: reruns the read-only audit from the repository root.
- `audit_result.json`: generated in this folder upon successful execution.

## Run

Unzip into the EHP Proof Tracer repository root, then run `powershell -ExecutionPolicy Bypass -File .\phase166_r3g_route_check_fix\run.ps1`.

Only static syntax and the corrected concatenation were checked during packaging. Runtime execution requires the user's environment. Full pytest was not run.
