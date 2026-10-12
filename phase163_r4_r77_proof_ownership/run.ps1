$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$bundle = Join-Path $root 'phase163_r4_r77_proof_ownership'
$env:PYTHONPATH = "$bundle;$(Join-Path $root 'phase163_r4_r76_tex_boundary_link');$root"
python -m pytest -q (Join-Path $bundle 'tests/test_phase163_r4_r77_proof_ownership.py')
if ($LASTEXITCODE -ne 0) { throw 'R77 focused pytest failed' }
$sources = Join-Path $root 'phase163_r4_r42_tex_extract/inputs'
$inputFile = Join-Path $root 'phase163_r4_r76_output/numbered_boundary_crosswalk.json'
if (-not (Test-Path $sources)) { throw "Missing extracted TeX: $sources" }
if (-not (Test-Path $inputFile)) { throw "Missing R76 output: $inputFile" }
python (Join-Path $bundle 'phase163_r4_r77_proof_ownership.py') --input $inputFile --sources $sources --output (Join-Path $root 'phase163_r4_r77_output')
if ($LASTEXITCODE -ne 0) { throw 'R77 TeX proof ownership audit failed' }
Write-Host 'R77 complete. No production changes. Full pytest not run.'
