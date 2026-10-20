$ErrorActionPreference = 'Stop'
if (-not (Test-Path (Join-Path (Get-Location).Path 'phase165_r55_nk_only_goal.py'))) {
  throw 'Run from ehp_proof repository root.'
}
python (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-Q read-only audit failed.' }
Write-Host 'Read-only R3-Q audit completed; full pytest NOT run.'
