param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R48 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R48_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R48 integrated kernel audit failed' }
    $Groups = @(
        @{Name='R48_STATIC'; Path='phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_static.py'; Mode='importlib'},
        @{Name='R48_GUARD'; Path='phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_guard.py'; Mode='importlib'},
        @{Name='R48_FRONTIER'; Path='phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_frontier.py'; Mode='importlib'},
        @{Name='R47_FRONTIER_REGRESSION'; Path='phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/tests/test_frontier.py'; Mode='importlib'},
        @{Name='R36_CITED_KERNEL_REGRESSION'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_public.py'; Mode='importlib'},
        @{Name='R35_GENERIC_KERNEL_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'; Mode='importlib'},
        @{Name='R34_PRIOR_SOURCE_REGRESSION'; Path='phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_public.py'; Mode='importlib'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R48_TEST_GROUP=' + $Group.Name)
        $ImportMode = $Group.Mode
        python -B -m pytest -q "--import-mode=$ImportMode" -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R48 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R48_RUN=PASS'
    Write-Output 'PHASE174_R3R7R48_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
