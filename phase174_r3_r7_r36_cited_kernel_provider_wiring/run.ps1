param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r36_cited_kernel_provider_wiring.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R36 Source Guard failed' }
    python -B -m phase174_r3_r7_r36_cited_kernel_provider_wiring.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R36 Source Audit DryRun failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R36_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r36_cited_kernel_provider_wiring.install
    if ($LASTEXITCODE -ne 0) { throw 'R36 installation failed' }
    python -B -m phase174_r3_r7_r36_cited_kernel_provider_wiring.audit
    if ($LASTEXITCODE -ne 0) { throw 'R36 public kernel audit failed' }
    $Groups = @(
        @{Name='R36_STATIC'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_static.py'},
        @{Name='R36_CONTEXT'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_context.py'},
        @{Name='R36_PUBLIC'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_public.py'},
        @{Name='R3R4_HISTORICAL'; Path='phase165_r6_2_unified_registry_r3_r4/test_r3_r4.py'},
        @{Name='R35_RULE'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'},
        @{Name='R34_PUBLIC'; Path='phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_public.py'},
        @{Name='R34_SOURCE'; Path='phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R36_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R36 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R36_RUN=PASS'
    Write-Output 'PHASE174_R3R7R36_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
