# EHP Proof Tracer — Phase 171 R2J-R4-R9-R9

This package connects a source-screened finite cyclic-structure backward obligation to the ordinary shared Proof Search provider. The rule says a finite group of order `m` with a proved element of order `m` is cyclic, and a registered generator identity must agree with the requested presentation.

## Changes

The installer modifies only the existing `shared_expansion_provider()` function in `phase165_r52_r9_shared_math.py`, inserting four statements immediately after the reviewed R9-R8 provider hook. Top-level imports are unchanged. The package adds `source.py` with the full typed inference rule and backward provider, `install.py`, `audit.py`, focused tests, and this documentation.

The backward provider reuses the reviewed R9-R7 typed source-witness proposer, which currently supports order four. It never uses that source as proof of nonzeroness, cardinality, or element order. All new cyclic-structure premises must be independently reconstructed by the existing recursive proof search. No prior complete `ProofStep` is injected.

## Preconditions and protected patch

Use branch `develop`, with R9-R7 and R9-R8 already installed. The installer accepts only GitHub-reviewed baseline `phase165_r52_r9_shared_math.py` with the exact three reviewed hooks (R7, R8, and optional already-installed R9). It refuses unknown local edits, does not reset or pull, and is idempotent. The reviewed original Git blob is `68846671215c38e3e0a572932b8ed955a7880edc`.

## Windows PowerShell

Extract the ZIP in the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r9_public_cyclic_structure\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r9_public_cyclic_structure\run.ps1"
git status -sb
git diff --stat
```

The run executes 10 new tests and 8 focused R9-R8 tests, not the full suite. It then writes `output/audit.json`. The installer also writes the **entire final** `shared_expansion_provider()` and `phase165_r52_r9_shared_math.py` into its output folder, along with the original file backup if a patch is applied.

## Completion boundary

Success requires exactly one generic cyclic-structure proposal in the public provider, a valid independent inference match, 0 new `GIVEN`, and passing focused tests. Public Proof Search and Web completion are reported as observed; this package does not claim those are complete. Remaining full-order, short-exact or cited-source proof paths belong to later iterations. The public Trust Boundary and Web renderer are not modified.
