$ErrorActionPreference = 'Stop'
python '.\phase166_r3am_suspension_one\apply.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q '.\phase166_r3am_suspension_one\tests\test_suspension_one.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Targeted tests PASS; full pytest NOT run.'
