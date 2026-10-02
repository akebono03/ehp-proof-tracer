$ErrorActionPreference = "Stop"
$RepoRoot=(Get-Location).Path
$PackageDir=Split-Path -Parent $MyInvocation.MyCommand.Path
$Out=Join-Path $RepoRoot "phase155_closure_r3_output"
$Orig=Join-Path $Out "shard_plan.json"
$Repair=Join-Path $Out "r3_r2_repair_plan.json"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R3-R2"
Write-Host "=============================================================="
Write-Host "Preserve PASS shards: 1,2,6,7"
Write-Host "Rerun only original shards: 3,4,5,8"
Write-Host ""

python "$PackageDir\apply_phase155_closure_r3_r2.py" --repo-root "$RepoRoot" --original-plan "$Orig"
if ($LASTEXITCODE -ne 0) { throw "apply failed" }

python "$PackageDir\phase155_r3_r2_plan.py" --original-plan "$Orig" --output "$Repair"
if ($LASTEXITCODE -ne 0) { throw "plan failed" }

python "$PackageDir\run_phase155_r3_r2.py" --repo-root "$RepoRoot" --package-dir "$PackageDir" --plan "$Repair" --output-dir "$Out" --timeout 600
if ($LASTEXITCODE -ne 0) { throw "R3-R2 incomplete" }

Write-Host "Closure-R3-R2 COMPLETE"
