param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
try {
    if ($DryRun) {
        python -B -m phase176_r3r31_generic_hopf_public_connection.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw "R3R31 DryRun failed" }
    } else {
        python -B -m phase176_r3r31_generic_hopf_public_connection.installer
        if ($LASTEXITCODE -ne 0) { throw "R3R31 installation failed" }
        python -B -m phase176_r3r31_generic_hopf_public_connection.audit
        if ($LASTEXITCODE -ne 0) { throw "R3R31 public audit failed" }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r31_generic_hopf_public_connection\tests `
            .\phase176_r3r30_generic_hopf_substitution_isolated\tests `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw "R3R31 focused pytest failed" }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw "R3R31 git diff check failed" }
        Write-Host "PHASE176_R3R31_GATE=PASS_R3R31_FOCUSED_TESTS"
        Write-Host "PHASE176_R3R31_FULL_PYTEST=NOT_RUN"
        Write-Host "(END)"
    }
} finally {
    Pop-Location
}
