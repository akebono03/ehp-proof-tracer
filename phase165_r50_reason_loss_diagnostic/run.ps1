$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python "$PSScriptRoot\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R50 read-only diagnostic failed; see phase165_r50_reason_loss_diagnostic_output\audit.json' }
