$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
$patched = $false
try {
    try {
        python -m phase168_r3_41c_partial_web_cutover.capture before
        if ($LASTEXITCODE -ne 0) { throw 'R3-41C pre-patch capture failed' }

        python -m phase168_r3_41c_partial_web_cutover.apply
        if ($LASTEXITCODE -ne 0) { throw 'R3-41C patch failed' }
        $patched = $true

        python -m pytest -q `
            '.\phase168_r3_41c_partial_web_cutover\tests\test_phase168_r3_41c_partial_web_cutover.py' `
            '.\phase168_r3_41b1_citation_fixture_fix\tests\test_phase168_r3_41b_partial_model_projection.py' `
            '.\test_phase165_r52_r3_web_adapter.py' `
            '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py' `
            '.\phase168_r3_20_flask_actual_cutover\tests\test_phase168_r3_20_flask_actual_cutover.py' `
            '.\phase168_r3_5_model_web_boundary\tests\test_phase168_r3_5_model_web_boundary.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3-41C limited pytest failed' }

        python -m phase168_r3_41c_partial_web_cutover.capture after
        if ($LASTEXITCODE -ne 0) { throw 'R3-41C post-patch capture failed' }
        python -m phase168_r3_41c_partial_web_cutover.compare
        if ($LASTEXITCODE -ne 0) { throw 'R3-41C compatibility comparison failed' }
        python -m phase168_r3_41c_partial_web_cutover.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3-41C Web narrative audit failed' }
        Write-Host 'R3-41C complete. Full pytest NOT run.'
    }
    catch {
        if ($patched -or (Test-Path (Join-Path $package 'installed_state.json'))) {
            python -m phase168_r3_41c_partial_web_cutover.apply --rollback
            if ($LASTEXITCODE -ne 0) { throw 'R3-41C rollback failed; inspect backup' }
        }
        throw
    }
}
finally {
    Pop-Location
}
