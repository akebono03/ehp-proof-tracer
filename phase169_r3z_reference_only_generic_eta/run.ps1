$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
Push-Location $Repo
$Applied = $false
try {
    Write-Host 'Phase 169 R3Z: general higher-eta source only in Reference'
    python -B "$Package\install.py" install
    if ($LASTEXITCODE -ne 0) { throw 'R3Z guarded install failed' }
    $Applied = $true
    python -B -m pytest -q -p no:cacheprovider "$Package\tests\test_r3z_reference_only_generic_eta.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3Z new narrative tests failed' }
    Write-Host 'R3Z_NEW_TESTS_PASS=True'
    $Tests = @(
        '.\phase169_r3y_hopf_bound_codomain\tests\test_phase169_r3y_hopf_bound_codomain.py',
        '.\phase169_r3u_delta_diagonal_dependency\tests\test_phase169_r3u_delta_diagonal_dependency.py',
        '.\phase169_r3i_cited_ehp_inference\tests\test_phase169_r3i_cited_ehp_inference.py',
        '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
    )
    foreach ($Test in $Tests) {
        python -B -m pytest -q -p no:cacheprovider $Test
        if ($LASTEXITCODE -ne 0) { throw "R3Z focused regression failed: $Test" }
    }
    Write-Host 'R3Z_LIMITED_TESTS_PASS=True'
    python -B -m phase169_r3z_reference_only_generic_eta.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3Z actual narrative audit failed' }
    Write-Host 'R3Z_COMPLETE=True; full pytest NOT run'
    $Applied = $false
}
catch {
    Write-Warning $_
    if ($Applied) {
        python -B "$Package\install.py" restore
        if ($LASTEXITCODE -ne 0) { throw 'R3Z restore failed: inspect output backup' }
    }
    throw
}
finally {
    Pop-Location
}
