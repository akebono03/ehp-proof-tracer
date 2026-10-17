$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$folder = Join-Path $root "phase165_r6_2_unified_registry_r3_r3"
if (-not (Test-Path (Join-Path $folder "install.py"))) { throw "Run from repository root" }
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $folder "test_r3_r3.py")
if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed; no installation" }
python -m phase165_r6_2_unified_registry_r3_r3.install
if ($LASTEXITCODE -ne 0) { throw "Installer failed" }
python -c "import phase165_r52_r9_shared_math; print('Shared provider import: PASS')"
if ($LASTEXITCODE -ne 0) { throw "Import check failed" }
Write-Output 'R3-3 installed; full pytest NOT run.'
