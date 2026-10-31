# Phase 172 R3R2 — R2 Regression Test Contract Correction

This guarded package repairs one outdated assertion in an existing Phase 172 R2 integration test after the verified Phase 172 R3 Hopf-display projection was introduced.

The earlier assertion required the intermediate equality `nu' eta_6 = nu' E eta_5` to appear in the public proof. That assertion was valid for R2 alone but is no longer a required presentation invariant under R3. The test now checks that Proposition 2.2 and equation (5.3) remain in the Reference section, while continuing to verify the cited suspension source, hidden duplicate suspension equalities, retained final Hopf identity, order-four conclusion, and eight citations.

## Prerequisites

- A clean `develop` worktree with the committed Phase 172 R2 Renderer and R2 test baseline.
- The unchanged directory `phase172_r3_hopf_chain_display/` from `EHP_Phase172_R3_VERIFIED_HOPF_DISPLAY.zip` already unpacked at the repository root.
- Python 3.10 or later, pytest, Git, and PowerShell.
- No simultaneous worktree mutations while the guarded runner is active.

## Run

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase172_R3R2_R2_TEST_CONTRACT_CORRECTION.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r3r2_r2_test_contract_correction\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r3r2_r2_test_contract_correction\run.ps1" -RunFocusedTests
git status -sb
git diff --stat
```

Dry run validates immutable inputs without altering the repository and exports the entire updated test function and test file under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r3r2_*`.

The apply step checks Git blobs, package digests, worktree cleanliness, and remote alignment when available. It runs six isolated guard unit tests, then invokes the **original Phase 172 R3 installer**, which applies the presentation-only Renderer update and runs its five existing focused pytest groups. Only the following tracked files can remain modified on success:

- `phase172_r2_suspension_relation_display/tests/test_projection.py`
- `phase168_r3_5_model_renderer.py`

If a test or guard fails during application, both tracked files are restored from backups. No changes are made to proof inference, ProofSteps, citation records, database data, or mathematical source material.

## Completion gate

Require `PHASE172_R3R2_RESULT=PASS_R3R2_AND_R3`, all five `PHASE172_R3_FOCUSED_*` groups PASS, and `PHASE172_R3_RESULT=PASS_R3_HOPF_DISPLAY_ONLY`. No full suite is run; it is reserved for Phase 172 closeout.
