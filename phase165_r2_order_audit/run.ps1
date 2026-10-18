$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r55_nk_only_goal.py'))) { throw 'Run from the EHP Proof Tracer project root.' }
$env:PYTHONPATH = "$root;$env:PYTHONPATH"
python "$PSScriptRoot\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'Audit failed. No project source files were changed.' }
Write-Host 'Read-only audit complete. No pytest run; no source files changed.'
