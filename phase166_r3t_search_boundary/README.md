# Phase 166 R3-T Search Boundary Audit

This package inspects the existing recursive proof path without modifying production code.

It checks whether pi_4^3 is independently obtained by the shared prover, whether the existing cited Toda (4.5) specialization is available, and whether the finite-cyclic transport rule can propose its proof obligations when supplied typed candidate premises. Candidate obligations are not treated as proof.

## New files
- `audit.py`: complete `inspect` and `main`
- `test_audit.py`: three focused tests and full imports
- `run.ps1`: PowerShell entrypoint
- `README.md`: this guide

## Run
Expand into the EHP Proof Tracer root and run:

`powershell -ExecutionPolicy Bypass -File .\phase166_r3t_search_boundary\run.ps1`

## Completion and boundary
The report distinguishes proved pi_4^3 from hypothetical premises, and tests the existing Toda transport logic. It does not assert pi_5^4 COMPLETE and does not execute the full pytest suite. Production correction is deferred until these observed boundaries are verified.
