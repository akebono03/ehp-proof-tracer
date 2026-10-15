$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
python ".\phase165_r57_r18_generator_substitution\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$tests = @(
    ".\phase165_r57_r18_generator_substitution\test_phase165_r57_r18_generator_substitution.py",
    ".\phase165_r57_r17_readonly_audit\test_audit.py"
)
foreach ($test in $tests) {
    Write-Host "Running focused pytest: $test"
    python -m pytest -q $test
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Write-Host "R57-R18 targeted tests passed; full pytest NOT run."
python ".\phase165_r57_r18_generator_substitution\audit_r18.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
