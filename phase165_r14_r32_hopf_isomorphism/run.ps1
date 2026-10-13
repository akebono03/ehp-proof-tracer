$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r32_hopf_isomorphism.py" ".\phase165_r14_r32_hopf_isomorphism.py" -Force
$OldPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($OldPath) { "$Root$([IO.Path]::PathSeparator)$OldPath" } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r32_hopf_isomorphism.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $OldPath }
Write-Host "R14-R32 targeted tests complete; full pytest NOT run."
