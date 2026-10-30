# EHP Proof Tracer — Phase 171 R2J-R4-R9-R5

This read-only, focused diagnostic identifies the next canonical backward-search frontier after R9-R4 has independently re-derived the surjectivity of the Hopf map from the source-bound Proposition 5.3 group premise.

## Scope

This package adds only its own files. It does not change the shared inference provider, the proof search engine, the trust boundary, the Web renderer, or any preexisting test. The validated R4-R8 proof is inspected solely for its inference rules and target subgoals. The canonical search engine independently reconstructs its ProofSteps from earlier screened sources. A matcher probe records the first genuine failure, distinguishing mismatched conclusions, mismatched ProofRule status, and rejection despite apparently matching premises. This observation does not prove the ultimate root.

## Requirements

Run in a `develop` worktree after the successful R9-R4 replay, with all prior Phase 171 audit modules available. The reviewed GitHub baseline is `58416a7da55a4d97bce161625cef98f673612118`.

## Commands

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r5_remaining_match_frontier\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r5_remaining_match_frontier\run.ps1"
git status -sb
git diff --stat
```

Only eight new and eight related focused tests are run. The complete pytest suite is reserved for Phase closeout. The report is written to `output/audit.json` under this package and contains the first rejected matcher attempt, its full typed premises, the canonical unresolved goal, and all selected observations. It does not promote an incomplete search to complete or claim that the public Web is verified.
