param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r38_source_bound_zero_image_public_wiring.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R38 Source Guard failed' }
    if ($DryRun) {
        python -B -m phase174_r3_r7_r38_source_bound_zero_image_public_wiring.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R38 audit DryRun failed' }
        Write-Output 'PHASE174_R3R7R38_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r38_source_bound_zero_image_public_wiring.install
    if ($LASTEXITCODE -ne 0) { throw 'R38 guarded installation failed' }
    python -B -m phase174_r3_r7_r38_source_bound_zero_image_public_wiring.audit
    if ($LASTEXITCODE -ne 0) { throw 'R38 public audit failed' }
    $Groups = @(
        @{Name='R38_STATIC'; Path='phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_static.py'},
        @{Name='R38_PUBLIC'; Path='phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R36_CONTEXT_REGRESSION'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_context.py'},
        @{Name='R36_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_public.py'},
        @{Name='R6_CYCLIC_ZERO_IMAGE'; Path='phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py'},
        @{Name='R7_COMPOSITE_ZERO'; Path='phase174_r3_r7_r7_composite_zero_audit/tests/test_rule.py'},
        @{Name='R9_ASSOCIATIVITY'; Path='phase174_r3_r7_r9_composition_associativity/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R38_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R38 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R38_RUN=PASS'
    Write-Output 'PHASE174_R3R7R38_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
