param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
try {
    if ($DryRun) {
        python -B -m phase176_r3r30_generic_hopf_substitution_isolated.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw "R3R30 DryRun failed" }
    } else {
        python -B -m phase176_r3r30_generic_hopf_substitution_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw "R3R30 audit failed" }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r30_generic_hopf_substitution_isolated\tests `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw "R3R30 focused tests failed" }
        Write-Host "PHASE176_R3R30_GATE=PASS_R3R30_FOCUSED_TESTS"
        Write-Host "PHASE176_R3R30_FULL_PYTEST=NOT_RUN"
        Write-Host "(END)"
    }
} finally {
    Pop-Location
}
