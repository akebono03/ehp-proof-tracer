$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
Push-Location $Repo
$Installed = $false
try {
    Write-Host 'Phase 169 R3Y: source-bound Hopf codomain proof'
    python -B "$Package\install.py" install
    if ($LASTEXITCODE -ne 0) { throw 'R3Y guarded installation failed' }
    $Installed = $true
    python -B -m pytest -q "$Package\tests\test_phase169_r3y_hopf_bound_codomain.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3Y new proof tests failed' }
    $Tests = @(
        '.\phase169_r3i_cited_ehp_inference\tests\test_phase169_r3i_cited_ehp_inference.py',
        '.\phase169_r3i1_proof_closure_audit\tests\test_phase169_r3i_cited_ehp_inference.py',
        '.\phase169_r3i2_import_repair\tests\test_phase169_r3i_cited_ehp_inference.py',
        '.\phase169_r3u_delta_diagonal_dependency\tests\test_phase169_r3u_delta_diagonal_dependency.py',
        '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
    )
    foreach ($Test in $Tests) {
        python -B -m pytest -q $Test
        if ($LASTEXITCODE -ne 0) { throw "R3Y regression failed: $Test" }
    }
    Write-Host 'R3Y_LIMITED_TESTS_PASS=True'
    python -B -m phase169_r3y_hopf_bound_codomain.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3Y actual proof and references audit failed' }
    Write-Host 'R3Y_COMPLETE=True; full pytest NOT run'
    $Installed = $false
}
catch {
    Write-Warning $_
    if ($Installed) {
        python -B "$Package\install.py" restore
        if ($LASTEXITCODE -ne 0) { throw 'R3Y restore failed: inspect output backups' }
    }
    throw
}
finally {
    Pop-Location
}
