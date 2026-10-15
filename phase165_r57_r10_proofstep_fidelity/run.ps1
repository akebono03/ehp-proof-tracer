$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python "$package\install.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q "$package\test_phase165_r57_r10_proofstep_fidelity.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q ".\phase165_r57_r9_renderer_comparison\test_phase165_r57_r9_renderer_comparison.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q ".\phase165_r57_r8_general_specialization\test_phase165_r57_r8_general_specialization.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "R57-R10 targeted pytest passed; full pytest NOT run."
} finally { Pop-Location }
