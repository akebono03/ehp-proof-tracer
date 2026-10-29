# Phase 170 R3-R6 — Source-checked Proposition 5.8 transport premise

This package aims to complete a genuine proof of `pi_7^2` using the existing generalized Toda (5.2) route. The source group `pi_7^3 = Z/2{nu' eta_6}` is printed in Toda Proposition 5.8, but the shared typed registry currently exposes its clause only as component metadata. The patch checks the adopted TeX archive identity and a unique printed clause, compares the source's concrete typed generator with `HyoujiGen.csv`, and replaces exactly one existing Proposition 5.8 metadata assertion with a typed fixed assertion. It does **not** turn database rows or saved proofs into GIVEN premises.

## Changes

- Existing file: `phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py`. Replace its full import section and the entire `connect_explicit_literature_components()` function. The entire replacement file is supplied under `replacement/phase168_r2_7_4_literature_connection.py`.
- New file: `phase170_r3_r6_prop58_source.py`, placed at the repository root. Contains `SOURCE_ID`, `SOURCE_DIGEST`, `COMPONENT_ID`, `SOURCE_CLAUSE`, `_source_checked_pi73_relation()`, and `register_source_checked_prop58_pi73()` in full.
- New tests: `tests/test_phase170_r3_r6_source.py` and `tests/test_offline_contract.py`. All imports and test functions are supplied in full.
- New installer: `runner.py`, `verify.py`, and `run.ps1` in this package.

No changes to `phase168_r2_toda52_transport.py`, DB files, Web renderer, or Trust Boundary verification code are made. The successfully committed R3-R5 update to Toda (5.2) at reviewed `develop` HEAD `970535190e160e9f2ae9e596a3ccb13abb9c913c` is a **required prerequisite** and will be preserved after rollback. Only the typed source clause for `pi_7^3` is newly admitted; the other Proposition 5.8 components remain metadata-only.

## Windows execution

Extract the ZIP at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r6_prop58_pi73_source\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r6_prop58_pi73_source\run.ps1"
git status -sb
```

The runner checks exact known Git HEAD, existing committed source blob, the committed R3-R5 Git blob and its exact working-file SHA-256, and clean staged/unstaged status before touching files. It runs only focused pytest modules and a genuine public Web trust-gated narrative check for `pi_5^2` and `pi_7^2`.

If tests or the live Web check fail, it restores the original literature connection module and deletes the new source module, leaving the committed R3-R5 implementation intact. Logs and pre-edit backups are saved to `%LOCALAPPDATA%\EHPProofTracerRecovery` outside the repository.

## Acceptance and limits

Accept only `PHASE170_R3R6_RESULT=PATCHED_AND_WEB_VERIFIED`, `PHASE170_R3R6_pi_7^2=COMPLETE_AND_WEB_VERIFIED`, zero unresolved goals and successful focused pytest. This patch does not prove `pi_6^2`, `pi_8^2`, higher groups, zero groups or direct sums. Full pytest is deferred to phase closeout.

## R3-R6 HEAD sync correction (2026-10-29)

The original installer only accepted Git HEAD `32377a9fa4dde75ee0366c7460287354a137536f` with an **uncommitted** R3-R5 file. The current reviewed GitHub `develop` is `970535190e160e9f2ae9e596a3ccb13abb9c913c`, incorporating exactly the successful R3-R5 committed file and its associated package. The old guard therefore refused correctly but unnecessarily. This replacement package changes **only** the R3-R6 runner's preflight and matching package documentation/tests; the Proposition 5.8 mathematical registration, existing production replacement, verified Web check, and rollback are byte-for-byte unchanged. The runner now demands the exact reviewed committed HEAD, the exact committed R3-R5 Git blob, its SHA-256, the unchanged source-registration blob, and a clean Git index/worktree. Never reset or checkout to the earlier HEAD.

This package replaces the already-unpacked `phase170_r3_r6_prop58_pi73_source/` folder. Run the existing `run.ps1 -DryRun` first, followed by `run.ps1` if it passes. Production source is changed only by a successful full run, and only if both `pi_5^2` and `pi_7^2` are verified. This package still does not run full pytest.
