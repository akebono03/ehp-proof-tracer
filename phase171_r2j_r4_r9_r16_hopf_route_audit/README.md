# Phase 171 R2J–R4–R9–R16: Independent EHP Map Obligation Audit

This **read-only audit** investigates a specific failure in the ordinary `π₆(S³)` proof search. R15 found sixteen distinct unresolved goals: fifteen with unproved proposals and one without any proposal. The missing proposal requests an isomorphism `E: π₅(S²) → π₆(S³)` that is mathematically false on the 2-primary components (`Z/2` and `Z/4`). The correct short-exact-sequence argument needs **injectivity**, not isomorphism.

R16 does not add this incorrect isomorphism, weaken the canonical resolver, or add any `GIVEN` leaf. Instead, it independently queries the existing canonical resolver for four legitimately useful obligations: Hopf surjectivity at degree 7, Hopf surjectivity at degree 6, vanishing of the connecting homomorphism, and suspension injectivity. Each query uses the same screened earlier references and shared expansion provider as the public proof search. Existing finished proof trees are never inserted into the search.

## Run on Windows PowerShell

Unzip the archive at the repository root. On a clean `develop` worktree with R11-compatible shared-provider content and existing R14/R15 JSON reports:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r16_hopf_route_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r16_hopf_route_audit\run.ps1"
```

`run.ps1` invokes only the six focused R16 tests, with pytest's cache provider disabled, and the read-only audit. The full repository test suite must not be run during this step.

Results are written to `phase171_r2j_r4_r9_r16_hopf_route_audit/output/audit.json`. An independently proved map obligation is **not** a proof of the original `π₆(S³)` group structure. This stage does not authorize a web `complete` status.

## Safety guarantees

- Only checked-out `develop` and the unchanged R11 provider blob are accepted.
- Existing R14 and R15 reports must agree by SHA-256 and metadata.
- Production source files, `GIVEN` statements, proof inference rules, rendering, and trust boundaries are untouched.
- Only exact earlier screened fixed statements are accepted as proof leaves.
- Unexpected isomorphism proposals, malformed proof ancestry, or unrecognized output abort the audit.

Mathematical background: Wang and Xu, *A Survey of Computations of Homotopy Groups of Spheres and Cobordisms*, Theorem 3.2.59 (2-primary groups at dimensions 5 and 6).
