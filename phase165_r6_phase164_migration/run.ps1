$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python (Join-Path $PSScriptRoot 'apply_and_test.py')
if ($LASTEXITCODE -ne 0) { throw 'Phase164 limited pytest failed or source guard refused patch' }
