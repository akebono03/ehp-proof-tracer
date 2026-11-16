# EHP Proof Tracer — Phase 175 R3R8R1: Verified Prior DB Public Connection

## Scope

This package corrects the mismatch identified by the actual R3R8 public search. The canonical solver accepts the earlier group $\pi_6^2$ as an adopted database prior (`GIVEN`), whereas the previously developed zero-image and Hopf generator-lift rules require all group premises to be inferred (`INFERENCE`). The R3R8 experiment stopped after six accepted steps, with seven open goals; its tracked edit was rolled back successfully.

The correction adds **two general provenance-checked alternatives**, without changing the older inference-only rules:

1. If a finite-cyclic group presentation is a *strictly earlier, freshly verified adopted DB prior*, and the zero image of its generator is separately inferred, the suspension map has zero image.
2. If a Hopf map is separately proved injective, its finite-cyclic codomain is a *strictly earlier, freshly verified adopted DB prior*, and the Hopf image of a domain element is separately inferred to be the codomain generator, the domain is the corresponding finite cyclic group.

The existing `admitted_db_step` and `verified_db_step` gates are used both when offering a candidate and when checking the actual parent `ProofStep`. A forged `GIVEN` step, a target reused as its own prior, an unknown database result, or a non-inferred generator image does not satisfy the rules. This is not a new mathematical source or an automatic promotion of group goals to proofs.

## Changes

- Existing file: `phase165_r52_r9_shared_math.py`, full function `search_shared_group_goal()` only. No top-level imports or other existing functions are changed. The single route insertion is guarded by `(n,k)=(3,4)`.
- New `rule.py`: four reusable functions implementing two general verified-prior inference alternatives.
- New `route.py`: connects the two alternatives to the earlier R3R7 source-backed expansions; the original inference-only options remain available.
- New package-specific `install.py`, `audit.py`, `run.ps1`, tests, and full-code documentation. The installer retains the pinned original Git blob, checks that the complete prior function is unchanged, and backs up before writing.

No direct $\pi_7^3$ result is registered as `GIVEN`. No saved completed proof is imported. No changes to the Web renderer, documentation under `docs/`, or unrelated group routes are made. The canonical First Successful Proof Search policy is preserved.

## Installation and verification

Extract `R3R8R1.zip` into the repository root. In PowerShell:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R8R1.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r8r1_verified_prior_public\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
Write-Output "DRYRUN_EXIT_CODE=$LASTEXITCODE"
```

Only when `DRYRUN_EXIT_CODE=0`, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $script
Write-Output "R3R8R1_EXIT_CODE=$LASTEXITCODE"
git status -sb
```

Normal execution runs focused pytest and then the real ordinary `(n,k)=(3,4)` search, proof trust verification, linked narrative model, and standard Web Group proof view. The tracked edit is automatically rolled back if any success condition fails. Reports and backups are written outside the repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3r8r1_verified_prior_public\`.

## Acceptance criteria

- Source Guard and independently observed R3R7 six inference obligations still pass.
- Focused tests pass, including tests for forged or non-earlier DB premises and the actual ordinary group proof search.
- Actual search is `complete`, has no open goals, and its conclusion equals the typed database target.
- The proof tree passes the existing trust boundary; the Web view is `generic-complete-proof` with references and no partial flag.
- On failure, the exact original tracked function is restored and the reason recorded. No full-suite pytest is executed before the end of Phase 175.
