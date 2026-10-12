$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
$env:PYTHONPATH = $PSScriptRoot
python -m pytest -q ".\phase163_r4_r72_mathematical_role_proposals\tests\test_phase163_r4_r72_mathematical_role_proposals.py"
if ($LASTEXITCODE -ne 0) { throw 'R72 focused pytest failed' }
python ".\phase163_r4_r72_mathematical_role_proposals\phase163_r4_r72_mathematical_role_proposals.py" --r71 ".\phase163_r4_r71_output\semantic_review_queue.json" --output ".\phase163_r4_r72_output"
if ($LASTEXITCODE -ne 0) { throw 'R72 audit failed' }
Write-Host 'R72 complete. No production changes. Full pytest not run.'
