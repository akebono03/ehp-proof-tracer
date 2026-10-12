$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$review = Join-Path $root 'phase163_r4_r50_output\review.json'
$catalog = Join-Path $root 'phase163_r4_r47_output\catalog.json'
$inputs = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
$output = Join-Path $root 'phase163_r4_r51_output'
foreach ($path in @($review, $catalog, $inputs)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r51_priority_semantic_review.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r51_priority_semantic_review.py" --review "$review" --catalog "$catalog" --inputs "$inputs" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Read-only R4-R51 complete. No source, catalog, Registry or ID changes. Full pytest not run.'
