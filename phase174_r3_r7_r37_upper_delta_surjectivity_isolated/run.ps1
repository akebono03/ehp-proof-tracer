param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r37_upper_delta_surjectivity_isolated.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R37 Source Guard / DryRun failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R37_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r37_upper_delta_surjectivity_isolated.audit
    if ($LASTEXITCODE -ne 0) { throw 'R37 isolated mathematical audit failed' }
    $Groups = @(
        @{Name='R37_STATIC'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_static.py'},
        @{Name='R37_GENERAL_RULE'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'},
        @{Name='R37_SOURCE_AUDIT'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_audit.py'},
        @{Name='R36_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_public.py'},
        @{Name='R36_CONTEXT_REGRESSION'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_context.py'},
        @{Name='R35_KERNEL_RULE_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'},
        @{Name='R5_HOPF_INJECTIVITY_REGRESSION'; Path='phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R37_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R37 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R37_RUN=PASS'
    Write-Output 'PHASE174_R3R7R37_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
