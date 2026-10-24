$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m pytest -q `
        '.\phase168_r3_41d_live_partial_reference_audit\tests\test_phase168_r3_41d_live_partial_reference_audit.py' `
        '.\phase168_r3_5_model_web_boundary\tests\test_phase168_r3_5_model_web_boundary.py' `
        '.\phase168_r3_12_body_binding\tests\test_phase168_r3_12_body_binding.py' `
        '.\phase168_r3_41c1_heading_capture_fix\tests\test_phase168_r3_41c1_heading_capture_fix.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41D focused tests failed' }

    python -m phase168_r3_41d_live_partial_reference_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41D read-only live audit failed' }

    Write-Host 'R3-41D read-only audit complete. No production code modified. Full pytest NOT run.'
}
finally {
    Pop-Location
}
