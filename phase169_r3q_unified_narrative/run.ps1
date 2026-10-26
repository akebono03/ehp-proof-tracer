$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Applied = $false
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run within ehp-proof-tracer repository root.' }
    Write-Host 'Phase 169 R3Q: one common proof-reason renderer'
    Write-Host 'Scope: typed map sentence and model renderer only; no proof/search/registry edits'
    python -B -m phase169_r3q_unified_narrative.apply
    if ($LASTEXITCODE -ne 0) { throw 'R3Q guarded installation failed' }
    $Applied = $true

    $Focused = @('.\phase169_r3q_unified_narrative\tests\test_phase169_r3q_unified_narrative.py')
    python -B -m pytest -q @Focused
    if ($LASTEXITCODE -ne 0) { throw 'R3Q focused pytest failed' }
    Write-Host 'R3Q_FOCUSED_PYTEST_PASS=True'

    python -B -m pytest -q '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3Q 1-stem regression failed' }
    Write-Host 'R3Q_ONE_STEM_PYTEST_PASS=True'

    python -B -m pytest -q '.\phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3Q 2-stem regression failed' }
    Write-Host 'R3Q_TWO_STEM_PYTEST_PASS=True'
    Write-Host 'R3Q_COMPLETE: limited tests only; full pytest not run.'
    $Applied = $false
} catch {
    Write-Warning $_
    if ($Applied) {
        python -B -m phase169_r3q_unified_narrative.restore
        if ($LASTEXITCODE -ne 0) { throw 'R3Q rollback failed; inspect output/*.before.' }
    }
    throw
} finally {
    Pop-Location
}
