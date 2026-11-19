# Phase 175 R4R14R5 — Source-bound composite zero transport

This package connects the previously isolated R4R14R4 generic zero-transport inference to the common backward proof provider. It introduces no new mathematical GIVEN, target-specific theorem, or renderer.

The provider requires a screened Toda (5.9) general source, matches the whole typed lifted composite against its general-law specialization, and asks the existing proof search to prove both the generator image and the cited zero relation. It does **not** claim completion of any root group.

## Execution

Extract this ZIP into the repository root on the `develop` branch. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r14r5_public_zero_transport\run.ps1 -DryRun` and then run the same command without `-DryRun`.

The guarded installer changes only the `shared_expansion_provider()` function in `phase165_r52_r9_shared_math.py`. It checks the reviewed Git blob and the worktree before writing and generates `SHARED_PROVIDER_FULL_JA.md` with the complete revised function. After the focused tests, `audit.py` performs an actual target search and records the observed status and Open Goals; it does not assert completion. Focused pytest uses `--import-mode=importlib` and disables the tracked pytest cache provider.

If a gate fails, do not treat the target proof as complete. Full-suite pytest is reserved for the end of Phase 175.
