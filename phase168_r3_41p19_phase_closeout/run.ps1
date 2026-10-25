$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -Path $Output -ItemType Directory -Force | Out-Null
$Installed = $false
Push-Location $Repo
try {
    & python -B -m phase168_r3_41p19_phase_closeout.snapshot before
    if ($LASTEXITCODE -ne 0) { throw 'P19 before snapshot failed' }

    & python -B -m phase168_r3_41p19_phase_closeout.install
    if ($LASTEXITCODE -ne 0) { throw 'P19 install failed' }
    $Installed = $true

    # The archived Phase 144 copies have already been retired in Phase 165.
    # Update only three stale reference tests, and remove byte-identical
    # active duplicates after verifying their preserved archive copies.
    & python -B -m phase168_r3_41p19_phase_closeout.active_tests install
    if ($LASTEXITCODE -ne 0) { throw 'Active test migration failed' }

    & python -B -m phase168_r3_41p18_origin_boundary_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'P18 origin audit regression' }

    $Tests = @(
        '.\phase168_r3_41p19_phase_closeout\tests\test_phase168_r3_41p19_phase_closeout.py',
        '.\phase168_r3_41p19_phase_closeout\tests\test_scope_audit.py',
        '.\phase168_r3_41p19_phase_closeout\tests\test_active_test_migration.py',
        '.\tests\test_phase167_r2_range_dedup.py',
        '.\tests\test_phase167_r2_shared_reference.py',
        '.\tests\test_phase167_r2_unified_reference.py',
        '.\phase168_r3_41p18_origin_boundary_audit\tests\test_phase168_r3_41p18_origin_boundary_audit.py',
        '.\phase168_r3_41p17_origin_handoff\tests\test_phase168_r3_41p17_origin_handoff.py',
        '.\phase168_r3_41p15_complete_fail_closed\tests\test_phase168_r3_41p15_complete_fail_closed.py',
        '.\phase168_r3_41p13_trust_boundary\tests\test_phase168_r3_41p13_trust_boundary.py',
        '.\phase168_r3_41p8_trust_boundary_audit\tests\test_phase168_r3_41p8_trust_boundary.py',
        '.\phase168_r3_41p12_publication_boundary_audit\tests\test_publication_gate.py',
        '.\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py',
        '.\tests\test_phase168_r3_4_link_bridge.py',
        '.\tests\test_phase165_r3_recursive_search.py'
    )
    $StdOut = Join-Path $Output 'pytest_focused_stdout.log'
    $StdErr = Join-Path $Output 'pytest_focused_stderr.log'
    & python -B -m pytest -q --import-mode=importlib @Tests 1> $StdOut 2> $StdErr
    $Status = $LASTEXITCODE
    Get-Content -LiteralPath $StdOut -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    if ((Test-Path $StdErr) -and (Get-Item $StdErr).Length -gt 0) {
        Get-Content -LiteralPath $StdErr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
    }
    if ($Status -ne 0) { throw "P19 focused pytest failed: $Status" }

    & python -B -m phase168_r3_41p19_phase_closeout.snapshot after
    if ($LASTEXITCODE -ne 0) { throw 'P19 fulltext/Reference/Citation regression' }
    & python -B -m phase168_r3_41p12_publication_boundary_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'P19 publication audit regression' }

    # Phase 165 already preserved exact duplicate Phase 144 test sources.
    # With those retired duplicates removed from active tests/, run ALL of
    # remaining tests/ without --ignore, -k or --maxfail filters.
    Write-Host 'PHASE_168_ACTIVE_SUITE_PYTEST_START'
    Write-Host 'PYTEST_SCOPE tests/ (no ignored modules), plus Phase 168 focused regression modules'
    Write-Host 'RETIRED_PHASE144_DUPLICATES_ARCHIVED_IN_PHASE165 2'
    if (-not (Test-Path (Join-Path $Repo 'tests') -PathType Container)) {
        throw 'Active tests/ directory missing; refusing to substitute a narrower suite'
    }
    & python -B -m phase168_r3_41p19_phase_closeout.scope_audit preflight
    if ($LASTEXITCODE -ne 0) { throw 'preflight import boundary diagnosis failed' }
    $FullOut = Join-Path $Output 'pytest_full_stdout.log'
    $FullErr = Join-Path $Output 'pytest_full_stderr.log'
    & python -B -m pytest tests -q --tb=short --continue-on-collection-errors 1> $FullOut 2> $FullErr
    $FullStatus = $LASTEXITCODE
    Get-Content -LiteralPath $FullOut -Encoding UTF8 | Select-Object -Last 85 | ForEach-Object { Write-Host $_ }
    if ((Test-Path $FullErr) -and (Get-Item $FullErr).Length -gt 0) {
        Get-Content -LiteralPath $FullErr -Encoding UTF8 | Select-Object -Last 35 | ForEach-Object { Write-Warning $_ }
    }
    & python -B -m phase168_r3_41p19_phase_closeout.scope_audit after --pytest-code $FullStatus
    if ($LASTEXITCODE -ne 0) { throw 'active suite diagnosis report failed' }
    $StatusFile = Join-Path $Output 'active_suite_diagnostics.json'
    $StatusData = Get-Content -LiteralPath $StatusFile -Raw -Encoding UTF8 | ConvertFrom-Json
    $Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    & python -B -m phase168_r3_41p19_phase_closeout.review_bundle "review_bundle_$Stamp.zip"
    if ($LASTEXITCODE -ne 0) { throw 'review bundle failed' }
    if (-not $StatusData.full_suite_certified) {
        throw "Phase 168 active-suite pytest incomplete: $FullStatus (see $StatusFile and $FullOut)"
    }

    Write-Host 'PHASE_168_FINAL_TESTS_PASS'
    Write-Host 'REFERENCE_TESTS_UPDATED_FOR_COMMON_MODEL_RENDERER 3'
    Write-Host 'RETIRED_DUPLICATES_HAVE_BYTE_IDENTICAL_HISTORICAL_COPIES 2'
    Write-Host 'RENDERER_COMPATIBILITY_GUARDS_RETAINED'
    Write-Host 'ORIGIN_OBSERVATION_NOT_USED_AS_CERTIFICATE'
    $Installed = $false
}
catch {
    Write-Warning $_
    if (Test-Path (Join-Path $Output 'active_tests_manifest.json')) {
        & python -B -m phase168_r3_41p19_phase_closeout.active_tests restore
        if ($LASTEXITCODE -ne 0) { throw 'test migration auto-restore failed; inspect manifest' }
    }
    if ($Installed -or (Test-Path (Join-Path $Output 'manifest.json'))) {
        & python -B -m phase168_r3_41p19_phase_closeout.restore
        if ($LASTEXITCODE -ne 0) { throw 'automatic restore failed; inspect manifest' }
    }
    throw
}
finally {
    Pop-Location
}
