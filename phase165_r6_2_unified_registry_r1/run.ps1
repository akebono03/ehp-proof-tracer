$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from the repository root.' }
python -m pytest -q .\phase165_r6_2_unified_registry_r1\test_registry.py
if ($LASTEXITCODE -ne 0) { throw 'Unified registry targeted tests failed.' }
python -m phase165_r6_2_unified_registry_r1.install
if ($LASTEXITCODE -ne 0) { throw 'Install failed.' }
python -c "import phase165_r52_r9_shared_math; print('Shared provider import: PASS')"
if ($LASTEXITCODE -ne 0) { throw 'Shared provider import failed.' }
Write-Output 'Unified registry R1 installed; full pytest NOT run.'
