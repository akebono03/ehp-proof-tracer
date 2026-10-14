# Phase 165 R27-R16 — First legacy builder removal

This patch removes the automatic legacy Production Repository construction in the standard Operation query entrypoint. It deliberately returns a structured not-found result until the common typed proof pipeline supports certified operation proofs. It does not fabricate evidence, and it preserves the explicit-repository API `query_repository_operation_input`.

Only `repository_operation_query_facade.py` is modified. The entire `query_standard_repository_operation_input` function and its import section are replaced via a guarded script. A backup is created. No other production files are edited.

Run from the repository root using `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r16\run.ps1`. Targeted pytest only. This step does not remove the shared Bootstrap or affect Generator APIs; those require subsequent migrations. Old tests expecting legacy proof-backed Operation results will need deliberate transition in a later substep.
