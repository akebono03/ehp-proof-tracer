$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
if (-not (Test-Path (Join-Path $project 'phase165_r52_r9_shared_math.py'))) {
    throw 'Run from the EHP Proof Tracer project root'
}
python -m phase166_r3ab_pi65_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-AB audit failed' }
python -m pytest -q phase166_r3ab_pi65_audit/test_r3ab.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AB targeted tests failed; inspect report.json' }
Write-Host 'R3-AB audit finished; full pytest NOT run.'
