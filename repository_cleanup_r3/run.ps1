$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path -LiteralPath (Join-Path $root 'unified_statement_registry.py') -PathType Leaf)) {
    throw 'Run from EHP Proof Tracer project root.'
}
if (-not (Test-Path -LiteralPath (Join-Path $root 'repository_cleanup_r2_output\r2_cache_candidates.csv') -PathType Leaf)) {
    throw 'R2 candidate CSV missing. Run R2 first.'
}
python (Join-Path $PSScriptRoot 'r3_cleanup.py') --project $root --apply
if ($LASTEXITCODE -ne 0) { throw 'R3 cleanup failed. Read r3_report.md if present.' }
