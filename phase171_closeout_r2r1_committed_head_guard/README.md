# Phase 171 Closeout R2R1 — Committed R1R1 HEAD guard correction

R2 incorrectly required the reviewed earlier Git HEAD and the R1R1 test to remain uncommitted. A normal reviewed follow-up commit, `3e74849bf90bc115c16503ddd46d49996baa0856`, contains the same five documents and the corrected R1R1 test, so that exact commit pin is no longer appropriate.

This package replaces only two previously reviewed audit files in the existing `phase171_closeout_r2_documentation_full_output/` directory. It validates original or already-corrected content hashes, the five reviewed document section hashes, the `develop` branch, and local `origin/develop` synchronization. The corrected R2 writer accepts only descendants of the reviewed base with commits restricted to R1/R1R1 audit paths, and checks the unchanged five document Git blobs and the reviewed R1R1 test bytes. It rejects unrelated source commits.

Extract at the existing worktree root. Run the wrapper `run.ps1 -DryRun` and then `run.ps1` to install and execute the corrected R2 writer. The normal run invokes only the original R2 focused pytest manifest, **not** the Phase 171 full test suite.

The script backs up and restores corrected audit files and all five documents if the corrected R2 run fails. It does not call Git add, commit, reset, checkout, pull, or push. The complete updated Python files and their tests are in `replacements/`; reports and backups go into `%LOCALAPPDATA%/EHPProofTracerRecovery`.
