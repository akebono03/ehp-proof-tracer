$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Source = Join-Path $PSScriptRoot 'phase165_r8_rule_provider.py'
$Destination = Join-Path $Root 'phase165_r8_rule_provider.py'
Copy-Item $Source $Destination -Force
$TestSource = Join-Path $PSScriptRoot 'test_phase165_r8_rule_provider.py'
$TestDestination = Join-Path $Root 'tests\test_phase165_r8_rule_provider.py'
Copy-Item $TestSource $TestDestination -Force
python -m py_compile $Destination $TestDestination (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R8 syntax check failed' }
python -m pytest -q $TestDestination
if ($LASTEXITCODE -ne 0) { throw 'R8 focused tests failed' }
$OldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$Root$([IO.Path]::PathSeparator)$OldPythonPath"
    python (Join-Path $PSScriptRoot 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R8 audit failed' }
} finally { $env:PYTHONPATH = $OldPythonPath }
Write-Host 'R8 generic rule catalog built; no source assertion promoted; full pytest NOT run.'
