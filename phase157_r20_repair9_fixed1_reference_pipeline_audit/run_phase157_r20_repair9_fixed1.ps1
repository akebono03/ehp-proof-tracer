$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair9 fixed1 - Reference pipeline audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host ""

$RepositoryRoot = (Get-Location).Path
$env:PYTHONPATH = $RepositoryRoot

Write-Host "Repository root: $RepositoryRoot"
Write-Host "PYTHONPATH: $env:PYTHONPATH"
Write-Host ""

python ".\phase157_r20_repair9_fixed1_reference_pipeline_audit\audit_phase157_r20_repair9_fixed1.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No pytest is run in this audit package."
Write-Host "No production file is modified."
