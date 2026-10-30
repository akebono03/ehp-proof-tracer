# EHP Proof Tracer — Phase 171 R2J-R4-R9-R6

This audit-only package repairs the **second** Hopf surjectivity reconstruction in the isolated Phase 171 scoped canonical search. The first Hopf branch (R9-R4) is retained.

## Scope and soundness

The R9-R5 real-source matcher trace identifies `H: pi_6^3 -> pi_6^5`: the reconstructed codomain group has `GIVEN` proof status although its unchanged surjectivity rule requires `INFERENCE`. The other Hopf-image premise remains a cited `GIVEN`.

This package uses the existing `SourceBoundGoal` contract to force re-derivation of the cyclic codomain from one unique, publication-eligible fixed Proposition 5.1 source. Only a typed `GoalExpansion` is introduced into the scoped provider. No completed proof step, new `GIVEN`, target result, database row, or literature citation is injected. All existing production providers, match guards, trust boundaries, and Web entrypoints are unchanged.

The package is not a general public-provider implementation. A full scoped search may remain partial after this specific repair. Trust-boundary acceptance and public Web completion are reported separately.

## Windows PowerShell

Extract the ZIP into the Git repository root, then execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r6_source_bound_cited_hopf\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r6_source_bound_cited_hopf\run.ps1"
git status -sb
git diff --stat
```

The runner executes 10 new and 8 existing focused tests, followed by independent reconstruction and a read-only scoped search. A full repository pytest suite is deferred until the Phase 171 closeout.
