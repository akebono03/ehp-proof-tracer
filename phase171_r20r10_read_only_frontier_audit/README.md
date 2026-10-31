# Phase 171 R20R10 — Read-only Public Search Frontier Audit

This package observes the **actual** `search_group_from_registered_goal(n=3, k=3)` call, preserving the original first-success algorithm. It traces expansion proposals and proof outcomes and compares them against the independently built R4–R8 reference tree **only after** the genuine public search has finished. It never injects previously completed proofs or creates mathematical GIVEN steps.

Production code and existing tests are untouched. Outputs are written outside the repository, under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r20r10_read_only\<timestamp>\audit.json` (or the system temporary directory if LOCALAPPDATA is unset). The source guard checks actual reviewed Git blob content, while tolerating LF/CRLF conversion; HEAD equality is neither assumed nor sufficient.

From the repository root, after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r10_read_only_frontier_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r10_read_only_frontier_audit\run.ps1"
```

The full audit runs only the five focused unit tests, not the project-wide pytest suite. Python bytecode and pytest cache writes are disabled in the runner. For a quicker first pass, append `-SkipReferenceComparison`; this omits the independent R4–R8 tree replay but does not change public search. Do not infer `complete` from a matching backward proposal: check `public_complete` and the accepted proof events.

If the source guard fails, the package stops without writing or changing repository files. Review the actual code changes before producing a revised audit script; do not reset or clean the repository.
