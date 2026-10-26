$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -ItemType Directory -Force -Path $Output | Out-Null
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run R3S1 from its parent repository.' }
    Write-Host 'Phase 169 R3S1: inherited composite scope repair'
    Write-Host 'Only project_reference_bodies() is changed; proof, search, registry unchanged'
    python -B -m phase169_r3s1_composite_scope_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R3S1 guarded installation failed' }

    $Tests = @(
        '.\phase169_r3s1_composite_scope_fix\tests\test_r3s1_composite_scope.py',
        '.\phase169_r3s_composite_reference_projection\tests\test_r3s_composite_reference.py',
        '.\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py'
    )
    python -B -m pytest -q -p no:cacheprovider @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R3S1 reference tests failed' }
    Write-Host 'R3S1_REFERENCE_TESTS_PASS=True'

    python -B -m pytest -q -p no:cacheprovider '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3S1 1-stem regression failed' }
    Write-Host 'R3S1_ONE_STEM_TESTS_PASS=True'
    Write-Host 'R3S1_COMPLETE=True; full pytest NOT run'
}
catch {
    $Backup = Join-Path $Output 'phase168_r3_37c_reference_projection.py.before'
    if (Test-Path $Backup) {
        python -B -c 'from phase169_r3s1_composite_scope_fix.install import restore; restore()'
        if ($LASTEXITCODE -ne 0) { throw 'R3S1 restore failed: inspect backup' }
    }
    throw
}
finally {
    Pop-Location
}
