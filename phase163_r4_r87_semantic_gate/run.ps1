$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = $PSScriptRoot
$InputFile = Join-Path $ProjectRoot 'phase163_r4_r86_output\claim_review_catalog.json'
if (-not (Test-Path $InputFile)) { throw "Missing R86 output: $InputFile" }
$Bundled = Join-Path $PackageRoot 'claim_review_catalog.json'
if ((Get-FileHash $InputFile -Algorithm SHA256).Hash -ne (Get-FileHash $Bundled -Algorithm SHA256).Hash) { throw 'R86 review input differs from audited snapshot; stop for review.' }
$env:PYTHONPATH = "$PackageRoot;$ProjectRoot;$env:PYTHONPATH"
python -m pytest -q (Join-Path $PackageRoot 'tests\test_phase163_r4_r87_semantic_gate.py')
if ($LASTEXITCODE -ne 0) { throw 'R87 focused pytest failed' }
python (Join-Path $PackageRoot 'phase163_r4_r87_semantic_gate.py') --input $InputFile --output (Join-Path $ProjectRoot 'phase163_r4_r87_output')
if ($LASTEXITCODE -ne 0) { throw 'R87 audit failed' }
Write-Host 'R87 complete. Production unchanged. Full pytest not run.'
