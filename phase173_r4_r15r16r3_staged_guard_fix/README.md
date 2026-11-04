# Phase 173 R4-R15R16R3: Staging-safe installer

This ZIP replaces the failed R15R16R2 installer without changing its
mathematical or narrative patch. It uses the same shared renderer and tree
adapter, with staging-aware preflight checks. It never invokes git reset,
git add, git restore --staged, git checkout, or git commit.

Reviewed baseline: 92f967c079f4a66e19a598e0acc54b742f11df9c.

On a staged reviewed source file, the index must match the reviewed R15R16
worktree. After installation, the index may still hold the original R15R16
bytes, and the working tree contains R15R16R3. This is allowed on re-run and
rollback. No index data is changed.

Run in PowerShell from the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_R4_R15R16R3_STAGE_SAFE_GUARD.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r16r3_staged_guard_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r16r3_staged_guard_fix\run.ps1"
git status -sb
git diff --stat
git diff --cached --stat
```

DryRun runs only isolated contract tests. The normal command installs exactly
the reviewed source change and runs focused tests; it does not run all pytest
at this stage of Phase 173.
