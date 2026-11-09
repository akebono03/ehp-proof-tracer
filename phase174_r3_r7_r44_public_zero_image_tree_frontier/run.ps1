param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r44_public_zero_image_tree_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R44 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R44_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r44_public_zero_image_tree_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R44 canonical frontier audit failed' }
    $Groups = @(
        @{Name='R44_STATIC'; Path='phase174_r3_r7_r44_public_zero_image_tree_frontier/tests/test_static.py'},
        @{Name='R44_GUARD'; Path='phase174_r3_r7_r44_public_zero_image_tree_frontier/tests/test_source_guard.py'},
        @{Name='R44_FRONTIER'; Path='phase174_r3_r7_r44_public_zero_image_tree_frontier/tests/test_frontier.py'},
        @{Name='R43_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_public.py'},
        @{Name='R41_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_public.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R44_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R44 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R44_RUN=PASS'
    Write-Output 'PHASE174_R3R7R44_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
