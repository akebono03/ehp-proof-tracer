$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$catalog = Join-Path $root 'phase163_r4_r47_output\catalog.json'
$overlap = Join-Path $root 'phase163_r4_r53_output\overlap_audit.json'
$output = Join-Path $root 'phase163_r4_r55_output'
foreach ($path in @($catalog, $overlap, (Join-Path $root 'unified_statement_registry.py'))) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r55_structured_definition_trial.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r55_structured_definition_trial.py" --catalog "$catalog" --overlap "$overlap" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R55 isolated definition trial complete. Production registry unchanged. Full pytest not run.'
