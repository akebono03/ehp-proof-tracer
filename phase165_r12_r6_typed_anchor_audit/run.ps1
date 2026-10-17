$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$oldPythonPath = $env:PYTHONPATH
$oldEncoding = $env:PYTHONIOENCODING
Push-Location $root
try {
    $env:PYTHONPATH = if ($oldPythonPath) { "$root;$oldPythonPath" } else { $root }
    $env:PYTHONIOENCODING = 'utf-8'
    & python -m pytest -q '.\phase165_r12_r6_typed_anchor_audit\tests\test_r12_r6.py' '.\tests\test_phase165_r8_rule_provider.py' '.\tests\test_phase165_r12_r5_structure_bridge.py'
    if ($LASTEXITCODE -ne 0) { throw 'R12-R6 focused pytest failed.' }
    & python -m phase165_r12_r6_typed_anchor_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R12-R6 typed binding audit failed.' }
    Write-Host 'R12-R6 real typed witness audit finished; full pytest NOT run.'
} finally {
    $env:PYTHONPATH = $oldPythonPath
    $env:PYTHONIOENCODING = $oldEncoding
    Pop-Location
}
