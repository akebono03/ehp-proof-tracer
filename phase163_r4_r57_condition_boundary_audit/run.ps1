$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$scope = Join-Path $root 'phase163_r4_r56_output\scope.json'
$sources = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
$output = Join-Path $root 'phase163_r4_r57_output'
foreach ($path in @($scope, $sources)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r57_condition_boundary_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r57_condition_boundary_audit.py" --scope "$scope" --sources "$sources" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R57 evidence boundary audit complete. No production changes. Full pytest not run.'
