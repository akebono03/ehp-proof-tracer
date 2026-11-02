# Phase 173 R4-R1: Guarded pytest Cache Correction

This package corrects a **read-only audit preflight**, not a production proof rule. The reported Git status had exactly one unstaged modification: `.pytest_cache/v/cache/nodeids`. That file is a pytest cache artifact. The existing R4-R1 audit rejected all tracked modifications, so the runtime audit did not run even though its focused tests passed.

The corrected `git()` preserves the leading porcelain status characters, and `verify_tracked_worktree()` allows **only** the exact unstaged ` M .pytest_cache/v/cache/nodeids` record. Every other staged or unstaged modification is rejected, and the existing reviewed production source blob checks remain intact. The focused test runner disables pytest's cache provider to avoid further cache changes. This correction does **not** remove, restore, or stage any tracked file, and it does not create mathematical GIVEN statements or ProofSteps.

## Files

- `install.py`, `manifest.py`, `run.ps1`: guarded package installer and local runner.
- `tests/test_install.py`: installer-focused checks.
- `payload/phase173_r4_r1_audit_only/audit.py`: complete corrected audit module.
- `payload/phase173_r4_r1_audit_only/tests/test_audit.py`: complete corrected focused tests.
- `payload/phase173_r4_r1_audit_only/run.ps1`: corrected original runner.
- `CODE_FULL_JA.md`, `AUDIT_PLAN_JA.md`: complete Japanese change information.

Only these **three untracked R4-R1 audit files** are replaced, and only if all three match the shipped original SHA-256 hashes. The installer backs them up under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r4_r1_cache_guard_fix\backups`. Unknown local modifications cause a stop, without overwriting them. Repeated installation after success is idempotent.

## Run

Extract to the `ehp_proof` repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_cache_guard_fix\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_cache_guard_fix\run.ps1'
```

`-DryRun` runs only correction-focused tests and the SHA-256 installation preflight, with no installation. A normal run installs the corrected untracked audit files, runs the R4-R1 focused tests and source dry-run, then runs the read-only R4-R1 public-root inspection. It does not run the full test suite.

Audit JSON: `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r4_r1_audit_only\audit.json`.

**This is a narrow, reviewed cache exemption, not a general dirty-worktree bypass.** The output must accurately show `TRACKED_UNCHANGED=False` when the cache remains dirty and `REVIEWED_SOURCE_UNCHANGED=True` when all reviewed source files pass.
