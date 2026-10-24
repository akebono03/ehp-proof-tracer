$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    try {
        python -m phase168_r3_41b1_citation_fixture_fix.fix_test
        if ($LASTEXITCODE -ne 0) { throw 'R3-41B1 test fixture repair failed' }

        python -m phase168_r3_41b1_citation_fixture_fix.capture before
        if ($LASTEXITCODE -ne 0) { throw 'R3-41B1 pre-patch capture failed' }

        python -m phase168_r3_41b1_citation_fixture_fix.apply
        if ($LASTEXITCODE -ne 0) { throw 'R3-41B1 implementation patch failed' }

        python -m pytest -q `
            '.\phase168_r3_41b1_citation_fixture_fix\tests\test_phase168_r3_41b1_citation_fixture_fix.py' `
            '.\phase168_r3_41b1_citation_fixture_fix\tests\test_phase168_r3_41b_partial_model_projection.py' `
            '.\phase168_r3_3_narrative_model\tests\test_phase168_r3_3_proof_narrative_model.py' `
            '.\phase168_r3_12_body_binding\tests\test_phase168_r3_12_body_binding.py' `
            '.\phase168_r3_5_model_web_boundary\tests\test_phase168_r3_5_model_web_boundary.py' `
            '.\test_phase165_r52_r3_web_adapter.py' `
            '.\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py' `
            '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3-41B1 limited pytest failed' }

        python -m phase168_r3_41b1_citation_fixture_fix.capture after
        if ($LASTEXITCODE -ne 0) { throw 'R3-41B1 post-patch capture failed' }
        python -m phase168_r3_41b1_citation_fixture_fix.compare
        if ($LASTEXITCODE -ne 0) { throw 'Completed Narrative changed' }
        python -m phase168_r3_41b1_citation_fixture_fix.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3-41B1 partial-state audit failed' }
        Write-Host 'R3-41B1 complete. Full pytest NOT run.'
    }
    catch {
        Write-Host 'R3-41B1 failed. Restoring implementation and test files.'
        if (Test-Path (Join-Path $package 'installed_state.json')) {
            python -m phase168_r3_41b1_citation_fixture_fix.apply --rollback
            if ($LASTEXITCODE -ne 0) { throw 'Implementation rollback failed; inspect backup' }
        }
        if (Test-Path (Join-Path $package 'test_fix_state.json')) {
            python -m phase168_r3_41b1_citation_fixture_fix.fix_test --rollback
            if ($LASTEXITCODE -ne 0) { throw 'Test rollback failed; inspect backup' }
        }
        throw
    }
}
finally {
    Pop-Location
}
