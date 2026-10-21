$ErrorActionPreference = 'Stop'
python .\phase166_r3ac_stable_notation\apply.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AC apply failed' }
python -m pytest -q .\phase166_r3ac_stable_notation\tests\test_r3ac.py .\phase166_r3v_test_repair\test_r3v.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AC targeted tests failed' }
python -m phase166_r3ab_pi65_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-AB runtime audit failed' }
Write-Host 'Targeted tests completed; full pytest NOT run.'
