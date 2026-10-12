$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$overlap = Join-Path $root 'phase163_r4_r53_output\overlap_audit.json'
$output = Join-Path $root 'phase163_r4_r54_output'
foreach ($path in @($overlap, (Join-Path $root 'phase163_r4_registry_bridge.py'), (Join-Path $root 'unified_statement_registry.py'), (Join-Path $root 'theorem_facts.py'), (Join-Path $root 'toda_literature_statement_boundary.py'))) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r54_live_registry_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r54_live_registry_audit.py" --overlap "$overlap" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R54 read-only live bridge content audit complete. Full pytest not run.'
