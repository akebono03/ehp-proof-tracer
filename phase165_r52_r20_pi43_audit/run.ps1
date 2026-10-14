$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from repository root.' }
Copy-Item "$package\phase165_r52_r20_pi43_audit.py" '.\phase165_r52_r20_pi43_audit.py' -Force
Copy-Item "$package\test_phase165_r52_r20_pi43_audit.py" '.\test_phase165_r52_r20_pi43_audit.py' -Force
python -m pytest -q test_phase165_r52_r20_pi43_audit.py test_phase165_r52_r9_shared_math.py
if ($LASTEXITCODE -ne 0) { throw 'R20 targeted tests failed' }
python -m phase165_r52_r20_pi43_audit
if ($LASTEXITCODE -ne 0) { throw 'R20 audit failed' }
Write-Host 'R20 read-only audit completed; full pytest NOT run.'
