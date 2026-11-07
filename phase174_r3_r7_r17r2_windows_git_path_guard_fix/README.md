# EHP Proof Tracer — Phase 174 R3-R7-R17R2

This focused recovery package corrects a Windows-only source-guard comparison in the previously extracted R17R1 audit script. Git reports changed paths with forward slashes, but the historical script built its expected paths with `str(Path)`, which uses backslashes on Windows. It rejected the two intended tracked changes even though both regression and public display tests passed.

The patch changes only the **untracked** `phase174_r3_r7_r17r1_historical_test_contract/audit.py`. It preserves the exact two-file allowlist and all existing hash, source, and proof checks. It requires the original R17 and R17R1 folders already extracted under the repository root, and the reviewed local/remote `develop` HEAD `388f63797a6aba61418bb93e734b8ce5999dc7f6`.

The wrapper checks the exact original audit-script SHA, the original R17R1 runner SHA, and the Git state before touching anything. It then invokes the original R17R1 `run.ps1` without weakening its tests. Only focused pytest tests are run. Mathematical inference rules, GIVEN statements, Verified Proof Tree, and common Narrative are unchanged. The root proof of `pi_12^7 = 0` remains incomplete.

Run in Windows PowerShell from the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase174_R3_R7_R17R2_WINDOWS_GIT_PATH_GUARD_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r17r2_windows_git_path_guard_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r17r2_windows_git_path_guard_fix\run.ps1"
```

On success the original R17R1 gate is `PASS_HISTORICAL_TEST_CONTRACT_CORRECTED_R17_PUBLIC_UNCHANGED` and the wrapper gate is `PASS_WINDOWS_GIT_PATH_GUARD_R17R1_FINAL`.

If the reviewed HEAD or either original package differs, the preflight fails rather than resetting, merging, or overwriting unknown code. Local backups are retained under `%LOCALAPPDATA%\EHPProofTracerAudit`. The wrapper restores its audit-script change on failure; the original R17R1 runner handles rollback of the two tracked changes.
