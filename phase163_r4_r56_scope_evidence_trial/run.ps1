$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$catalog = Join-Path $root 'phase163_r4_r47_output\catalog.json'
$trial = Join-Path $root 'phase163_r4_r55_output\trial.json'
$output = Join-Path $root 'phase163_r4_r56_output'
foreach ($path in @($catalog, $trial)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r56_scope_evidence_trial.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r56_scope_evidence_trial.py" --catalog "$catalog" --trial "$trial" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R56 explicit scope audit complete. No production changes. Full pytest not run.'
