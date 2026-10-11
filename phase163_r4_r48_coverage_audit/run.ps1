$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$catalog = Join-Path $root 'phase163_r4_r47_output\catalog.json'
$inputs = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
$output = Join-Path $root 'phase163_r4_r48_output'
foreach ($path in @($catalog, $inputs)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r48_coverage_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r48_coverage_audit.py" --catalog "$catalog" --inputs "$inputs" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'No source, Registry, or catalog modifications. Full pytest not run.'
