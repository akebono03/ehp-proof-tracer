param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R41 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R41_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.install
    if ($LASTEXITCODE -ne 0) { throw 'R41 guarded public connection installation failed' }
    python -B -m phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.audit
    if ($LASTEXITCODE -ne 0) { throw 'R41 public source and candidate audit failed' }
    $Groups = @(
        @{Name='R41_STATIC'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_static.py'},
        @{Name='R41_GUARD'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_source_guard.py'},
        @{Name='R41_PUBLIC'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R40_RULE_REGRESSION'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py'},
        @{Name='R40_PROOF_REGRESSION'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_audit.py'},
        @{Name='R39_PROOF_REGRESSION'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_proof.py'},
        @{Name='R38_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R6_CYCLIC_REGRESSION'; Path='phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R41_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R41 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R41_RUN=PASS'
    Write-Output 'PHASE174_R3R7R41_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
