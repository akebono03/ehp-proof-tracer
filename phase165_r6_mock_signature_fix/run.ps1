$ErrorActionPreference = 'Stop'
python -X utf8 '.\phase165_r6_mock_signature_fix\apply.py'
if ($LASTEXITCODE -ne 0) { throw "R6 mock signature targeted tests failed; exit=$LASTEXITCODE" }
Write-Host 'R6 mock signatures: 3 targeted tests PASS; full pytest NOT run.'
