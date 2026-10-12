$ErrorActionPreference = "Stop"
$project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $project
if (-not (Test-Path ".\phase163_r4_r72_output\role_proposals.json")) { throw "Run R4-R72 first: input is missing" }
python -m pytest -q ".\phase163_r4_r73_context_decisions\tests\test_phase163_r4_r73_context_decisions.py"
if ($LASTEXITCODE -ne 0) { throw "R73 focused pytest failed" }
python ".\phase163_r4_r73_context_decisions\phase163_r4_r73_context_decisions.py"
if ($LASTEXITCODE -ne 0) { throw "R73 audit failed" }
Write-Host "R4-R73 editorial context decisions complete. Production registry unchanged. Full pytest not run."
