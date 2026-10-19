$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python '.\phase165_r6_8_4_close\check.py'
if ($LASTEXITCODE -ne 0) {
  Write-Host 'R6-8(4): outstanding collection or direct legacy imports; inspect report.'
  exit $LASTEXITCODE
}
Write-Host 'R6-8(4): targeted collection clean; full pytest NOT run.'
