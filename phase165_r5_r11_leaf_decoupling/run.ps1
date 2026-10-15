$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python "$PSScriptRoot\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R11 installation aborted' }
$env:PYTHONPATH = $root
python -m pytest -q "$PSScriptRoot\test_r5_r11.py" "test_phase165_r52_r11_common_renderer.py" "test_phase165_r56_common_renderer.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Regression detected; restoring original modules'
    python "$PSScriptRoot\restore.py"
    throw 'R5-R11 regression; changes restored'
}
Write-Host 'R5-R11 targeted tests PASS; legacy Narrative retained; full pytest NOT run.'
