# Phase 165 R27-R29

Safely retire legacy Prop. 5.6 proof-step extraction in the historical Phase 163 helper, then delete the Prop. 5.6, midstream, and Phase 65 bootstrap implementation modules if no other root-level production imports remain. The explicit typed literature registration API is preserved.

Extract ZIP in the repository root; run `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r29\run.ps1`.

The installer performs a preflight AST import audit and backs up all files before changes. Historical tests that explicitly import removed bootstrap modules are not migrated in this step. Full pytest is deferred until Phase 165 closure.
