$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$crosswalk = Join-Path $root 'phase163_r4_r52_output\crosswalk.json'
$catalog = Join-Path $root 'phase163_r4_r47_output\catalog.json'
$inputs = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
$output = Join-Path $root 'phase163_r4_r53_output'
foreach ($path in @($crosswalk, $catalog, $inputs)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r53_semantic_overlap_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r53_semantic_overlap_audit.py" --crosswalk "$crosswalk" --catalog "$catalog" --inputs "$inputs" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R53 read-only containment/overlap boundary audit complete. Full pytest not run.'
