# EHP Proof Tracer — Phase 173 R1 Read-Only Audit

This package audits the **current registered proof-search capability for n >= 3** without installing inference rules, editing data, changing tests, modifying application code, or updating official project documents.

## Reviewed repository snapshot

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`
- Reviewed GitHub HEAD: `11ea331f322883e2f2cf34b9e865dea2134f5058`
- `data/sphere.csv`: 797 distinct registered `(n,k)` coordinates with `n >= 3`, from explicit rows only
- Priority scope (default): all 34 registered `n=3, k=0..33` groups plus `(4,3)`, `(5,3)`, `(6,3)`, `(7,3)` (38 groups)
- All scope (explicit opt-in): all 797 registered groups

The preflight requires the exact reviewed branch and HEAD, verifies the pinned Git blobs of relevant sources, checks the remote `origin/develop` ref by default, and rejects **tracked or staged changes**. Existing untracked archive directories are allowed and left untouched. It does not fetch, reset, pull, commit, or modify tracked files. Do not assume a previous local HEAD has already moved forward.

## Windows PowerShell

Extract the ZIP into the existing repository root and execute:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_R1_NGE3_AUDIT_ONLY.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r1_nge3_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r1_nge3_audit\run.ps1"
git status -sb
```

Before running, inspect `git branch --show-current`, `git rev-parse HEAD`, `git status -sb`, and `git ls-remote origin refs/heads/develop`. If the local checkout is behind the reviewed GitHub HEAD, **review any existing changes first**. Only if the tracked worktree and index are clean, `git fetch origin develop` and `git merge --ff-only origin/develop` can update the local branch. The runner never does this for you.

`-DryRun` executes only the **new package's focused tests** and its read-only Git/CSV preflight; it does not run proof-search workers. The normal run executes the same tests, then isolates each selected group in a child Python process. To audit the whole registered scope explicitly, use `run.ps1 -Scope all`. The per-group timeout can be adjusted with `-TimeoutSeconds 480`. `-SkipRemoteCheck` bypasses only the online ref comparison; the exact reviewed local HEAD and blob checks still apply.

## Evidence and classification

Outputs are saved outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r1_*`:

- `audit.json` — selected coordinates, registered domain size, per-group typed DB result, search status, proof-step count, unresolved goals, diagnostics, GIVEN references, verified model citations, canonical Web route, and summary
- `audit.md` — review table (normal run only)
- `n_NNN_k_NNN.log` — one isolated worker log per selected group

`COMPLETE_AND_WEB_VERIFIED` requires a typed DB goal, complete proof search, a proven root matching that DB goal, no open goals, at least one ProofStep, a verified citation model, and a canonical Web complete-proof route with actual steps and lines. Missing proofs and missing typed results remain visible as gaps; only worker crashes/timeouts, inconsistent worker output, or a changed tracked tree cause the audit command to fail. The `priority` scope never claims coverage of unselected groups.

**Limitations:** This is an observational audit, not an independent formal verification of the truth of Toda's printed source assertions or the database priors. It does not run the repository-wide test suite; that is reserved for Phase 173 closeout. Actual proof-search and Web results must be obtained in the user's reviewed Windows checkout; the package's offline contract tests cannot substitute for them.

## Files

The archive adds only `phase173_r1_nge3_audit/` with `audit.py`, `run.ps1`, `tests/test_audit.py`, `__init__.py`, this README, `AUDIT_PLAN_JA.md`, and `CODE_FULL_JA.md`. All new function and test bodies, imports, and the complete execution launcher are reproduced in `CODE_FULL_JA.md`.
