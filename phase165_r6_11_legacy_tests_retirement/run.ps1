$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path '.').Path
$Package = Join-Path $Root 'phase165_r6_11_legacy_tests_retirement'
Push-Location $Package
try {
    python -m pytest -q test_apply.py
    if ($LASTEXITCODE -ne 0) { throw 'Package self-tests failed; no retirement applied' }
} finally { Pop-Location }
python (Join-Path $Package 'apply.py') $Root
if ($LASTEXITCODE -ne 0) { throw 'Dependency blockers or parse errors; retirement aborted. Inspect report.json' }
Write-Host 'Only 13 named test files considered; legacy Probes and math/rules untouched; full pytest NOT run.'
