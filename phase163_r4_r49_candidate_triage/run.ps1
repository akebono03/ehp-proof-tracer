$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$audit = Join-Path $root 'phase163_r4_r48_output\audit.json'
$catalog = Join-Path $root 'phase163_r4_r47_output\catalog.json'
$inputs = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
$output = Join-Path $root 'phase163_r4_r49_output'
foreach ($path in @($audit, $catalog, $inputs)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r49_candidate_triage.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r49_candidate_triage.py" --audit "$audit" --catalog "$catalog" --inputs "$inputs" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Read-only R4-R49 completed. No Registry, catalog, TeX or IDs modified. Full pytest not run.'
