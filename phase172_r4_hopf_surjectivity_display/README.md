# EHP Proof Tracer — Phase 172 R4

This is a guarded, presentation-only update to remove repeated Hopf surjectivity prose in an already verified complete proof. The mathematical proof, original proof steps, literature citations, and search rules are unchanged.

## Installation

Extract the ZIP into the repository root and run these commands in Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r4_hopf_surjectivity_display\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r4_hopf_surjectivity_display\run.ps1" -RunFocusedTests
```

DryRun creates the complete new renderer function and full proposed source in a timestamped directory under `%LOCALAPPDATA%\EHPProofTracerRecovery`; it changes no existing production source.

The installer reconstructs the verified R3 renderer from the committed R2 Git blob and the exact R3 transformation. It accepts either a committed or an uncommitted R3 worktree when its content matches that reconstructed source. Unknown source content is rejected.

On any test failure, the installer restores the prior renderer bytes. It runs **focused tests only**; do not run the full test suite until Phase 172 closeout. R4 changes the common renderer function, not any mathematical inference or proof storage.

## Files

- `projection.py`: verify the two surjectivity statements denote the identical typed Hopf map and the later claim comes from an exactness path through the earlier claim.
- `tests/test_projection.py`: live proof and fail-closed regression tests.
- `install.py`, `run.ps1`: preflight, full-function export, focused pytest and rollback.
- `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`: Japanese change and code documentation.
