$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r4_remaining_schemas.py" ".\phase165_r14_r4_remaining_schemas.py" -Force
$OriginalPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($OriginalPythonPath) {
        "$Root$([IO.Path]::PathSeparator)$OriginalPythonPath"
    } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r4_remaining_schemas.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $OriginalPythonPath }
Write-Host "Phase 165 R14-R4 targeted tests and source audit complete; full pytest NOT run."
