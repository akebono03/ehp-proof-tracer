$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path -LiteralPath (Join-Path $root 'unified_statement_registry.py'))) {
    throw 'Run this script from EHP Proof Tracer project root.'
}
$script = Join-Path $PSScriptRoot 'r2_audit.py'
python $script --project $root
if ($LASTEXITCODE -ne 0) { throw 'R2 audit failed.' }
