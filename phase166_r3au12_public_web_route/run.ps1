$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Set-Location $Root
# Include the repository root when audit.py is launched by filename.
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$Root$([IO.Path]::PathSeparator)$env:PYTHONPATH" } else { $Root }
python ".\phase166_r3au12_public_web_route\audit.py" --n 3 --k 2 --entry flask
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest ".\phase166_r3au12_public_web_route\test_r3au12.py" -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R3-AU-12 targeted PASS; full pytest NOT run.'
