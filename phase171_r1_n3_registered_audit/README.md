# Phase 171 R1 — n=3 Registered Group Audit

This package performs a **read-only** audit of all distinct `(n=3, k)` group coordinates explicitly registered in `data/sphere.csv`, currently `k=0..33` (34 groups). It does not implement mathematical inference rules, change the database, mark unfinished proofs complete, or run the repository-wide test suite.

## Audited code and snapshot

The package was prepared against `akebono03/ehp-proof-tracer`, GitHub `develop`, commit `715b00d67d4b3ff4b34bf87229842d14960ea6bb`. Its preflight checks the branch, local and remote commit, clean tracked worktree, six reviewed Git blobs, and the explicit CSV group coordinates. The audit folder may remain untracked.

The baseline worker/API was reviewed in `phase170_r3_r8_n2_exhaustive_audit/audit.py`. This package uses the existing `search_group_from_registered_goal(n=3,k=k)`, `exact_prior_database_result(3,k)`, and canonical `build_standard_web_group_proof_view` directly. It records exact search/Web outcomes without assuming the Toda (5.2) transport applies to the n=3 target.

## Windows PowerShell

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase171_r1_n3_registered_audit.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r1_n3_registered_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r1_n3_registered_audit\run.ps1"
git status -sb
```

`-DryRun` runs the focused package contract tests and read-only repository checks but does not start proof searches. The regular invocation executes 34 separate workers and validates the public Web result for each. All outputs go into `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r1_n3_audit_*`, including `audit.json`, `audit.md`, and individual `k_XXX.log` files. Proof gaps are legitimate outcomes, and `AUDIT_COMPLETE_WITH_GAPS` has exit code zero; worker failures and changed tracked files are errors.

Use `-TimeoutSeconds 480` if a legitimate search requires a higher per-group timeout. Do not run the full pytest suite during Phase 171 R1.

## Scope and limitations

A `COMPLETE_AND_WEB_VERIFIED` result means the existing typed proof search and public, trust-gated Web path completed under the reviewed code. It is not independent verification of the mathematical truth of source assertions, the original printed Toda edition, all possible group presentations, or arbitrary `(n,k)`.

Files added at the repository root: this package's `audit.py`, `run.ps1`, `tests/test_contract.py`, `__init__.py`, `README.md`, `監査方針.md`, and `FULL_CHANGED_CODE_JA.md`. No pre-existing source, test, or official document is altered.
