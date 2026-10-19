$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $here 'audit.py') --data-dir (Join-Path $here 'data') --output (Join-Path $here 'audit_result.json')
if ($LASTEXITCODE -ne 0) { throw 'R1 read-only database audit failed' }
Write-Host 'R1 read-only audit completed; no production code modified; full pytest NOT run.'
