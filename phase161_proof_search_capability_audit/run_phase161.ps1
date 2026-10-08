$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$script = Join-Path $PSScriptRoot 'audit_phase161.py'
if (-not (Test-Path (Join-Path $repo 'repository_inference.py'))) {
  throw 'Run this script from the ehp-proof-tracer repository root.'
}
python -B $script
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
