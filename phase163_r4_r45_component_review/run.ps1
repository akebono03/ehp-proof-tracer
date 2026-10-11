$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$crosswalk = Join-Path $root 'phase163_r4_r44_output\crosswalk.json'
$mapping = Join-Path $root 'phase163_r4_r43_output\mapping.json'
$extraction = Join-Path $root 'phase163_r4_r42_output\extraction.json'
$inputs = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
foreach ($path in @($crosswalk, $mapping, $extraction, $inputs)) {
    if (-not (Test-Path $path)) { throw "Required input not found: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r45_component_review.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r45_component_review.py" --crosswalk "$crosswalk" --mapping "$mapping" --extraction "$extraction" --inputs "$inputs" --output "$root\phase163_r4_r45_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
