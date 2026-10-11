$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$extraction = Join-Path $root 'phase163_r4_r42_output\extraction.json'
$mapping = Join-Path $root 'phase163_r4_r43_output\mapping.json'
$crosswalk = Join-Path $root 'phase163_r4_r44_output\crosswalk.json'
$inputs = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
$output = Join-Path $root 'phase163_r4_r47_output'
foreach ($path in @($extraction, $mapping, $crosswalk, $inputs)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r47_tex_catalog.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r47_tex_catalog.py" --extraction "$extraction" --mapping "$mapping" --crosswalk "$crosswalk" --inputs "$inputs" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
