$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r15_typed_diagonal.py" ".\phase165_r14_r15_typed_diagonal.py" -Force
$Prior = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($Prior) { "$Root$([IO.Path]::PathSeparator)$Prior" } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r15_typed_diagonal.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $Prior }
Write-Host "R14-R15 targeted checks complete; full pytest NOT run."
