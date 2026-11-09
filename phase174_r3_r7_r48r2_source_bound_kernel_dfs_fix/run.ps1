param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r48r2_source_bound_kernel_dfs_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R48R2 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R48R2_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r48r2_source_bound_kernel_dfs_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R48R2 guarded patch failed' }
    powershell -NoProfile -ExecutionPolicy Bypass `
      -File '.\phase174_r3_r7_r48_cited_lower_kernel_tree_frontier\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R48 integrated audit or focused pytest failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
      'phase174_r3_r7_r48r2_source_bound_kernel_dfs_fix/tests/test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R48R2 patch regression failed' }
    Write-Output 'PHASE174_R3R7R48R2_RUN=PASS'
    Write-Output 'PHASE174_R3R7R48R2_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
