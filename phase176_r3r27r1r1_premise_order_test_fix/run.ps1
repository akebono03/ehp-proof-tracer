param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    if ($DryRun) {
        python -B -m phase176_r3r27r1r1_premise_order_test_fix.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1R1 DryRun failed' }
        Write-Host 'PHASE176_R3R27R1R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    } else {
        python -B -m phase176_r3r27r1r1_premise_order_test_fix.install
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1R1 installation failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests `
            .\phase174_r3_r6_source_extension\tests\test_source.py `
            .\phase171_r2e_toda53_double_source\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1R1 focused pytest failed' }
        Write-Host 'PHASE176_R3R27R1R1_GATE=PASS_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R27R1R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
