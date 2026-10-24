$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m pytest -q '.\phase168_r3_41h_finite_cyclic_blocker_audit\tests\test_phase168_r3_41h_finite_cyclic_blocker_audit.py' `
        '.\phase168_r3_41g_zero_step_search_trace\tests\test_phase168_r3_41g_zero_step_search_trace.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41H limited pytest failed' }

    python -m phase168_r3_41h_finite_cyclic_blocker_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41H read-only audit failed' }

    Write-Host 'R3-41H read-only audit complete. Full pytest NOT run.'
}
finally {
    Pop-Location
}
