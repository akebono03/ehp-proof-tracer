param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r46r1_source_guard_merge_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R46R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R46R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r46r1_source_guard_merge_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R46R1 guarded repair failed' }
    powershell -NoProfile -ExecutionPolicy Bypass `
      -File '.\phase174_r3_r7_r46_prop42_dfs_audit\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R46 cited Prop42 DFS audit failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
      'phase174_r3_r7_r46r1_source_guard_merge_fix/tests/test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R46R1 guard regression tests failed' }
    Write-Output 'PHASE174_R3R7R46R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R46R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
