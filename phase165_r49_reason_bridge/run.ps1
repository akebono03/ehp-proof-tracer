$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
if (Get-Command python -ErrorAction SilentlyContinue) { $python = 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { $python = 'py' } else { throw 'Python 3 is required.' }
if ($python -eq 'py') { & py -3 '.\phase165_r49_reason_bridge\apply.py' } else { & python '.\phase165_r49_reason_bridge\apply.py' }
if ($LASTEXITCODE -ne 0) { throw 'R49 install failed' }
Copy-Item '.\phase165_r49_reason_bridge\test_phase165_r49_typed_reasons.py' '.\tests\test_phase165_r49_typed_reasons.py' -Force
if ($python -eq 'py') { & py -3 -m pytest -q tests/test_phase165_r49_typed_reasons.py } else { & python -m pytest -q tests/test_phase165_r49_typed_reasons.py }
if ($LASTEXITCODE -ne 0) { throw 'R49 targeted tests failed' }
Write-Output 'R49 targeted tests passed; full pytest NOT run.'
