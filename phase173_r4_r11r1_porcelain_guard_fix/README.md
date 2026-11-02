# EHP Proof Tracer — Phase 173 R4-R11R1 Installer Guard Fix

This package fixes one comparison in the existing R4-R11 installer. Its `git()` helper applies `.strip()` to the Git porcelain output, so the one-file unstaged state is returned as `M phase165_r55_nk_only_goal.py` instead of ` M phase165_r55_nk_only_goal.py`. The original `preflight()` therefore rejected the edit it had just installed.

## Changed files and functions

The sole existing file change is to `phase173_r4_r11_zero_public_connection/install.py`, function `preflight()` (one character in one condition). The complete replacement module, including all imports and unmodified functions, is `replacement_install.py.txt`. The fix also adds `repair.py` with the full functions `git`, `checked_tracked_status`, `prepared_replacement`, `preflight`, `apply_fix`, and `main`; new `tests/test_repair.py`, `run.ps1`, and documentation. No mathematical rule, group-proof engine, or renderer is edited.

## Source protection

The local and remote `develop` HEAD must both be `de390132fcdcb52d2d5c16d2259f2b1073f09ad9`. The only tracked change must be the exact previously installed R4-R11 production function, with an empty Git index. The repair checks original package files, the unchanged source blobs and R4-R10 core. Other tracked changes or unreviewed code cause an immediate failure; no reset, pull, commit, or push is performed.

The `-DryRun` validates without modifying files. The regular run repairs only the installer, then invokes the original R4-R11 runner for actual public Group query, Web trust boundary, and focused regression checks. Public completion must be established by that rerun, not inferred from the previous eight isolated tests.
