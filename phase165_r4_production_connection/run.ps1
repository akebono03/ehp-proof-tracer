$ErrorActionPreference = 'Stop'

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $PackageDir '..')).Path
Set-Location $Root

foreach ($name in @(
    'phase165_r3_recursive_search.py',
    'phase165_r2_registry_lookup.py',
    'phase165_goal_only_search.py',
    'phase165_r4_production_connection.py',
    'phase163_r4_registry_bridge.py'
)) {
    if (-not (Test-Path (Join-Path $Root $name))) {
        throw "Required project module missing: $name"
    }
}

python -m py_compile `
    '.\phase165_r4_production_connection.py' `
    '.\tests\test_phase165_r4_production_connection.py' `
    '.\phase165_r4_production_connection\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R4 syntax failure' }

python -m pytest -q '.\tests\test_phase165_r4_production_connection.py'
if ($LASTEXITCODE -ne 0) { throw 'R4 focused tests failed' }

$OldPythonPath = $env:PYTHONPATH
try {
    if ([string]::IsNullOrEmpty($OldPythonPath)) {
        $env:PYTHONPATH = $Root
    } else {
        $env:PYTHONPATH = "$Root$([IO.Path]::PathSeparator)$OldPythonPath"
    }

    python '.\phase165_r4_production_connection\audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4 registry discovery failed' }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
}

Write-Host 'R4 registry discovery complete; Goal-only proof is not yet certified. Full pytest NOT run.'
