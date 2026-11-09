# Phase 174 R3-R7-R43R3: Reviewed Git Index Recovery

This package corrects a local Git **index state**, not a mathematical rule or production file. The R43 package's twelve new files were staged (`git add`) before R43R2, which intentionally refuses any staged changes.

The preflight permits **only** the exact twelve new R43 files staged with status `A`, or the same twelve files already untracked. Any other staged change, unstaged tracked modification, missing file, changed branch, or changed local/remote Git HEAD is rejected.

The normal run performs `git restore --staged -- <the twelve exact paths>` to remove them from the index **without changing worktree files**, and then executes the existing R43R2 DryRun and normal run, which include R43R1, R43, and focused tests. It does not run the full pytest suite or use `git reset`, `git clean`, or `git restore --worktree`.

Install at the repository root; run `run.ps1 -DryRun` and then `run.ps1` from PowerShell. No production files are modified by this package. R43 production wiring is performed only by the previously supplied guarded installer after the index is recovered.
