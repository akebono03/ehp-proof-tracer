$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r13_source_review.py" ".\phase165_r14_r13_source_review.py" -Force
$Old = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($Old) { "$Root$([IO.Path]::PathSeparator)$Old" } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r13_source_review.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $Old }
Write-Host "Phase 165 R14-R13 focused checks complete; full pytest NOT run."
