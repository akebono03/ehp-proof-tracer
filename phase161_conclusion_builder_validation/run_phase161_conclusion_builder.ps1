$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
$script = Join-Path $PSScriptRoot 'audit_phase161_conclusion_builder.py'
python -B $script
if ($LASTEXITCODE -ne 0) { throw "Audit failed with exit code $LASTEXITCODE" }
