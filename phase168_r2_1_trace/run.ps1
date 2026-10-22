$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONPATH = $Root
python ".\phase168_r2_1_trace\audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
