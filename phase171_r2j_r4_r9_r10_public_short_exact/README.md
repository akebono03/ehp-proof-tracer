# EHP Proof Tracer — Phase 171 R2J-R4-R9-R10

## Purpose

Connect the **existing, general** EHP short-exact backward inference
`expand_ehp_short_exact(goal)` to the common recursive proof-search provider.
This is the next missing obligation after the successful R7 cyclic root,
R8 middle cardinality, and R9 cyclic structure connections.

The mathematical inference is already implemented in
`phase171_r2j_r4_r5_short_exact_sequence/source.py`. Its typed premises are
`MapInjective(E)`, a valid `TodaProp42ExactnessStatement` for the E-H window,
and `MapSurjective(H)`. Every premise must be independently inferred by the
existing proof search; this package does **not** add a completed short-exact
proof, a group structure, a literature citation, or a new `GIVEN` leaf.

## Changes

- `phase165_r52_r9_shared_math.py`: insert exactly two lines in the full
  `shared_expansion_provider()` function, immediately after the R9 hook.
  Top-level imports and all other existing functions remain unchanged.
- New directory `phase171_r2j_r4_r9_r10_public_short_exact/`:
  `install.py`, `audit.py`, `tests/test_audit.py`, `run.ps1`, and documentation.
- The installer checks the reviewed GitHub baseline and exact existing
  R7/R8/R9 patches. Unrecognized changes abort without overwriting files.
  It supports both uncommitted prerequisite hooks and already-committed hooks,
  and it is safe to rerun.
- After installation, the **entire changed function** and **entire changed
  existing module** are saved to `output/shared_expansion_provider_FULL.py`
  and `output/phase165_r52_r9_shared_math.FULL.py`.

## Run on Windows

Unzip into the root of the `develop` checkout of
`akebono03/ehp-proof-tracer`. In PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r10_public_short_exact\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r10_public_short_exact\run.ps1"
git status -sb
git diff --stat
```

The execution runs only 17 focused tests (eight new and nine existing),
then reports the public search status and first unresolved goal in
`output/audit.json`. No full test suite is run until Phase closeout.

## Completion boundary

Successful integration means the ordinary shared provider offers exactly
one verified route for the EHP short-exact goal, matching the established
R4-R5 inference. It does **not** mean the public group proof is complete.
Any remaining map-property or citation subgoal must be resolved in the next
implementation increment, not assumed in this one. The Web renderer and
its proof-tree trust boundary are unchanged.
