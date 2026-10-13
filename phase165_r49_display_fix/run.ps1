$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
if (Get-Command python -ErrorAction SilentlyContinue) { $python = 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { $python = 'py' } else { throw 'Python 3 is required' }
if ($python -eq 'py') { & py -3 '.\phase165_r49_display_fix\apply.py' } else { & python '.\phase165_r49_display_fix\apply.py' }
if ($LASTEXITCODE -ne 0) { throw 'R49 display bridge installation failed' }
Copy-Item '.\phase165_r49_display_fix\test_phase165_r49_display_fix.py' '.\tests\test_phase165_r49_display_fix.py' -Force
if ($python -eq 'py') { & py -3 -m pytest -q tests/test_phase165_r49_typed_reasons.py tests/test_phase165_r49_display_fix.py } else { & python -m pytest -q tests/test_phase165_r49_typed_reasons.py tests/test_phase165_r49_display_fix.py }
if ($LASTEXITCODE -ne 0) { throw 'R49 targeted tests failed' }
Write-Output 'R49 focused tests completed; full pytest NOT run.'
