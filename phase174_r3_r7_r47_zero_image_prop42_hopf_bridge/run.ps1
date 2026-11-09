param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r47_zero_image_prop42_hopf_bridge.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R47 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R47_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r47_zero_image_prop42_hopf_bridge.audit
    if ($LASTEXITCODE -ne 0) { throw 'R47 integrated canonical EHP audit failed' }
    $Groups = @(
        @{Name='R47_STATIC'; Path='phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/tests/test_static.py'; ImportMode='importlib'},
        @{Name='R47_GUARD'; Path='phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/tests/test_guard.py'; ImportMode='importlib'},
        @{Name='R47_FRONTIER'; Path='phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/tests/test_frontier.py'; ImportMode='importlib'},
        @{Name='R44_ZERO_IMAGE_REGRESSION'; Path='phase174_r3_r7_r44_public_zero_image_tree_frontier/tests/test_frontier.py'; ImportMode='importlib'},
        @{Name='R46_EXACTNESS_REGRESSION'; Path='phase174_r3_r7_r46_prop42_dfs_audit/tests/test_audit.py'; ImportMode='importlib'},
        @{Name='R5_HOPF_REGRESSION'; Path='phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py'; ImportMode='importlib'},
        @{Name='PROP42_SPECIALIZATION_REGRESSION'; Path='phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'; ImportMode='prepend'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R47_TEST_GROUP=' + $Group.Name)
        $ImportMode = $Group.ImportMode
        python -B -m pytest -q "--import-mode=$ImportMode" -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R47 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R47_RUN=PASS'
    Write-Output 'PHASE174_R3R7R47_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
