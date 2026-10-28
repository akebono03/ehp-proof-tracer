# EHP Proof Tracer — Git Reflog Conflict Recovery R2B

This is the corrected, self-contained version of the R2 safety package. The user's **actual read-only R2 audit** reported three Dropbox conflict copies in `.git/logs/`, not in `.git/refs/`. The R2 `Quarantine` precondition listed two incorrect paths and would refuse that observed state. R2B changes the exact allowlist to the three real reflog paths and adds tests to prevent that discrepancy from recurring.

The default run is **read-only**. It prints the actual HEAD and each conflicted path and never edits the worktree or Git metadata. Quarantine is optional and requires an explicit `-Mode Quarantine -DropboxPaused` switch. The operator must actually pause Dropbox on **every syncing computer** and close VS Code and other Git clients beforehand; the switch acknowledges those manual steps, it cannot verify their completion.

## Run the read-only check

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_git_environment_r2b_reflog_only_quarantine.zip" -DestinationPath . -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_git_environment_r2b_reflog_only_quarantine\run.ps1"
```

## Quarantine, only after pausing Dropbox on all PCs and closing Git clients

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_git_environment_r2b_reflog_only_quarantine\run.ps1" -Mode Quarantine -DropboxPaused
git -c core.longpaths=true status -sb
git show-ref --verify refs/heads/develop
git show-ref --verify refs/remotes/origin/develop
```

Quarantine first copies the **entire `.git` directory**, the Git index, and all currently modified or staged tracked files to `%LOCALAPPDATA%\EHPProofTracerRecovery`, outside Dropbox. It verifies the index and conflict files using SHA-256 before moving **only these exact three files**:

- `.git/logs/HEAD (oomae-pc11 の競合コピー 2026-10-28)`
- `.git/logs/refs/heads/develop (oomae-pc11 の競合コピー 2026-10-28)`
- `.git/logs/refs/remotes/origin/develop (oomae-pc11 の競合コピー 2026-10-28)`

Any other conflict path, Git lock, unexpected HEAD branch, or a backup path in Dropbox is rejected. Post-check failure attempts to restore the moved copies. The tool **does not** run `git reset`, `git clean`, `git add`, or `git commit`; it does not delete the long R5D generated files, modify Python production sources, or run the full pytest suite.

Keep the backup directory even after success. Do not restart Dropbox syncing until confirming the Git status and recovery backup. This tool does not itself resolve the Windows path-length issue; for subsequent commits stage specific source files rather than the entire long generated `output/` tree.

Focused tests: `python -m pytest -q -p no:cacheprovider phase169_git_environment_r2b_reflog_only_quarantine/tests/test_recovery.py`.
