param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    $argsList = @('-B', '-m', 'phase176_r3r26_toda53_55_reuse_audit.audit')
    if ($DryRun) { $argsList += '--dry-run' }
    & python @argsList
    if ($LASTEXITCODE -ne 0) { throw 'R3R26 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider `
          .\phase176_r3r26_toda53_55_reuse_audit\tests `
          .\phase171_r2e_toda53_double_source\tests\test_source.py `
          .\phase174_r3_r6_source_extension\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R26 focused pytest failed' }
        Write-Output 'PHASE176_R3R26_GATE=PASS_R3R26_FOCUSED_TESTS'
        Write-Output 'PHASE176_R3R26_FULL_PYTEST=NOT_RUN'
        Write-Output '(END)'
    }
} finally {
    Pop-Location
}
