# EHP Proof Tracer — Phase 171 R2J-R4-R9-R3

This is a strictly read-only diagnostic for the scoped canonical-search gap observed in R9-R2. Its first unresolved dependency is the Hopf-surjectivity statement for `H: pi_7^3 -> pi_7^5`, which prevents the subsequent delta-zero, suspension-injective, short-exact, and cardinality conclusions from being replayed.

This package records the exact R4-R8 Hopf inference rule and its required premises, then runs the same positioned `pi_6^3` target through the existing recursive engine using R9-R2's scoped rule-only provider. An in-process, temporary observer records canonical proof events and attempts to match that precise Hopf inference rule. The original matcher remains authoritative and is not changed. An observation is never used as mathematical evidence.

No completed proof steps are added to the repository, no unregistered literature statement or database result is created, and no shared production provider, Web code, source document, or previously established API is changed. A partial result is reported as partial, never as a completed Web proof. This phase does not resolve the gap or certify the public Web proof.

## Run from the repository root on Windows PowerShell

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic\run.ps1"
git status -sb
git diff --stat
```

The runner executes only focused tests: eight new checks and the seven R9-R2 source-unit checks. The full test suite remains deferred to Phase closeout. JSON diagnostics are written to the package's untracked `output/audit.json`.

The diagnostic distinguishes three principal outcomes: not all Hopf premises were reconstructed, the matcher rejected reconstructed premises, or a match was found but the root was not admitted. It also records actual observed proof-rule kinds to detect premature direct GIVEN/DB reuse. These are diagnostic categories, not self-certifying explanations.
