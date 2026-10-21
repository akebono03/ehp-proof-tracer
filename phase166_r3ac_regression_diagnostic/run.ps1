$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from EHP Proof Tracer root' }
python -m phase166_r3ac_regression_diagnostic.diagnose
if ($LASTEXITCODE -ne 0) { throw 'Diagnostic failed' }
Write-Host 'Read-only diagnostic completed; no pytest or production changes.'
