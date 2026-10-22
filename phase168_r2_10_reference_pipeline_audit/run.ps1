$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Join-Path $project 'phase168_r2_10_reference_pipeline_audit'
if (-not (Test-Path (Join-Path $package 'audit.py'))) {
    throw 'Run this script from the ehp_proof repository root after Expand-Archive.'
}
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Read-only audit finished. Open output/reference_pipeline_report.md'
