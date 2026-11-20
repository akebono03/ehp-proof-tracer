param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    if ($DryRun) {
        python -B -m phase176_r3r28_toda55_quadruple_public.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R28 DryRun failed' }
    } else {
        python -B -m phase176_r3r28_toda55_quadruple_public.install
        if ($LASTEXITCODE -ne 0) { throw 'R3R28 installation failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r28_toda55_quadruple_public\tests `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests `
            .\phase174_r3_r6_source_extension\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R28 focused tests failed' }
        Write-Host 'PHASE176_R3R28_GATE=PASS_R3R28_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R28_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
