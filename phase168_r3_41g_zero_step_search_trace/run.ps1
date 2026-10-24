$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m pytest -q '.\phase168_r3_41g_zero_step_search_trace\tests\test_phase168_r3_41g_zero_step_search_trace.py' `
        '.\phase168_r3_41c1_heading_capture_fix\tests\test_phase168_r3_41c1_heading_capture_fix.py' `
        '.\phase168_r3_41e_certified_prefix_reference_audit\tests\test_phase168_r3_41e_certified_prefix_reference_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41G limited pytest failed' }

    python -m phase168_r3_41g_zero_step_search_trace.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41G read-only real search audit failed' }

    Write-Host 'R3-41G complete. No implementation files modified. Full pytest NOT run.'
}
finally {
    Pop-Location
}
