$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $PackageDir '..')).Path
Set-Location $Root
python -m py_compile '.\phase165_r6_binding_candidates.py' '.\tests\test_phase165_r6_binding_candidates.py' '.\phase165_r6_binding_candidates\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R6 syntax failed' }
python -m pytest -q '.\tests\test_phase165_r6_binding_candidates.py'
if ($LASTEXITCODE -ne 0) { throw 'R6 focused tests failed' }
$OldPythonPath = $env:PYTHONPATH
try {
    if ([string]::IsNullOrEmpty($OldPythonPath)) { $env:PYTHONPATH = $Root }
    else { $env:PYTHONPATH = "$Root$([IO.Path]::PathSeparator)$OldPythonPath" }
    python '.\phase165_r6_binding_candidates\audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R6 audit failed' }
}
finally { $env:PYTHONPATH = $OldPythonPath }
Write-Host 'R6 candidates generated; no proof promotion; full pytest NOT run.'
