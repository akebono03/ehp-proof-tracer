$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$extraction = Join-Path $root 'phase163_r4_r42_output\extraction.json'
$inputs = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
if (-not (Test-Path $extraction)) { throw "R4-R42 extraction not found: $extraction" }
if (-not (Test-Path $inputs)) { throw "R4-R42 TeX inputs not found: $inputs" }
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r43_mapping.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r43_mapping.py" --extraction "$extraction" --inputs "$inputs" --output "$root\phase163_r4_r43_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
