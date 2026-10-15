$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
python ".\phase165_r57_r19_delta_image_backward\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$tests = @(
    ".\phase165_r57_r19_delta_image_backward\test_phase165_r57_r19_delta_image_backward.py",
    ".\phase165_r57_r18_generator_substitution\test_phase165_r57_r18_generator_substitution.py"
)
foreach ($test in $tests) {
    Write-Host "Running focused pytest: $test"
    python -m pytest -q $test
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Write-Host "R57-R19 targeted tests passed; full pytest NOT run."
python ".\phase165_r57_r19_delta_image_backward\audit_r19.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
