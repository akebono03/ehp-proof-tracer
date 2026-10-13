$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$python = 'python'
& $python '.\phase165_r50_downstream_trace\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R50 downstream trace failed; inspect output/audit.json' }
