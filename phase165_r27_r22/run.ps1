$ErrorActionPreference = "Stop"
$Root = (Get-Location).Path
$Package = Join-Path $Root "phase165_r27_r22"
python (Join-Path $Package "apply.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $Package "test_patch.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R27-R22 targeted tests passed; full pytest NOT run."
