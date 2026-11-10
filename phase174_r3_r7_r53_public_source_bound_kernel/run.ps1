param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r53_public_source_bound_kernel.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R53 source guard or planned patch failed' }
    python -B -m phase174_r3_r7_r53_public_source_bound_kernel.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R53 audited context preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R53_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r53_public_source_bound_kernel.install
    if ($LASTEXITCODE -ne 0) { throw 'R53 guarded public provider integration failed' }
    python -B -m phase174_r3_r7_r53_public_source_bound_kernel.audit
    if ($LASTEXITCODE -ne 0) { throw 'R53 actual public and Web-model proof audit failed' }
    $Groups = @(
        @{Name='R53_STATIC'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_static.py'},
        @{Name='R53_GUARD'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_guard.py'},
        @{Name='R53_PUBLIC'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_public.py'},
        @{Name='R52_PROBE_REGRESSION'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py'},
        @{Name='R51_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py'},
        @{Name='R50_SCOPED_PROOF_REGRESSION'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_frontier.py'},
        @{Name='R36_CITED_KERNEL_REGRESSION'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_public.py'},
        @{Name='R35_KERNEL_MATH_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R53_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) {
            throw ('R53 focused pytest failed: ' + $Group.Name)
        }
    }
    Write-Output 'PHASE174_R3R7R53_RUN=PASS'
    Write-Output 'PHASE174_R3R7R53_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
