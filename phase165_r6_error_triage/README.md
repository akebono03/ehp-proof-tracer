# Phase 165 R6 — Collection error triage

Read-only classification of the prior scoped pytest collection log. This tool does not collect or run the project-wide suite, alter tests, reintroduce retired APIs, or dismiss collection errors. It creates `phase165_r6_audit_results/collection_error_triage.json`.

## Run

From the repository root on Windows, extract the ZIP with `Expand-Archive -Force` and invoke `powershell -ExecutionPolicy Bypass -File .\phase165_r6_error_triage\run.ps1`.

## Boundary

Classification indicates shared exception messages, not validated shared root causes. Review each dependency against current source and tests before any test change or exclusion. Phase closure remains pending.
