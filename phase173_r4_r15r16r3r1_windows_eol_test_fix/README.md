# Phase 173 R4-R15R16R3R1 — Windows EOL Test Correction

This archive corrects one platform-sensitive test assertion in the previously extracted R15R16R3 package. It does **not** change production Python code, proof search, verified proof trees, the common narrative renderer, or the Git index.

The existing installer correctly preserves the source file's line ending convention. The prior regression test incorrectly expected a literal LF byte in a newly appended line on Windows. The corrected test checks for CRLF when the original file contains CRLF and LF otherwise.

## Use

From the repository root, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r15r16r3r1_windows_eol_test_fix\run.ps1 -DryRun`, then repeat without `-DryRun`. The original `phase173_r4_r15r16r3_staged_guard_fix` folder must already exist.

The new runner verifies Git lineage, preserves staged changes, runs eleven isolated tests, installs only the corrected test, and invokes the prior R15R16R3 runner to execute its normal DryRun and focused tests. If the original runner fails, the corrected test is restored to its reviewed baseline. No full pytest run is performed.

See `FULL_CHANGED_UNITS.md` and `SOURCE_CODE.md` for complete imports, tests, and scripts. Restore only the test with `python -m phase173_r4_r15r16r3r1_windows_eol_test_fix.install --restore` when needed before committing.
