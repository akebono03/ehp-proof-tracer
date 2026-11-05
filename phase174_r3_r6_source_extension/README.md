# EHP Proof Tracer — Phase 174 R3-R6

This archive connects cited universal Toda equations (4.8) and (5.5) to the existing generic backward proof search. It neither registers the target group as a GIVEN nor adds a group-specific narrative renderer.

## Reviewed base

`akebono03/ehp-proof-tracer`, branch `develop`, commit `7bd64d36e17246195525ecb0ec27a170abb73206` (`174-3-5`). The prior local HEAD `45d97b2adc73c2347866de28b344fce1e6d2c095` is accepted only when the worktree matches the reviewed R3-R5 implementation blob for blob. The remote `develop` must match the reviewed HEAD. The runner never fetches, resets, merges, commits or pushes automatically.

## Changed files and complete functions

Four existing files are changed, only after source blob checks:

* `phase165_r52_r9_shared_math.py`: `build_shared_typed_bridge()` and `shared_expansion_provider()`.
* `phase174_r3_r4_public_delta_connection/tests/test_connection.py`: `test_r3r4_real_production_file_has_only_reviewed_wiring()`.
* `phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py`: `test_public_pi85_cyclic_root_and_delta_proposals_reached()`.
* `phase174_r3_r5_preflight/audit.py`: `inspect_source_provider()`.

All existing module-level imports remain unchanged. Complete revised functions are exported during installation to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r6\*_FULL.py`. New file contents, including full imports, classes and functions, are included in `CODE_FULL_JA.md`.

The source checks pin the adopted Chapter IV/V Git blobs and the reviewed ordered manifest: Toda (4.8) = 7500, Toda (5.5) = 8600, Proposition 5.6 = 8800. Only the two **universal** formulas are admitted as source GIVENs. Their specializations require independently inferred proof steps. The original printed edition has not been independently verified.

## Source literal correction

The R3-R6 verification guard now matches the adopted Toda (4.8) text exactly: `\ \text{は単射で, }` (with a space before the closing brace). The pinned Chapter IV/V blobs, conditional premise checks, manifest order and source ancestry remain mandatory.

## Run (PowerShell)

Extract the ZIP at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r6_source_extension\run.ps1 -DryRun
Write-Output "DRYRUN_EXIT_CODE=$LASTEXITCODE"
```

After DryRun succeeds:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r6_source_extension\run.ps1
Write-Output "R3R6_EXIT_CODE=$LASTEXITCODE"
git status -sb
```

Normal execution applies an exact-content patch, verifies source ancestry in the public search context, and runs **focused pytest only**. Full pytest belongs at the final phase gate. A passing gate alone does not assert completed group proof or web rendering.

## Phase boundary

R3-R6 only connects source-verified universal facts and the general doubled relation. The prior group proof and named group root must still pass the canonical search. No new direct group GIVEN, no dedicated renderer, and no Phase 174 closeout are included.
