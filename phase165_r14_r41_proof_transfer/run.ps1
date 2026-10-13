$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r41_proof_transfer.py" ".\phase165_r14_r41_proof_transfer.py" -Force
python "$PSScriptRoot\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$PSScriptRoot\test_phase165_r14_r41_proof_transfer.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$PSScriptRoot\audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R41 target tests complete. Full pytest NOT run. Restart Web server."
