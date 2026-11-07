# Phase 174 R3-R7-R17R1 — Historical Test Contract Correction

This guarded recovery package addresses an obsolete Phase 173 test expectation: the `n=5, k=3` example (`pi_8^5`) is now proof-complete, whereas the historical test still expected a failed search with three pending goals. It preserves the pending-goal checks for `n=4, k=8` and `n=4, k=9`, and adds an explicit completed-proof regression for `pi_8^5`.

The package depends on the previously extracted `phase174_r3_r7_r17_typed_map_open_goal/` directory. It first executes the unchanged R17 source guards and its typed-map formatting patch, then corrects the historical test and executes the full corrected historical test file. It does not alter proof-search rules, given statements, or common narrative architecture. It does not run the full test suite.

From the `develop` repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase174_R3_R7_R17R1_HISTORICAL_TEST_CONTRACT_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r17r1_historical_test_contract\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r17r1_historical_test_contract\run.ps1"
```

Source guards require matching local and remote `develop` at reviewed HEAD `388f63797a6aba61418bb93e734b8ce5999dc7f6`, an unmodified historical test and formatter, and the exact previously reviewed R17 package bytes. The script does not fetch and merge new code, commit, reset or stash. Unexpected changes are rejected; backups are kept under `%LOCALAPPDATA%\EHPProofTracerAudit`.

Success gate: `PASS_HISTORICAL_TEST_CONTRACT_CORRECTED_R17_PUBLIC_UNCHANGED`.

The expected mathematical state remains **incomplete**: the public EHP zero-group root has one backward candidate, but Delta surjectivity has no certified inference candidate. The formatting correction does not assert any proof step.
