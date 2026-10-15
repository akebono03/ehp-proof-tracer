$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $project
$env:PYTHONPATH = $project
python -m pytest -q '.\phase165_r5_r17_legacy_renderer_retirement\test_installer.py'
if ($LASTEXITCODE -ne 0) { throw 'R5-R17 installer tests failed before deletion.' }
python '.\phase165_r5_r17_legacy_renderer_retirement\install.py'
if ($LASTEXITCODE -ne 0) { throw 'R5-R17 preflight failed; files were not deleted.' }
python -m pytest -q 'tests/test_phase165_r52_r11_common_renderer.py' 'tests/test_phase165_r56_common_renderer.py'
if ($LASTEXITCODE -ne 0) {
    python '.\phase165_r5_r17_legacy_renderer_retirement\restore.py'
    throw 'R5-R17 common Renderer regression failed. Deleted files restored.'
}
Write-Host 'R5-R17 legacy renderer files removed; common Renderer targeted tests PASS. Full pytest NOT run.'
