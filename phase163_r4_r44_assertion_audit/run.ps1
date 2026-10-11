$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$mapping = Join-Path $root 'phase163_r4_r43_output\mapping.json'
$extraction = Join-Path $root 'phase163_r4_r42_output\extraction.json'
$inputs = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
if (-not (Test-Path $mapping)) { throw "R4-R43 mapping not found: $mapping" }
if (-not (Test-Path $extraction)) { throw "R4-R42 extraction not found: $extraction" }
if (-not (Test-Path $inputs)) { throw "TeX source directory not found: $inputs" }
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r44_assertion_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r44_assertion_audit.py" --mapping "$mapping" --extraction "$extraction" --inputs "$inputs" --output "$root\phase163_r4_r44_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
