$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m phase168_r3_41b_partial_model_projection.capture before
    if ($LASTEXITCODE -ne 0) { throw 'Before capture failed' }
    python -m phase168_r3_41b_partial_model_projection.apply
    if ($LASTEXITCODE -ne 0) { throw 'R3-41B patch application failed' }
    try {
        python -m pytest -q `
            '.\phase168_r3_41b_partial_model_projection\tests\test_phase168_r3_41b_partial_model_projection.py' `
            '.\phase168_r3_3_narrative_model\tests\test_phase168_r3_3_proof_narrative_model.py' `
            '.\phase168_r3_12_body_binding\tests\test_phase168_r3_12_body_binding.py' `
            '.\phase168_r3_5_model_web_boundary\tests\test_phase168_r3_5_model_web_boundary.py' `
            '.\test_phase165_r52_r3_web_adapter.py' `
            '.\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py' `
            '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3-41B limited pytest failed' }
        python -m phase168_r3_41b_partial_model_projection.capture after
        if ($LASTEXITCODE -ne 0) { throw 'After capture failed' }
        python -m phase168_r3_41b_partial_model_projection.compare
        if ($LASTEXITCODE -ne 0) { throw 'Completed Narrative changed' }
        python -m phase168_r3_41b_partial_model_projection.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3-41B partial-state audit failed' }
        Write-Host 'R3-41B completed. Legacy Web routes untouched. Full pytest NOT run.'
    }
    catch {
        Write-Host 'R3-41B failed; restoring implementation files.'
        python -m phase168_r3_41b_partial_model_projection.apply --rollback
        if ($LASTEXITCODE -ne 0) { throw 'Automatic rollback failed; inspect backup directory' }
        throw
    }
}
finally {
    Pop-Location
}
