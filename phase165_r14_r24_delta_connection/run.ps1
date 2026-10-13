$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r24_delta_connection.py" ".\phase165_r14_r24_delta_connection.py" -Force
$OriginalPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($OriginalPythonPath) { "$Root$([IO.Path]::PathSeparator)$OriginalPythonPath" } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r24_delta_connection.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $OriginalPythonPath }
Write-Host "R14-R24 targeted tests finished; full pytest NOT run."
