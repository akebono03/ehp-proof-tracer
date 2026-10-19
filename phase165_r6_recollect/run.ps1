$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$root;$env:PYTHONPATH"
$env:PYTHONIOENCODING = 'utf-8'
& python -m pytest -q (Join-Path $bundle 'tests')
if ($LASTEXITCODE -ne 0) { throw 'Recollection utility self-tests failed.' }
& python (Join-Path $bundle 'recollect.py') --root $root
if ($LASTEXITCODE -ne 0) { throw 'Collection process interrupted or failed to run; see report.' }
Write-Host 'Read report.json and collection.log; no full pytest was performed.'
