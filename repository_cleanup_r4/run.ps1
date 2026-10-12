$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
if (-not (Test-Path -LiteralPath (Join-Path $project 'unified_statement_registry.py') -PathType Leaf)) {
    throw 'Run from EHP Proof Tracer project root.'
}
python (Join-Path $PSScriptRoot 'r4_verify.py') --project $project
if ($LASTEXITCODE -ne 0) { throw 'R4 verification failed. See repository_cleanup_r4_output/r4_report.md and r4_targeted_pytest.log.' }
