# Phase 163 R4-R58 Registration Readiness

Read-only staging readiness assessment for Toda equations (2.9), (2.10), and (4.3). It reads existing Phase R55, R56, R57 JSON reports; it does not mutate the registry, allocate IDs, verify formal mathematical semantics, or connect proof search.

From the project root, extract the archive and execute `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r58_registration_readiness\run.ps1`. Only nine focused tests are run. Results are written to `phase163_r4_r58_output` as JSON, CSV, and Markdown.

The word "ready" means ready to stage the source-grounded record **with unresolved semantics**, not ready as a verified assertion or citable proof premise. All trial IDs remain temporary.

This repaired package fixes the R4-R58 test fixture paths. The test fixture reads the R55-R57 outputs from their actual phase output directories, using the same absolute paths provided to the runner through `R58_TRIAL_PATH`, `R58_SCOPE_PATH`, and `R58_BOUNDARY_PATH`. No project-root `trial.json`, `scope.json`, or `boundary.json` files are required.
