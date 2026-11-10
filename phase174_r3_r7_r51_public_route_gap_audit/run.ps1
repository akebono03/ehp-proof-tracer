param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r51_public_route_gap_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R51 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R51_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r51_public_route_gap_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R51 public route audit failed' }
    $Groups = @(
        @{Name='R51_STATIC'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_static.py'; Mode='importlib'},
        @{Name='R51_GUARD'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_guard.py'; Mode='importlib'},
        @{Name='R51_PUBLIC'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py'; Mode='importlib'},
        @{Name='R50_SCOPED_PROOF_REGRESSION'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_frontier.py'; Mode='importlib'},
        @{Name='R35_KERNEL_MATH_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'; Mode='importlib'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R51_TEST_GROUP=' + $Group.Name)
        $Mode = $Group.Mode
        python -B -m pytest -q "--import-mode=$Mode" -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R51 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R51_RUN=PASS'
    Write-Output 'PHASE174_R3R7R51_PRODUCTION_FILES_CHANGED=0'
    Write-Output 'PHASE174_R3R7R51_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
