# Phase 171 R2H-R1 — CRLF-aware installer preflight repair

This narrowly scoped repair fixes a false "unreviewed changes" rejection in the previously distributed Phase 171 R2H installer. The reviewed Git blob `phase165_r52_r9_shared_math.py` contains CRLF line endings, while the old installer normalized CRLF to LF **before comparing its hash with the original Git blob SHA**. Unmodified files were therefore rejected.

The repaired `status()` method verifies the precise committed Git blob SHA, reads the HEAD blob bytes, and compares checkout text after *only* CRLF/LF normalization. Both a legitimate unmodified checkout and the **exactly** expected R2H patch are accepted; arbitrary file edits and unexpected committed baselines are still rejected. The existing R2H package's mathematical code, citation verification, inference rules, and tests apart from the installer's specific regression tests remain unchanged.

## Scope

The guarded repair changes only:

- `phase171_r2h_prop22_cited_hopf/install.py`: complete `status()` function, with unchanged imports and other functions.
- `phase171_r2h_prop22_cited_hopf/tests/test_install.py`: five additional complete regression tests and one test fixture, appended after existing tests. Existing tests and imports are preserved.

This repair package also provides `repair.py`, `run.ps1`, self-contained baseline fixtures, and its own focused tests. No repository-wide test suite or history-changing Git command is used.

## Execute from the repository root in PowerShell

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2H_R1_CRLF_FIX.zip" -DestinationPath "."
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2h_r1_crlf_baseline_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2h_r1_crlf_baseline_fix\run.ps1"
git status -sb
git diff --stat
```

The DryRun is strictly read-only. The real run first verifies exact SHA-256 hashes of the original R2H installer/test, saves copies under `%LOCALAPPDATA%\EHPProofTracerRecovery`, and applies the repair. It then runs repair-focused pytest, the original R2H DryRun, and the original R2H runner with its focused pytest and mathematical proof audit.

R2H succeeds only if the previous package's cited Proposition 2.2 two-inference Proof Tree passes. It does **not** establish the group structure of `pi_6^3`, and it does not use an unrelated Proposition 5.6 result as a given.
