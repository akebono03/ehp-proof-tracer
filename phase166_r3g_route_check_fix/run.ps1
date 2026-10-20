$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python ".\phase166_r3g_route_check_fix\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R3-G route audit failed' }
Write-Host 'R3-G route audit completed; production code unchanged; full pytest NOT run.'
