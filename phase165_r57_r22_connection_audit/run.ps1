$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$python = 'python'
& $python '.\phase165_r57_r22_connection_audit\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R22 audit failed' }
& $python -m pytest -q '.\phase165_r57_r22_connection_audit\test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R22 targeted pytest failed' }
Write-Output 'R22 READ-ONLY AUDIT COMPLETE; full pytest NOT run.'
