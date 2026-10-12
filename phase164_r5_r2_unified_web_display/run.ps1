$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$Source = Join-Path $PSScriptRoot 'phase164_r5_r2_common_replay.py'
$Target = Join-Path $Project 'phase164_r5_r2_common_replay.py'
Copy-Item $Source $Target -Force
$TestSource = Join-Path $PSScriptRoot 'tests\test_phase164_r5_r2_unified_web_display.py'
$TestTarget = Join-Path $Project 'tests\test_phase164_r5_r2_unified_web_display.py'
Copy-Item $TestSource $TestTarget -Force
python -B (Join-Path $PSScriptRoot 'apply_patch.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R2 patch rejected the current source' }
python -B -m pytest -q tests/test_phase164_r5_r2_unified_web_display.py tests/test_phase164_r5_r1_common_renderer.py
if ($LASTEXITCODE -ne 0) { throw 'R5-R2 targeted pytest failed' }
python -B (Join-Path $PSScriptRoot 'sweep_112.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R2 112-target sweep failed' }
Write-Host 'Phase 164 R5-R2 single common Web renderer route installed. Full pytest NOT run.'
