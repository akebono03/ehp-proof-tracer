$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r12_registry_obligations.py" ".\phase165_r14_r12_registry_obligations.py" -Force
$Old = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($Old) { "$Root$([IO.Path]::PathSeparator)$Old" } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r12_registry_obligations.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $Old }
Write-Host "R14-R12 targeted tests finished; full pytest NOT run."
