$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $PackageDir

Set-Location $RepoDir

Write-Host "Phase 166 R3-AU: gen_coe cross audit"
Write-Host "Repository: $RepoDir"

python ".\phase166_r3au_gen_coe_cross_audit\audit.py" --repo "."
python -m pytest ".\phase166_r3au_gen_coe_cross_audit\test_r3au.py" -q

Write-Host "R3-AU targeted audit/tests completed; full pytest NOT run."
