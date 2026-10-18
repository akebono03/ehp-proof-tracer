$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$script = Join-Path $PSScriptRoot 'audit_r1.py'
if (-not (Test-Path (Join-Path $project 'phase165_r55_nk_only_goal.py'))) {
    throw 'Run this script from the ehp_proof project root.'
}
$env:PYTHONPATH = "$project;$env:PYTHONPATH"
python $script
if ($LASTEXITCODE -ne 0) { throw "R1 audit reported a stage error; inspect phase165_r1_audit_results\audit_result.json" }
