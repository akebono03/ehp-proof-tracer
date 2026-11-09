param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r40_adopted_db_zero_image_isolated.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R40 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R40_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r40_adopted_db_zero_image_isolated.audit
    if ($LASTEXITCODE -ne 0) { throw 'R40 isolated zero-image inference failed' }
    $Groups = @(
        @{Name='R40_STATIC'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_static.py'},
        @{Name='R40_RULE'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py'},
        @{Name='R40_REAL_AUDIT'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_audit.py'},
        @{Name='R40_GUARD'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_guard.py'},
        @{Name='R39_REAL_PROOF'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_proof.py'},
        @{Name='R6_HISTORICAL'; Path='phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py'},
        @{Name='R38_PUBLIC'; Path='phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_public.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R40_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R40 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R40_RUN=PASS'
    Write-Output 'PHASE174_R3R7R40_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
