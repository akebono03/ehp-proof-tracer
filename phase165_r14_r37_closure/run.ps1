$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r37_closure.py" ".\phase165_r14_r37_closure.py" -Force
$OldPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($OldPath) { "$Root$([IO.Path]::PathSeparator)$OldPath" } else { $Root }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r37_closure.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    if (Test-Path ".\phase165_r14_r37_output\phase_closed.flag") {
        Write-Host "Phase165 strict closure succeeded; running full pytest."
        python -m pytest -q
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } else {
        Write-Host "Phase165 NOT closed; strict registry unverified. Full pytest deferred until phase completion."
    }
}
finally { $env:PYTHONPATH = $OldPath }
