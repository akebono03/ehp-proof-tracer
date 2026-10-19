$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python '.\phase165_r6_partial_steps_display\patch.py'
if ($LASTEXITCODE -ne 0) { throw 'Patch verification failed' }
python -m pytest -q '.\phase165_r6_partial_steps_display\test_phase165_r6_partial_steps_display.py' '.\test_phase165_r52_r11_common_renderer.py' '.\test_phase165_r52_partial_proof.py' '.\test_phase165_r52_r3_web_adapter.py'
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
Write-Host 'R6 PARTIAL STEP DISPLAY TARGETED PASS; full pytest NOT run'
