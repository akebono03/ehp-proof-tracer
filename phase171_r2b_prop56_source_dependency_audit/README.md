# Phase 171 R2B — Proposition 5.6 Source Dependency Audit

This is a read-only continuation of the completed R2A alignment audit. It does not change application source, database files, source assertions, proof steps, or registered theorem status.

## Purpose

The three unresolved registered 3-stem queries are (n,k)=(3,3), (4,3), and (5,3). R2A established that each database-typed goal differs structurally from the registered Proposition 5.6 candidate and that none of those candidate assertions has a proof link. R2B records these two blockers separately and extracts the original Proposition 5.6 statement and its proof from the checked-in `sources/toda/Toda_05_2.tex`. The proof text is preserved verbatim in an external audit report, and literal references appearing in the proof are inventoried.

This source presence is **not** certification of mathematical correctness or authorization of a GIVEN ProofStep. The source registration remains unverified and must be reviewed before implementing a proof transformation. This package makes no inference and does not attempt to equate `Suspension` with `IteratedSuspension` or alter generator identities.

## Windows PowerShell

Run from your repository root:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2B_R2.zip" -DestinationPath "." -Force
$Alignment = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery\phase171_r2a_prop56_20261029_070818_650545\alignment.json"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2b_prop56_source_dependency_audit\run.ps1" -ReportPath $Alignment -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2b_prop56_source_dependency_audit\run.ps1" -ReportPath $Alignment
git status -sb
```

The runner uses `python -m` from the repository root to preserve import semantics and runs only package-focused pytest. Git must be on `develop`, with a clean tracked working tree. Both the reviewed baseline and `origin/develop` must be ancestors of local `HEAD`; therefore a local branch that is **ahead** only by reviewed Phase 171 audit commits is allowed, but a **behind** or diverged branch is rejected. All committed differences from the baseline and from `origin/develop` must be limited to the reviewed Phase 171 audit directories. Pinned production source Git blobs must remain unchanged. Untracked audit folders are allowed. Neither `git push` nor reset/checkout is required.

The full source proof and classification are saved as UTF-8 `dependency.json` and `dependency.md` under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2b_prop56_*`. This is an audit report, not a completed proof.

## Boundaries

Only files in this package are new. No runtime implementation or formal project document is modified. No full pytest is run before Phase 171 closeout. Subsequent implementation must independently verify cited premises, preserve chronology and the Proof Tree trust boundary, and rely on generic generator representation rather than label-specific normalization.
