$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$bundle = Join-Path $root 'phase163_r4_r76_tex_boundary_link'
$env:PYTHONPATH = "$bundle;$root"
python -m pytest -q (Join-Path $bundle 'tests/test_phase163_r4_r76_tex_boundary_link.py')
if ($LASTEXITCODE -ne 0) { throw 'R76 focused pytest failed' }
$sources = Join-Path $root 'phase163_r4_r42_tex_extract/inputs'
$inputFile = Join-Path $root 'phase163_r4_r75_output/ownership_proposals.json'
if (-not (Test-Path $sources)) { throw "Missing original TeX extract: $sources" }
if (-not (Test-Path $inputFile)) { throw "Missing R75 output: $inputFile" }
python (Join-Path $bundle 'phase163_r4_r76_tex_boundary_link.py') --input $inputFile --sources $sources --output (Join-Path $root 'phase163_r4_r76_output')
if ($LASTEXITCODE -ne 0) { throw 'R76 source boundary audit failed' }
Write-Host 'R76 read-only TeX boundary crosswalk complete. Full suite not run.'
