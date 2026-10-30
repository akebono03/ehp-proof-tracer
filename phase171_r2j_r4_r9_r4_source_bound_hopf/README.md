# EHP Proof Tracer — Phase 171 R2J-R4-R9-R4

This audit-only package tests a **source-bound Hopf codomain** in the canonical recursive proof engine. In the R9-R3 run, reconstructed Hopf premises were rejected by the existing matcher. An earlier database group result is eligible as a GIVEN, but the established cited Hopf surjectivity rule deliberately requires an INFERENCE for the cyclic codomain.

The package applies the already supported `SourceBoundGoal` mechanism to that one group subgoal. The cyclic group must then be re-derived from the uniquely screened, earlier Proposition 5.3 general statement. All other proof goals keep the normal scoped R9-R2 provider. No prior completed `ProofStep` is passed into the search. No theorem, GIVEN, map property or database fact is invented.

This is not a public-provider patch. The audit separately records the reconstructed Hopf statement, the status of the full scoped proof search, and acceptance by the existing narrative trust boundary. Public Web completion is always reported as false in this phase.

Extract the ZIP in the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r2j_r4_r9_r4_source_bound_hopf\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r2j_r4_r9_r4_source_bound_hopf\run.ps1'
git status -sb
git diff --stat
```

Only 16 focused tests run (8 new and 8 existing). The full suite remains deferred until the end of Phase 171. No tracked production file, prior test, or historical documentation is modified.

Reviewed against GitHub `akebono03/ehp-proof-tracer`, branch `develop`, commit `b531cace84529fa9c38584fa8883037f3e808852`.
