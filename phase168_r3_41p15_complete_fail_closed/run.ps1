$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -Path $Output -ItemType Directory -Force | Out-Null
$Installed = $false
Push-Location $Repo
try {
    if (-not (Test-Path '.\phase168_r3_41p13_trust_boundary\verification.py')) {
        throw 'R3-41P13 trust boundary missing'
    }
    if (-not (Test-Path '.\phase168_r3_41p14_trust_boundary_audit\audit.py')) {
        throw 'R3-41P14 audit package missing'
    }

    & python -B -m phase168_r3_41p15_complete_fail_closed.snapshot before
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P15 before snapshot failed' }

    & python -B -m phase168_r3_41p15_complete_fail_closed.install
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P15 patch installation failed' }
    $Installed = $true

    $Tests = @(
        '.\phase168_r3_41p15_complete_fail_closed\tests\test_phase168_r3_41p15_complete_fail_closed.py',
        '.\phase168_r3_41p14_trust_boundary_audit\tests\test_phase168_r3_41p14_trust_boundary_audit.py',
        '.\phase168_r3_41p13_trust_boundary\tests\test_phase168_r3_41p13_trust_boundary.py',
        '.\phase168_r3_41p12_publication_boundary_audit\tests\test_publication_gate.py',
        '.\phase166_r3t_goal_source_binding\test_connection.py',
        '.\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py',
        '.\tests\test_phase168_r3_4_link_bridge.py',
        '.\tests\test_phase165_r3_recursive_search.py'
    )
    $PytestOut = Join-Path $Output 'pytest_focused_stdout.log'
    $PytestErr = Join-Path $Output 'pytest_focused_stderr.log'
    & python -B -m pytest -q --import-mode=importlib @Tests 1> $PytestOut 2> $PytestErr
    $PytestExit = $LASTEXITCODE
    Get-Content -LiteralPath $PytestOut -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    if ((Test-Path $PytestErr) -and (Get-Item $PytestErr).Length -gt 0) {
        Get-Content -LiteralPath $PytestErr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
    }
    if ($PytestExit -ne 0) { throw "R3-41P15 focused pytest failed: $PytestExit" }

    & python -B -m phase168_r3_41p15_complete_fail_closed.snapshot after
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P15 fulltext/Reference/Citation comparison failed' }
    & python -B -m phase168_r3_41p12_publication_boundary_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P12 publication audit regression' }

    $Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $ReviewZip = "review_bundle_$Stamp.zip"
    & python -B -m phase168_r3_41p15_complete_fail_closed.review_bundle $ReviewZip
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P15 review bundle creation failed' }
    Write-Host 'R3-41P15 FOCUSED PASS; full pytest NOT run.'
    Write-Host "REVIEW_BUNDLE $(Join-Path $Output $ReviewZip)"
    Write-Host "BACKUP $(Join-Path $Output 'web_group_proof.py.before')"
    Write-Host 'RENDERER_GUARDS_RETAINED'
    $Installed = $false
}
catch {
    Write-Warning $_
    $Manifest = Join-Path $Output 'manifest.json'
    if ($Installed -or (Test-Path $Manifest)) {
        & python -B -m phase168_r3_41p15_complete_fail_closed.restore
        if ($LASTEXITCODE -ne 0) { throw 'R3-41P15 automatic restoration failed' }
    }
    throw
}
finally {
    Pop-Location
}
