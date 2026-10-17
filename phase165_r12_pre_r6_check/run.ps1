$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    & python -m pytest -q '.\phase165_r12_pre_r6_check\tests\test_pre_r6.py' '.\tests\test_phase165_r12_r5_structure_bridge.py' '.\tests\test_phase165_r8_rule_provider.py'
    if ($LASTEXITCODE -ne 0) { throw 'Pre-R6 focused pytest failed.' }
    $env:PYTHONIOENCODING = 'utf-8'
    & python -m phase165_r12_pre_r6_check.audit
    if ($LASTEXITCODE -ne 0) { throw 'Pre-R6 audit failed.' }
    Write-Host 'Pre-R6 READ-ONLY audit complete; full pytest NOT run.'
} finally {
    Pop-Location
}
