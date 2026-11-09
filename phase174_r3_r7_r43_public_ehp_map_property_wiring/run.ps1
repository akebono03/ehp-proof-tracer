param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r43_public_ehp_map_property_wiring.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R43 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R43_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r43_public_ehp_map_property_wiring.install
    if ($LASTEXITCODE -ne 0) { throw 'R43 guarded installation failed' }
    python -B -m phase174_r3_r7_r43_public_ehp_map_property_wiring.audit
    if ($LASTEXITCODE -ne 0) { throw 'R43 public EHP audit failed' }
    $Groups = @(
        @{Name='R43_STATIC'; Path='phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_static.py'},
        @{Name='R43_GUARD'; Path='phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_guard.py'},
        @{Name='R43_PUBLIC'; Path='phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_public.py'},
        @{Name='R41_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R37_UPPER_DELTA_REGRESSION'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'},
        @{Name='R5_HOPF_REGRESSION'; Path='phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py'},
        @{Name='R3_EHP_ROOT_REGRESSION'; Path='phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py'},
        @{Name='R40_RULE_REGRESSION'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R43_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R43 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R43_RUN=PASS'
    Write-Output 'PHASE174_R3R7R43_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
