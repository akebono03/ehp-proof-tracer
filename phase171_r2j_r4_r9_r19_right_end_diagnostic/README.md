# Phase 171 R2J–R4–R9–R19: right-end-group diagnostic

This audit examines why the existing canonical proof search cannot independently reconstruct the exact right endpoint, `pi_6^5 = Z/2{eta_5}`, required by its already-registered cardinality rule for `pi_6^3`.

The script verifies the reviewed R18 result and the published R11 shared-provider blob, then compares existing typed source assertions, Proposition 5.1 eta specialization, general scalar specialization, and actual shared provider proposals. It traces the original recursive resolver without modifying it. No completed proof is supplied to production. No new fixed fact, `GIVEN`, rule, alias, or public completeness claim is introduced.

Extract the ZIP in the repository root on branch `develop`, and run `run.ps1 -DryRun`, then `run.ps1`. This performs seven focused tests and writes `output/audit.json`. Full-suite pytest is intentionally excluded.

The existing R16, R17, and R18 audit packages and reports must remain available in the repository. The audit fails closed if the source baseline or R18 result differs from the reviewed version.
