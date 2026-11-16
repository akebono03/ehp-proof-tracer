# EHP Proof Tracer — Phase 175 R3R8R1R2 tracked-worktree guard fix

This package fixes the specific preflight failure reported for R3R8R1R1:
`R3_PROTECTED_TRACKED_CHANGE: phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md`.

The earlier R3 Source Guard permitted changes only to its own historical files. After a newer audit package is committed, extracting a revised ZIP can modify tracked files belonging to that newer package. This must not be mistaken for a production modification, but it must also not authorize unknown files or changed source code.

## Exact scope

- `phase175_r3r8r1_verified_prior_public/worktree_guard.py` (new): checks Git porcelain `-z` and SHA256 of each explicitly reviewed, **unstaged** changed file. Only the existing R3 whitelist and exact named R3R8R1 files are accepted. Production source `phase165_r52_r9_shared_math.py` remains prohibited at preflight.
- `phase175_r3r8r1_verified_prior_public/audit.py`: `extended_scoped_preflight()` uses the new guard and R3's existing pinned-source validation for reviewed successor edits. The R3R7 history allowlist and its independent source check remain intact.
- `phase175_r3r8r1_verified_prior_public/install.py`: `preflight()` preserves the reviewed tracked-file hashes, while `verify_postflight()` requires the exact public patch and unchanged reviewed files. Rollback remains unchanged.
- `tests/test_worktree_guard.py` (new): exercises a real local Git repository, including production-change rejection, staged-change rejection, a successful guarded patch and rollback.
- `tests/test_lineage.py`: includes the new guard file in the existing additive-lineage acceptance tests.

No mathematical statements, proof rules, renderer, source database, or existing production files are modified **by this repair**. The previous R3R8R1 installer still performs its single-function production patch only after all preflight checks pass and restores the original bytes on a failed public verification.

## Execution — Windows PowerShell

Extract at the repository root. This overwrites the previous R3R8R1 package, **not** the production source file.

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R8R1R2.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r8r1_verified_prior_public\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
Write-Output "DRYRUN_EXIT_CODE=$LASTEXITCODE"
```

Only if `DRYRUN_EXIT_CODE=0`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $script
Write-Output "R3R8R1R2_EXIT_CODE=$LASTEXITCODE"
git status -sb
```

The normal run performs **focused pytest only** before the ordinary `(n,k)=(3,4)` proof search, trust-boundary verification, and shared Web renderer. Completion requires actual `complete`, zero open goals, verified proof tree and `generic-complete-proof`. The full pytest suite is reserved for the end of Phase 175.

## Validation status

The new successor worktree guard and existing R3R8R1 installer were run in temporary Git repositories under lightweight dependency stubs: **12 tests passed**. All shipped Python files compile and ZIP integrity is checked. The full project checkout, Windows powershell execution and real Web proof search are not available in the packaging environment. A DryRun or `pytest` PASS is not evidence of complete mathematical proof.
