param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    if ($DryRun) {
        python -B -m phase176_r3r29_hopf_right_connection_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R29 DryRun failed' }
    } else {
        python -B -m phase176_r3r29_hopf_right_connection_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R29 audit failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r29_hopf_right_connection_audit\tests `
            .\phase176_r3r28_toda55_quadruple_public\tests\test_public.py `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests\test_source.py `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R29 focused tests failed' }
        Write-Host 'PHASE176_R3R29_GATE=PASS_R3R29_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R29_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
