$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    try {
        python -m phase168_r3_41f_inline_step_citations.capture before
        if ($LASTEXITCODE -ne 0) { throw 'R3-41F baseline capture failed' }

        python -m phase168_r3_41f_inline_step_citations.apply
        if ($LASTEXITCODE -ne 0) { throw 'R3-41F renderer patch failed' }

        python -m pytest -q `
            '.\phase168_r3_41f_inline_step_citations\tests\test_phase168_r3_41f_inline_step_citations.py' `
            '.\phase168_r3_41e_certified_prefix_reference_audit\tests\test_phase168_r3_41e_certified_prefix_reference_audit.py' `
            '.\phase168_r3_41d1_boundary_audit_fix\tests\test_phase168_r3_41d1_boundary_audit_fix.py' `
            '.\phase168_r3_41b1_citation_fixture_fix\tests\test_phase168_r3_41b_partial_model_projection.py' `
            '.\phase168_r3_41c1_heading_capture_fix\tests\test_phase168_r3_41c1_heading_capture_fix.py' `
            '.\phase168_r3_5_model_web_boundary\tests\test_phase168_r3_5_model_web_boundary.py' `
            '.\phase168_r3_12_body_binding\tests\test_phase168_r3_12_body_binding.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3-41F limited pytest failed' }

        python -m phase168_r3_41f_inline_step_citations.capture after
        if ($LASTEXITCODE -ne 0) { throw 'R3-41F post-patch capture failed' }
        python -m phase168_r3_41f_inline_step_citations.compare
        if ($LASTEXITCODE -ne 0) { throw 'R3-41F Narrative comparison failed' }
        Write-Host 'R3-41F complete. Full pytest NOT run.'
    }
    catch {
        if (Test-Path (Join-Path $package 'installed_state.json')) {
            python -m phase168_r3_41f_inline_step_citations.apply --rollback
            if ($LASTEXITCODE -ne 0) { throw 'R3-41F rollback failed; backup must be inspected' }
        }
        throw
    }
}
finally {
    Pop-Location
}
