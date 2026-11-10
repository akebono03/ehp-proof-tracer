param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r52_public_kernel_source_bound_probe.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R52 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R52_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r52_public_kernel_source_bound_probe.audit
    if ($LASTEXITCODE -ne 0) { throw 'R52 probe audit failed' }
    $Groups = @(
        @{Name='R52_STATIC'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_static.py'},
        @{Name='R52_GUARD'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_guard.py'},
        @{Name='R52_PROBE'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py'},
        @{Name='R51_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py'},
        @{Name='R50_SCOPED_PROOF_REGRESSION'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_frontier.py'},
        @{Name='R35_KERNEL_MATH_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R52_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R52 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R52_RUN=PASS'
    Write-Output 'PHASE174_R3R7R52_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
