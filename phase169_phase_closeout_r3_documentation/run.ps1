$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Package
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
Write-Host 'PHASE169_CLOSEOUT_R3_HELPER_TESTS_START'
python -B -m pytest -q --tb=short -p no:cacheprovider "$Package\tests\test_closeout.py"
if ($LASTEXITCODE -ne 0) { throw "Closeout helper tests failed: $LASTEXITCODE" }
Write-Host 'PHASE169_CLOSEOUT_R3_HELPER_TESTS_PASS'
python -B "$Package\run.py" --repo "$Repo"
if ($LASTEXITCODE -ne 0) { throw "Closeout documentation failed: $LASTEXITCODE" }
Write-Host 'PHASE169_CLOSEOUT_R3_EXIT=0'
