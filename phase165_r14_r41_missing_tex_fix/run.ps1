$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Source = Join-Path $PSScriptRoot "phase165_r14_r39_toda51.tex"
$Target = Join-Path $Root "phase165_r14_r39_toda51.tex"
if (-not (Test-Path $Source)) { throw "Missing bundled Toda (5.1) TeX" }
Copy-Item $Source $Target -Force
Copy-Item (Join-Path $PSScriptRoot "phase165_r14_r41_proof_transfer.py") (Join-Path $Root "phase165_r14_r41_proof_transfer.py") -Force
$Dispatcher = Get-Content (Join-Path $Root "phase164_r5_r2_common_replay.py") -Raw
if ($Dispatcher -notmatch 'build_phase165_r41_pi32_common_replay') {
  python (Join-Path $PSScriptRoot "install.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
python -m pytest -q (Join-Path $PSScriptRoot "test_phase165_r14_r41_proof_transfer.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python (Join-Path $PSScriptRoot "audit.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R41 bundled TeX fixed; targeted pytest only; no full pytest."
