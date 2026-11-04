# Phase 173 R15R17-R2R1: Windows Path and HEAD Guard Fix

This package corrects two issues in the **execution and installation guards** of the previously released R15R17-R2 package. It does not alter the proposed proof renderer patch, proof search, proof tree, citations, or proof statuses.

The initial PowerShell runner compared Git's Windows-style forward-slash path (`C:/...`) to PowerShell's backslash path (`C:\\...`) as raw strings and incorrectly reported that the ZIP was not at the repository root. The revised runner uses `System.IO.Path.GetFullPath` on both paths and a case-insensitive comparison. It prints `R15R17R2_REPOSITORY_ROOT=PASS` when the paths resolve to the same directory.

GitHub `develop` also advanced to commit `11fdf0f5c52ce2de786e36c3a3d0abe7a0d0fa26`, which committed R15R17-R1. A comparison of the preceding commit to this revision showed that the R2 target `phase168_r3_5_model_renderer.py` was unchanged, at blob `6dd75099bb2c71fb9873477cb36c11bdb7dad410`. The install guard pins the new remote revision while retaining strict checks on branch, source blob, prior R1 installed-state hashes, and the Git index. The prior allowed local HEADs remain recognized.

Extract this archive at the repository root using `Expand-Archive -Force`. Its files overwrite only the package directory `phase173_r4_r15r17r2_unsupported_given_clean/`; it never overwrites the R1 implementation or project source. No `installed_state.json` or backup files are shipped. Run `run.ps1 -DryRun`, then `run.ps1` only after DryRun succeeds. The normal run will apply the existing R2 renderer change and execute focused pytest. Use `run.ps1 -Restore` to restore only that change after a successful installation.

Modified package files are `run.ps1`, `install.py`, `README.md`, and `design.md`; `tests/test_path_guard.py` is newly added. `FULL_CHANGED_UNITS.md` contains the complete post-fix scripts and test source. The original five patch contract tests and public narrative regression tests are retained without modification.

Neither invocation stages, commits, resets, or cleans repository content, and no full pytest suite is executed. Actual Windows PowerShell and repository-integrated proof tests must be run on the user's machine.
