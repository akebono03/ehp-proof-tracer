$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
python -B "$here\apply_phase162_r4_b3_common_renderer_fix.py"
if ($LASTEXITCODE -ne 0) { throw "R4-B3 patch failed" }
python -B -m pytest -q tests/test_phase162_r4_b3_common_renderer_fix.py tests/test_phase162_r4_b2_replay_integration.py
if ($LASTEXITCODE -ne 0) { throw "R4-B3 focused tests failed" }
Write-Host "R4-B3 focused tests complete; public renderer unchanged; full suite not run."
