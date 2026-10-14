$ErrorActionPreference = "Stop"
$Root = (Get-Location).Path
$Package = Join-Path $Root "phase165_r27_r22_r4_fixture_fix"
$Installer = Join-Path $Root "phase165_r27_r22_r3_complete_fix"
if (-not (Test-Path (Join-Path $Installer "test_installer.py"))) {
  throw "R27-R22-R3 package missing; extract the previously installed R3 ZIP first"
}
python -m pytest -q (Join-Path $Installer "test_installer.py") (Join-Path $Package "test_patch.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R27-R22-R4: corrected typed generator test fixture; no production code modified; full pytest NOT run."
