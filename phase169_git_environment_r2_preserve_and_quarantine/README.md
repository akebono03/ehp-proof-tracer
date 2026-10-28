# EHP Proof Tracer — Git Conflict Copy Recovery

This bundle is an **environment repair tool**, not a change to mathematical proof implementation.

The default `run.ps1` invocation is read-only. It identifies the three exact Dropbox conflict-copy files inside `.git` and validates the real `develop` branch. It does not edit Git or the worktree.

The optional `-Mode Quarantine -DropboxPaused` operation requires the operator to close editors and Git clients, and pause Dropbox synchronization **on all computers sharing this folder**. It copies the **entire `.git` directory** and the modified/staged tracked worktree files into `%LOCALAPPDATA%\EHPProofTracerRecovery\...` outside Dropbox. The three pre-reviewed conflict-copy files are moved to the recovery folder only after byte-for-byte backup verification; valid refs, HEAD, index, and production sources are untouched. A failed post-check attempts rollback of moved files.

## Usage

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_git_environment_r2_preserve_and_quarantine.zip" -DestinationPath . -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_git_environment_r2_preserve_and_quarantine\run.ps1"
```

After reviewing the reported exact paths, **stop Dropbox on all participating PCs**, close VS Code and other Git clients, and run the explicitly opted-in quarantine:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_git_environment_r2_preserve_and_quarantine\run.ps1" -Mode Quarantine -DropboxPaused
```

The tool refuses other conflict filenames, active Git locks, non-`develop` HEAD, output under Dropbox, or a nonidentical backup. Keep the recovery folder. Do not run `git reset --hard`, `git clean -fd`, or delete `.git`.

Afterwards inspect `git -c core.longpaths=true status -sb`. The 273-character R5D audit output was **not** deleted or renamed. To avoid future `git add -A` failures, use targeted staging and consider an exclusion for generated `output/` only after examining existing Git tracking. Full pytest is not run.
