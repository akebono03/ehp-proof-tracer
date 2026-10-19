$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    python -m pytest -q -o addopts= "$PSScriptRoot/tests/test_retire_tests.py"
    if ($LASTEXITCODE -ne 0) { throw 'Installer tests failed; no retirement performed.' }
    python "$PSScriptRoot/retire_tests.py" --root $repo --apply
    if ($LASTEXITCODE -ne 0) { throw 'Retirement was blocked; no further work performed.' }
    Write-Host 'R6-8(4) legacy test cohort archived. Full pytest NOT run.'
} finally { Pop-Location }
