# Phase 175 R4R5R3R1 — Shared Finite-Cyclic Summand Order-Zero Rule (Head-Lineage Repair)

## Purpose

Connect the already isolated and verified R4R5R2 inference to the canonical shared backward-search provider. From an authenticated group presentation containing a finite-cyclic component `Z/m{g}`, the inference derives `m*g = 0` for that component. This works for a single finite-cyclic group, an ordinary direct sum, or nested direct sums. It is not specific to `eta_7`, `pi_8^4`, or `pi_9^5`.

The expansion is a **conditional proof proposal**. The canonical recursive search continues to resolve the entire source presentation as a verified earlier database result or a screened/previously proved source statement before applying the inference. No proof is reconstructed for an earlier database group, and no direct zero relation or target conclusion is registered as GIVEN.

## R4R5R3R1 head-lineage repair

The previous archive pinned the Git commit itself to `2789fb6297efaa35962695b95300063feb6e2ea2`, which rejected the subsequent legitimate `175-4-5` commit containing only the R4R5R2 audited package. The fixed guard permits only descendants of that reviewed base where every intervening tracked path is under `phase175_r4r5_eta7_annihilator_isolated/`. A non-descendant or changes anywhere else fail closed. The production function Git blob remains pinned to `ee1efa2d91df479168b7b964d24e814e0f516449`; the original isolated rule remains SHA256-pinned. No math, provider, or proof-engine behavior changes.

## Changed files and boundaries

- **Modified production file:** `phase165_r52_r9_shared_math.py`, **only** the whole function `shared_expansion_provider`. Its module-level import block and other functions are unchanged. The installer exports the full resulting function as `shared_expansion_provider_FULL.py` in the audit report directory. A pinned source blob and the exact AST function boundaries are checked before replacement.
- **Existing isolated rule:** `phase175_r4r5_eta7_annihilator_isolated/rule.py`, byte-for-byte unchanged from R4R5R2.
- **New public provider:** `phase175_r4r5r3_public_order_zero/provider.py`, containing `eligible_order_zero_sources` and `build_public_order_zero_provider`.
- **New installer:** `phase175_r4r5r3_public_order_zero/installer.py`, containing `git_blob`, `function_replacement`, `plan`, and `install`.
- **Updated audit:** `phase175_r4r5r3_public_order_zero/audit.py`, preserving the R4R5R2 audit boundary and proving conditional inference replay against authenticated prior DB parents.
- **Tests:** `tests/test_provider.py`, `tests/test_installer.py`, `tests/test_head_lineage.py`, and `tests/test_real_integration.py`.
- **Execution:** `run.ps1`; dry-run is read-only for production code, and the real run automatically restores the original production bytes if installation or focused integration tests fail.
- **Documentation:** complete `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, and `TEST_RESULTS_JA.md`.

Only **one existing general mathematical rule** is connected; there are **zero new mathematical rules** and **zero new GIVEN facts** in this revision. No renderer, source registry, group result, or database file is changed. The `pi_9^5` public proof remains incomplete pending the other EHP premises. No full pytest suite is executed before the end of Phase 175.

## Run from Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase175_R4R5R3R1_REVIEWED_HEAD_LINEAGE_FIX.zip" -DestinationPath '.' -Force
$script = '.\phase175_r4r5r3_public_order_zero\run.ps1'
$report = 'C:\Users\oomae\AppData\Local\EHPProofTracerAudit\phase175_r4r5_eta7_annihilator_isolated\20261117T071055_346099Z\report.json'
powershell -NoProfile -ExecutionPolicy Bypass -File $script -R4R5R2Report $report -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R4R5R3 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File $script -R4R5R2Report $report
if ($LASTEXITCODE -ne 0) { throw 'R4R5R3 install failed' }
git diff --check
git diff --stat
git status -sb
```

Expected gates: `PASS_R4R5R3_PUBLIC_PROVIDER_DRYRUN` and `PASS_R4R5R3_SHARED_PROVIDER_CONNECTED_NOT_COMPLETE`. Real integration tests run inside the audit after installation and must pass before the final success gate is written. The installed production bytes are rolled back by `run.ps1` if the audit fails. The audit report's generated full-function file is the complete replaceable unit for the changed production function.
