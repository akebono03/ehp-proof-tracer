$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
Push-Location $Repo
$Installed = $false
try {
    Write-Host 'Phase 169 R3U1: certified (5.1) domain prerequisite for Delta injectivity'
    Write-Host 'Scope: one source function and corresponding R3I contract tests in three prior test copies'
    python -B "$Package\install.py" install
    if ($LASTEXITCODE -ne 0) { throw 'R3U1 guarded installation failed' }
    $Installed = $true
    python -B -m pytest -q "$Package\tests\test_phase169_r3u_delta_diagonal_dependency.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3U1 new typed-proof tests failed' }
    Write-Host 'R3U1_NEW_TESTS_PASS=True'
    $R3ITests = @(
        '.\phase169_r3i_cited_ehp_inference\tests\test_phase169_r3i_cited_ehp_inference.py',
        '.\phase169_r3i1_proof_closure_audit\tests\test_phase169_r3i_cited_ehp_inference.py',
        '.\phase169_r3i2_import_repair\tests\test_phase169_r3i_cited_ehp_inference.py'
    )
    foreach ($TestPath in $R3ITests) {
        python -B -m pytest -q $TestPath
        if ($LASTEXITCODE -ne 0) { throw "R3U1 R3I contract tests failed: $TestPath" }
    }
    Write-Host 'R3U1_R3I_COMPATIBILITY_PASS=True'
    python -B -m pytest -q '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3U1 1-stem regression tests failed' }
    Write-Host 'R3U1_ONE_STEM_PASS=True'
    python -B "$Package\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3U1 actual Web/Proof Tree audit failed' }
    Write-Host 'R3U1_COMPLETE=True; full pytest NOT run'
    $Installed = $false
}
catch {
    Write-Warning $_
    if ($Installed) {
        python -B "$Package\install.py" restore
        if ($LASTEXITCODE -ne 0) { throw 'R3U1 automatic restore failed: inspect output backups' }
    }
    throw
}
finally {
    Pop-Location
}
