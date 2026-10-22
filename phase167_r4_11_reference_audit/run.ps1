$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$env:PYTHONPATH = $repo
python .\phase167_r4_11_reference_audit\audit.py
if ($LASTEXITCODE -ne 0) { throw 'R4-11 audit failed' }
Write-Host 'Audit completed. Production code unchanged.'
