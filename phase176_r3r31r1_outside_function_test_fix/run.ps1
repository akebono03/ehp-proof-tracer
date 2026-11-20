param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
try {
    if ($DryRun) {
        python -B -m phase176_r3r31r1_outside_function_test_fix.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R31R1 DryRun failed' }
    } else {
        python -B -m phase176_r3r31r1_outside_function_test_fix.installer
        if ($LASTEXITCODE -ne 0) { throw 'R3R31R1 install failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r31r1_outside_function_test_fix\tests `
            .\phase176_r3r31_generic_hopf_public_connection\tests `
            .\phase176_r3r30_generic_hopf_substitution_isolated\tests `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R31R1 focused tests failed' }
        Write-Host 'PHASE176_R3R31R1_GATE=PASS_R3R31R1_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R31R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
