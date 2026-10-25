$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -Path $Output -ItemType Directory -Force | Out-Null
$Installed = $false
Push-Location $Repo
try {
    if (-not (Test-Path '.\phase168_r3_41p13_trust_boundary\verification.py')) {
        throw 'R3-41P13 verifier missing'
    }
    if (-not (Test-Path '.\phase168_r3_41p16_origin_boundary_audit\audit.py')) {
        throw 'R3-41P16 origin audit missing'
    }

    & python -B -m phase168_r3_41p17_origin_handoff.snapshot before
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P17 before snapshot failed' }

    & python -B -m phase168_r3_41p17_origin_handoff.install
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P17 install failed' }
    $Installed = $true

    $Tests = @(
        '.\phase168_r3_41p17_origin_handoff\tests\test_phase168_r3_41p17_origin_handoff.py',
        '.\phase168_r3_41p16_origin_boundary_audit\tests\test_phase168_r3_41p16_origin_boundary_audit.py',
        '.\phase168_r3_41p15_complete_fail_closed\tests\test_phase168_r3_41p15_complete_fail_closed.py',
        '.\phase168_r3_41p13_trust_boundary\tests\test_phase168_r3_41p13_trust_boundary.py',
        '.\phase168_r3_41p12_publication_boundary_audit\tests\test_publication_gate.py',
        '.\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py',
        '.\tests\test_phase164_r8_r2_factory_contract.py',
        '.\tests\test_phase165_r3_recursive_search.py',
        '.\tests\test_phase168_r3_4_link_bridge.py'
    )
    $PytestOut = Join-Path $Output 'pytest_focused_stdout.log'
    $PytestErr = Join-Path $Output 'pytest_focused_stderr.log'
    & python -B -m pytest -q --import-mode=importlib @Tests 1> $PytestOut 2> $PytestErr
    $PytestExit = $LASTEXITCODE
    Get-Content -LiteralPath $PytestOut -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    if ((Test-Path $PytestErr) -and (Get-Item $PytestErr).Length -gt 0) {
        Get-Content -LiteralPath $PytestErr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
    }
    if ($PytestExit -ne 0) { throw "R3-41P17 focused pytest failed: $PytestExit" }

    & python -B -m phase168_r3_41p17_origin_handoff.snapshot after
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P17 fulltext/Reference/Citation comparison failed' }
    & python -B -m phase168_r3_41p12_publication_boundary_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P12 publication regression audit failed' }

    $Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $ReviewZip = "review_bundle_$Stamp.zip"
    & python -B -m phase168_r3_41p17_origin_handoff.review_bundle $ReviewZip
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P17 review bundle failed' }
    Write-Host 'R3-41P17 FOCUSED PASS. FULL_PYTEST_NOT_RUN.'
    Write-Host "REVIEW_BUNDLE $(Join-Path $Output $ReviewZip)"
    Write-Host "BACKUP $(Join-Path $Output 'phase164_r8_proofstep_factory.py.before')"
    Write-Host "BACKUP $(Join-Path $Output 'phase165_r52_r2_search_adapter.py.before')"
    Write-Host 'STANDARD_WEB_PATH_UNCHANGED'
    Write-Host 'RENDERER_GUARDS_RETAINED'
    $Installed = $false
}
catch {
    Write-Warning $_
    if ($Installed -or (Test-Path (Join-Path $Output 'manifest.json'))) {
        & python -B -m phase168_r3_41p17_origin_handoff.restore
        if ($LASTEXITCODE -ne 0) { throw 'R3-41P17 automatic restoration failed' }
    }
    throw
}
finally {
    Pop-Location
}
