$ErrorActionPreference = "Stop"
$project = Split-Path -Parent $PSScriptRoot
Set-Location $project
$source = Join-Path $project "phase163_r4_r70_output\pending_batch_audit.json"
if (-not (Test-Path $source)) { throw "Missing R70 output: $source" }
python -m pytest -q ".\phase163_r4_r71_semantic_review_queue\tests\test_phase163_r4_r71_semantic_review_queue.py"
if ($LASTEXITCODE -ne 0) { throw "R71 focused pytest failed" }
python ".\phase163_r4_r71_semantic_review_queue\phase163_r4_r71_semantic_review_queue.py" --input $source --output ".\phase163_r4_r71_output"
if ($LASTEXITCODE -ne 0) { throw "R71 generation failed" }
Write-Host "R71 read-only review queue complete. Full pytest not run."
