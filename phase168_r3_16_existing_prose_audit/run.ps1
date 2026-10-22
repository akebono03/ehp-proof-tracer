$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$project;$package;$previous"
    python -m pytest -q (Join-Path $package 'tests/test_phase168_r3_16_existing_prose_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-16 targeted tests failed' }
    python (Join-Path $package 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-16 probe failed' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-16 AUDIT_ONLY: no production code modified; full suite not run.'
