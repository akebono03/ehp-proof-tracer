param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r39_verified_zero_image_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R39 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R39_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r39_verified_zero_image_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R39 verified frontier audit failed' }
    $Groups = @(
        @{Name='R39_STATIC'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_static.py'},
        @{Name='R39_GUARD'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_guard.py'},
        @{Name='R39_REAL_PROOF'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_proof.py'},
        @{Name='R38_PUBLIC'; Path='phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R14_SOURCE'; Path='phase174_r3_r7_r14_public_annihilator_connection/tests/test_public.py'},
        @{Name='R6_CYCLIC'; Path='phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py'},
        @{Name='R7_COMPOSITE'; Path='phase174_r3_r7_r7_composite_zero_audit/tests/test_rule.py'},
        @{Name='R9_ASSOCIATIVITY'; Path='phase174_r3_r7_r9_composition_associativity/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R39_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R39 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R39_RUN=PASS'
    Write-Output 'PHASE174_R3R7R39_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
