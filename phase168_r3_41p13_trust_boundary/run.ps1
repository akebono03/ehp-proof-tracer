$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -ItemType Directory -Force -Path $Output | Out-Null
$Installed = $false
Push-Location $Repo
try {
    python -B -m phase168_r3_41p13_trust_boundary.snapshot before
    if ($LASTEXITCODE -ne 0) { throw 'Before snapshot failed' }
    python -B -m phase168_r3_41p13_trust_boundary.install
    if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
    $Installed = $true

    $Tests = @(
        '.\phase168_r3_41p13_trust_boundary\tests\test_phase168_r3_41p13_trust_boundary.py',
        '.\phase168_r3_41p12_publication_boundary_audit\tests\test_publication_gate.py',
        '.\phase166_r3t_goal_source_binding\test_connection.py',
        '.\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py',
        '.\tests\test_phase168_r3_4_link_bridge.py',
        '.\tests\test_phase165_r3_recursive_search.py'
    )
    python -B -m pytest -q --import-mode=importlib @Tests 2>&1 | Tee-Object -FilePath (Join-Path $Output 'pytest_focused.log')
    if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }

    python -B -m phase168_r3_41p13_trust_boundary.snapshot after
    if ($LASTEXITCODE -ne 0) { throw 'Fulltext/Reference/Citation comparison failed' }
    python -B -m phase168_r3_41p12_publication_boundary_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'Publication/fulltext regression audit failed' }
    Write-Host 'R3-41P13 FOCUSED PASS. FULL SUITE NOT RUN.'
    Write-Host "BACKUP $(Join-Path $Output 'web_group_proof.py.before')"
    Write-Host "FULL_FILE $(Join-Path $Output 'web_group_proof.py.FULL.py')"
    $Installed = $false
}
catch {
    Write-Warning $_
    if ($Installed) {
        python -B -m phase168_r3_41p13_trust_boundary.restore
        if ($LASTEXITCODE -ne 0) { throw 'Automatic restore failed; inspect saved backup before retrying' }
    }
    throw
}
finally {
    Pop-Location
}
