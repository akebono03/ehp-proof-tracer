$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -Path (Join-Path $PackageDir "phase163_r4_r4_role_classification.py") -Destination (Join-Path $ProjectRoot "phase163_r4_r4_role_classification.py") -Force
$TestDir = Join-Path $ProjectRoot "tests"
if (-not (Test-Path $TestDir)) { New-Item -ItemType Directory -Path $TestDir | Out-Null }
Copy-Item -Path (Join-Path $PackageDir "tests\test_phase163_r4_r4_role_classification.py") -Destination (Join-Path $TestDir "test_phase163_r4_r4_role_classification.py") -Force
python -m pytest -q tests/test_phase163_r4_r3_statement_mapping.py tests/test_phase163_r4_r4_role_classification.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python phase163_r4_r4_role_classification.py --root "$ProjectRoot" --output (Join-Path $ProjectRoot "phase163_r4_r4_output")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 163 R4-R4 focused tests complete. Full suite not run."
