$ErrorActionPreference = 'Stop'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $dir
Push-Location $root
try {
    $python = 'python'
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        if (Get-Command py -ErrorAction SilentlyContinue) { $python = 'py' }
        else { throw 'Python executable was not found' }
    }
    & $python -m pytest -q "$dir\test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R57-R17 focused tests failed' }
    & $python "$dir\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R57-R17 runtime audit reported an error; inspect audit_results.json' }
    Write-Host 'R57-R17 read-only audit completed; full pytest NOT run.'
    Write-Host "Results: $dir\audit_results.json"
    Write-Host "Summary: $dir\audit_results.txt"
} finally {
    Pop-Location
}
