$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $here 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R15 audit failed' }
python -m pytest -q (Join-Path $here 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R15 targeted pytest failed' }
Write-Host 'R27-R15 read-only audit complete; full pytest NOT run. Deletion begins R27-R16 after migration guards.'
