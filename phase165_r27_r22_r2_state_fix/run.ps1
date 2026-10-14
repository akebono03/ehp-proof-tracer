$ErrorActionPreference = "Stop"
$Root = (Get-Location).Path
$Package = Join-Path $Root "phase165_r27_r22_r2_state_fix"
python (Join-Path $Package "apply.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $Package "test_installer.py") (Join-Path $Package "test_patch.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R27-R22-R2 targeted checks passed; full pytest NOT run."
