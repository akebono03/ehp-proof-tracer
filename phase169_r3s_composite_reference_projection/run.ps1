$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
$Modified = $false
try {
    if (-not (Test-Path '.git')) { throw 'Run from an ehp-proof-tracer repository checkout' }
    Write-Host 'R3S: composite source statements into common Reference projection'
    Write-Host 'R3S_AUDIT_ONLY=False; one production function only'
    python -B -m phase169_r3s_composite_reference_projection.install
    if ($LASTEXITCODE -ne 0) { throw 'R3S install failed' }
    $Modified = (Test-Path '.\phase169_r3s_composite_reference_projection\output\phase168_r3_37c_reference_projection.py.before')
    python -B -m pytest -q -p no:cacheprovider '.\phase169_r3s_composite_reference_projection\tests\test_r3s_composite_reference.py' '.\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3S focused reference tests failed' }
    Write-Host 'R3S_REFERENCE_TESTS_PASS=True'
    python -B -m pytest -q -p no:cacheprovider '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3S 1-stem regression failed' }
    Write-Host 'R3S_ONE_STEM_PASS=True'
    Write-Host 'R3S_COMPLETE: full suite NOT run; (5.1) proof prerequisite remains outside scope'
}
catch {
    if ($Modified) {
        python -B -c 'from phase169_r3s_composite_reference_projection.install import restore; restore()'
        if ($LASTEXITCODE -ne 0) { throw 'R3S automatic restore failed' }
    }
    throw
}
finally {
    Pop-Location
}
