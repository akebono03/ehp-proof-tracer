param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    if ($DryRun) {
        python -B -m phase174_r3_r7_r35_isolated_cyclic_delta_kernel.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R35 Source Guard / DryRun failed' }
        Write-Output 'PHASE174_R3R7R35_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r35_isolated_cyclic_delta_kernel.audit
    if ($LASTEXITCODE -ne 0) { throw 'R35 Source Guard / audit failed' }
    $Groups = @(
        @{Name='R35_STATIC'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_static_contract.py'},
        @{Name='R35_RULE'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'},
        @{Name='R35_AUDIT'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_audit.py'},
        @{Name='R34_PRIOR_SOURCE'; Path='phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py'},
        @{Name='R34_PUBLIC'; Path='phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_public.py'},
        @{Name='R32_KERNEL_CONTRACT'; Path='phase174_r3_r7_r32_lower_delta_kernel_audit/tests/test_kernel_contract.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R35_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R35 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R35_RUN=PASS'
    Write-Output 'PHASE174_R3R7R35_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
