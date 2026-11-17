# EHP Proof Tracer — Phase 175 R4R1 (Audit Only; pytest cache guard repair)

This package performs a **read-only, source-first** audit of the unfinished proof of $\pi_9^5$ (`n=5`, `k=4`). It does not add a mathematical rule, a `GIVEN` assertion, a dedicated proof, a dedicated Narrative, or a completed result. It does not modify any existing production file, test, or root project document.

## Reviewed baseline

- Repository: `akebono03/ehp-proof-tracer`, `develop`.
- Reviewed R3 handoff ancestor: `a1ce1558be6bab647c5d23d26047b9cce45d4e2e`.
- Current GitHub `develop` at preparation: `c77a26fdebe0eead67f1f7dad3a469aa446b134f` (two commits later, affecting the eight R3R12 display-package files).
- The mathematical source pins come from the existing Phase 175 R1/R2 audit packages. A local checkout must have the reviewed R3 ancestor and matching Git blobs. Only pending changes within `phase175_r3r12_hopf_conclusion/` and the exact tracked pytest cache file `.pytest_cache/v/cache/nodeids` are tolerated; unrelated tracked edits cause an error. The existing cache modification is recorded separately and never restored or erased.
- Existing related tests were reviewed: Phase 175 R1, R2 and R3R12, and Phase 174 R34 source checks.

## What the audit verifies

The existing Phase 175 R1 observer is run in **isolated subprocesses** for `pi_9^5` and its already completed input group `pi_8^4`. The target is expected to remain incomplete, with a cyclic-structure goal and two directed relation goals. Changed search results are reported as an error for review rather than silently promoted.

The source audit reuses the pinned Toda Chapter V transcription and R34 typed source checks. It checks the Proposition 5.8 source clause and separate proof discussion of the EHP exact sequence, (5.8), Proposition 2.5, the kernel image of $\eta_9$, and the quotient calculation. The target clause printed in Proposition 5.8 **is not treated as an independent root proof**.

A transcription issue is logged: the EHP display within the source proof prints $\pi_8^9$ in the position where the mathematical sequence requires $\pi_8^4$. No source text is modified automatically. The original book has not been independently checked against the adopted transcription.

## Windows PowerShell

Extract the ZIP into the root of your existing local checkout, preserving the included directory. Run the following from the repository root:

```powershell
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase175_R4R1_PYTEST_CACHE_GUARD_FIX.zip" -DestinationPath "." -Force
$script = ".\phase175_r4_pi95_audit\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "Phase 175 R4 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "Phase 175 R4 audit failed" }
git diff --check
git status -sb
```

Both commands run only the **focused** R4 contract tests and existing R34 source tests, with `-p no:cacheprovider` so pytest cannot rewrite its tracked cache during those runs. DryRun checks Git/source state but does not run proof searches. The normal run also invokes the actual group-search and Web observer for `n=5,k=4` and `n=4,k=4`. Use `-TimeoutSeconds 600` if an isolated search legitimately needs more time; a timeout never becomes a pass.

## Reports and gates

A new timestamped folder is created under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r4_pi95_audit\` (or the OS temporary directory when `LOCALAPPDATA` is unavailable). It contains `report.json`, `report.md`, and, for a normal run, `pi_9_5.log` and `pi_8_4.log`. No file is written into the tracked repository by the Python auditor.

- `PASS_R4_AUDIT_ONLY_DRYRUN`: source and Git guards passed; no proof search was attempted.
- `PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE`: the live target remains incomplete with three actual goals, the prior `pi_8^4` is completed/trusted, and source evidence was checked.
- Any changed source, state mismatch, worker error, or unexpected local tracked edit outside the two permitted paths fails closed. A previously modified `.pytest_cache/v/cache/nodeids` remains on disk and is recorded in `preflight.tracked_dirty_pytest_cache`; no Git restore, reset, commit or staging is performed. The JSON report identifies the issue.

The mathematical next step is to connect the *general* kernel/image, exactness and quotient inference rules to verified steps. This R4 ZIP intentionally **does not perform that implementation**. The full pytest suite remains reserved for the end of Phase 175.

## Package contents

`audit.py`, `run.ps1`, `tests/test_audit.py`, `__init__.py`, `README.md`, `AUDIT_PLAN_JA.md`, `TEST_RESULTS_JA.md`, and `CODE_FULL_JA.md`. `CODE_FULL_JA.md` contains complete source units, imports and tests; no code is elided.

## R4R1 repair: tracked pytest cache guard

The user's first Windows R4 DryRun reported **23 focused tests passed**, then failed before source verification with `R4_UNREVIEWED_TRACKED_CHANGES: ['.pytest_cache/v/cache/nodeids']`. This tracked cache is written by pytest and is unrelated to the mathematical proof. It is not a source pin. The old audit guard rejected it as an unreviewed source change.

The repair is deliberately narrow:

1. `run.ps1` passes `-p no:cacheprovider` to the focused pytest command, preventing future cache writes from this runner.
2. `audit.py::validate_dirty_paths()` additionally permits exactly `.pytest_cache/v/cache/nodeids`, while continuing to reject every other unrelated tracked path.
3. `audit.py::preflight()` separately records any such existing cache modification in `tracked_dirty_pytest_cache` and retains `tracked_dirty_allowed_r3r12` for the historical R3 display edits only.
4. `tests/test_audit.py` verifies the precise cache exception and continues to reject production files, arbitrary cache paths and similarly named files.

No R4 mathematical, group-observation, source, renderer or public API logic is changed. No earlier R3 files are modified. This new ZIP overwrites only the existing R4 audit package; the mathematical next phase remains out of scope.

Pure R4R1 audit-contract tests in the package development environment: **22 passed**. The full Windows R34 + R4 integration tests and the real audit must still be run in the user's checkout; do not describe them as passed until the actual logs confirm that. Full-suite pytest is not run.


## R4R2 repair: R3-reviewed source SHA instead of stale R1 SHA

The user's R4R1 Windows DryRun passed **29 focused tests** but stopped at `R4_SOURCE_PIN_DRIFT: phase165_r52_r9_shared_math.py` before inspecting the source or running group workers. This was a baseline transition, not evidence of a mathematical regression: the earlier Phase 175 R1 source pin was `9fa11b383812570fae1a26868c98992a5934a327` at the reviewed Phase 174 baseline, while the reviewed Phase 175 R3 handoff `a1ce1558be6bab647c5d23d26047b9cce45d4e2e` contains `ee1efa2d91df479168b7b964d24e814e0f516449`. The current GitHub `develop` also has the latter blob. All 17 other inherited R1/R2 source pins were checked and matched the current GitHub code.

`audit.py::reviewed_source_pins()` now merges the unchanged historical R1/R2 source list, requires its old R1 blob for this exact path, verifies the actual Git blob at the reviewed R3 handoff commit, and then adopts that one exact R3 blob for `HEAD:path` validation. Every other source remains pinned to its original SHA; arbitrary new SHAs still fail closed. `preflight()` reports the old/new digest and reviewed commit as `r3_reviewed_source_pin_transition`. No production code, Git metadata or tracked cache files are modified by the repair.

The package's focused contract tests were run locally: **24 passed**. The real Windows `run.ps1 -DryRun`, full read-only audit and existing R34 source tests still require the user's local checkout. This ZIP contains complete English README and Japanese audit/code/test documentation; its only changes relative to R4R1 are this audit package's Python preflight/pin helper, audit tests and documentation. The runner is unchanged and never invokes the full pytest suite.
