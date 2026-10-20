$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from repository root.' }
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $folder 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-G runtime path audit failed.' }
Write-Host 'Read-only runtime path audit completed; full pytest NOT run.'
