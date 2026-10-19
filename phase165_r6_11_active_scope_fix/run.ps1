$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path '.').Path
$Package = Join-Path $Root 'phase165_r6_11_active_scope_fix'
Push-Location $Package
try {
    python -m pytest -q test_apply.py
    if ($LASTEXITCODE -ne 0) { throw 'Package self-tests failed; no retirement applied' }
} finally { Pop-Location }
python (Join-Path $Package 'apply.py') $Root
if ($LASTEXITCODE -ne 0) { throw 'Active dependencies or parse errors; retirement aborted. Inspect report.json' }
Write-Host 'Legacy tests retired or already absent. Full pytest NOT run.'
