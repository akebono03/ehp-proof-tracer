param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r46_prop42_dfs_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R46 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R46_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r46_prop42_dfs_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R46 cited exactness/DFS audit failed' }
    $Groups = @(
        @{Name='R46_STATIC'; Path='phase174_r3_r7_r46_prop42_dfs_audit/tests/test_static.py'; ImportMode='importlib'},
        @{Name='R46_GUARD'; Path='phase174_r3_r7_r46_prop42_dfs_audit/tests/test_guard.py'; ImportMode='importlib'},
        @{Name='R46_FRONTIER'; Path='phase174_r3_r7_r46_prop42_dfs_audit/tests/test_audit.py'; ImportMode='importlib'},
        @{Name='R45_FRONTIER_REGRESSION'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_frontier.py'; ImportMode='importlib'},
        @{Name='PROP42_SPECIALIZATION_REGRESSION'; Path='phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'; ImportMode='prepend'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R46_TEST_GROUP=' + $Group.Name)
        $ImportMode = $Group.ImportMode
        python -B -m pytest -q "--import-mode=$ImportMode" -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R46 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R46_RUN=PASS'
    Write-Output 'PHASE174_R3R7R46_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
