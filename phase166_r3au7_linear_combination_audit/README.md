# Phase 166 R3-AU-7: Linear-Combination ID Audit

Read-only inspection of multi-coefficient generators in `data/sphere.csv`.

For each nonzero coordinate, the audit looks for the same `(n,k)` component with the corresponding zero-based `id`. This is an empirical check, not mathematical certification.

Run `powershell -ExecutionPolicy Bypass -File ".\phase166_r3au7_linear_combination_audit\run.ps1"` from the repository root. Outputs appear in `results/`.

No existing production code or project documentation is modified. Only three targeted tests are run.
