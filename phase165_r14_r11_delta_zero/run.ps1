$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r11_delta_zero.py" ".\phase165_r14_r11_delta_zero.py" -Force
$PreviousPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($PreviousPath) { "$Root$([IO.Path]::PathSeparator)$PreviousPath" } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r11_delta_zero.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $PreviousPath }
Write-Host "Phase 165 R14-R11 targeted checks complete; full pytest NOT run."
