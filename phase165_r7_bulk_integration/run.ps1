$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
if (-not (Test-Path '.\phase163_r4_r94_output\manifest.json')) { throw 'Phase 163 manifest missing' }
if (-not (Test-Path '.\phase165_r5_manifest_bridge.py')) { throw 'R5 module missing' }
if (-not (Test-Path '.\phase165_r6_binding_candidates.py')) { throw 'R6 module missing' }
Copy-Item -Force (Join-Path $PSScriptRoot 'phase165_r7_bulk_integration.py') '.\phase165_r7_bulk_integration.py'
New-Item -ItemType Directory -Force '.\tests' | Out-Null
Copy-Item -Force (Join-Path $PSScriptRoot 'test_phase165_r7_bulk_integration.py') '.\tests\test_phase165_r7_bulk_integration.py'
python -m py_compile '.\phase165_r7_bulk_integration.py' '.\tests\test_phase165_r7_bulk_integration.py'
if ($LASTEXITCODE -ne 0) { throw 'Syntax check failed' }
python -m pytest -q '.\tests\test_phase165_r7_bulk_integration.py'
if ($LASTEXITCODE -ne 0) { throw 'R7 focused tests failed' }
$old = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$root$([IO.Path]::PathSeparator)$old"
    python (Join-Path $PSScriptRoot 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R7 production audit failed' }
} finally { $env:PYTHONPATH = $old }
Write-Host 'R7 bulk audit complete; unverified source assertions remain ineligible. Full pytest NOT run.'
