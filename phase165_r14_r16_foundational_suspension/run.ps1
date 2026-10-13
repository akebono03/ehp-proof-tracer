$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r16_foundational_suspension.py" ".\phase165_r14_r16_foundational_suspension.py" -Force
$PriorPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($PriorPythonPath) { "$Root$([IO.Path]::PathSeparator)$PriorPythonPath" } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r16_foundational_suspension.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $PriorPythonPath }
Write-Host "R14-R16 targeted verification finished; full pytest NOT run."
