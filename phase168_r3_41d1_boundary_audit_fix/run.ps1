$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m pytest -q `
        '.\phase168_r3_41d1_boundary_audit_fix\tests\test_phase168_r3_41d1_boundary_audit_fix.py' `
        '.\phase168_r3_5_model_web_boundary\tests\test_phase168_r3_5_model_web_boundary.py' `
        '.\phase168_r3_12_body_binding\tests\test_phase168_r3_12_body_binding.py' `
        '.\phase168_r3_41c1_heading_capture_fix\tests\test_phase168_r3_41c1_heading_capture_fix.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41D1 focused tests failed' }

    python -m phase168_r3_41d1_boundary_audit_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41D1 real-search audit coverage incomplete' }
    Write-Host 'R3-41D1 read-only audit complete. Project implementation untouched. Full pytest NOT run.'
}
finally {
    Pop-Location
}
