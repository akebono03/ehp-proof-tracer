# EHP Proof Tracer — Phase 174 R3-R7-R48R1

This archive repairs one missing function-local import in the R48 read-only audit.
The invoked function `find_inference_matches_for_rule` already exists in `proof.py`.
The patch changes only the R48 audit import and adds one scoped regression test.
No mathematical source, inference rule, provider, existing API, renderer, or production module is changed.

Extract the ZIP into the repository root on `develop`. Run `run.ps1 -DryRun`,
then `run.ps1`. The patch refuses unreviewed source content, changes no files
in dry-run mode, and is idempotent. It invokes the original R48 bounded audit
and its focused pytest groups, then the R48R1 patch regression. The full test
suite is intentionally not run before the end of Phase 174.
