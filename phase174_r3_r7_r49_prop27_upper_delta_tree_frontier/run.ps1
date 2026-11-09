param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r49_prop27_upper_delta_tree_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R49 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R49_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r49_prop27_upper_delta_tree_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R49 integrated Prop27 audit failed' }
    $Groups = @(
        @{ Name='R49_STATIC'; Path='phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/tests/test_static.py'; Mode='importlib' },
        @{ Name='R49_GUARD'; Path='phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/tests/test_guard.py'; Mode='importlib' },
        @{ Name='R49_FRONTIER'; Path='phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/tests/test_frontier.py'; Mode='importlib' },
        @{ Name='R48_FRONTIER_REGRESSION'; Path='phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_frontier.py'; Mode='importlib' },
        @{ Name='R30_PROP27_REGRESSION'; Path='phase174_r3_r7_r30_prop27_public_provider_wiring/tests/test_wiring.py'; Mode='importlib' },
        @{ Name='R29_PROP27_REGRESSION'; Path='phase174_r3_r7_r29_prop27_canonical_provider/tests/test_provider.py'; Mode='importlib' },
        @{ Name='R37_UPPER_DELTA_REGRESSION'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'; Mode='importlib' }
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R49_TEST_GROUP=' + $Group.Name)
        $Mode = $Group.Mode
        if ($Group.Name -eq 'R30_PROP27_REGRESSION') {
            # R30's historical HEAD-guard test belongs to its original phase;
            # R49 rechecks current develop with its own independently pinned guard.
            python -B -m pytest -q "--import-mode=$Mode" -p no:cacheprovider `
              -k 'not test_source_guard_accepts_reviewed_change' $Group.Path
        } else {
            python -B -m pytest -q "--import-mode=$Mode" -p no:cacheprovider $Group.Path
        }
        if ($LASTEXITCODE -ne 0) { throw ('R49 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R49_RUN=PASS'
    Write-Output 'PHASE174_R3R7R49_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
