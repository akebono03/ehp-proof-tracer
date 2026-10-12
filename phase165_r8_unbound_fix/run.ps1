$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root

$Production = Join-Path $Root 'phase165_r8_rule_provider.py'
$Test = Join-Path $Root 'tests\test_phase165_r8_rule_provider.py'
if (-not (Test-Path $Production)) { throw "R8 module missing: $Production" }
if (-not (Test-Path $Test)) { throw "R8 test missing: $Test" }

Copy-Item $Production "$Production.phase165_r8_unbound_backup" -Force
Copy-Item $Test "$Test.phase165_r8_unbound_backup" -Force
Copy-Item (Join-Path $PSScriptRoot 'phase165_r8_rule_provider.py') $Production -Force
Copy-Item (Join-Path $PSScriptRoot 'test_phase165_r8_rule_provider.py') $Test -Force

python -m py_compile $Production $Test
if ($LASTEXITCODE -ne 0) { throw 'R8 syntax check failed' }
python -m pytest -q $Test
if ($LASTEXITCODE -ne 0) { throw 'R8 focused tests failed' }

$OldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$Root$([IO.Path]::PathSeparator)$OldPythonPath"
    python (Join-Path $Root 'phase165_r8_rule_provider\audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R8 audit failed' }
} finally {
    $env:PYTHONPATH = $OldPythonPath
}
Write-Host 'R8 unbound-variable guard passed; no source assertion promoted; full pytest NOT run.'
