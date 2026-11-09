param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r45_ehp_open_obligation_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R45 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R45_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r45_ehp_open_obligation_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R45 EHP frontier audit failed' }
    $Groups = @(
        @{Name='R45_STATIC'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py'},
        @{Name='R45_GUARD'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_source_guard.py'},
        @{Name='R45_FRONTIER'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_frontier.py'},
        @{Name='PROP42_SPECIALIZATION_REGRESSION'; Path='phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'},
        @{Name='PROP42_CONSEQUENCE_REGRESSION'; Path='phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py'},
        @{Name='R5_HOPF_REGRESSION'; Path='phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py'},
        @{Name='R37_DELTA_REGRESSION'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R45_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R45 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R45_RUN=PASS'
    Write-Output 'PHASE174_R3R7R45_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
