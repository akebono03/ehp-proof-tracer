$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -ItemType Directory -Force -Path $Output | Out-Null
Push-Location $Repo
try {
    Write-Host 'R3-41P18 AUDIT_ONLY: application modules and existing tests will not be patched.'
    $Watched = @(
        'web_group_proof.py',
        'proof_origin_capture.py',
        'phase164_r8_proofstep_factory.py',
        'phase165_r3_recursive_search.py',
        'phase165_r52_r2_search_adapter.py',
        'phase165_r52_partial_proof.py',
        'phase165_r52_r9_shared_math.py',
        'phase165_r55_nk_only_goal.py',
        'phase168_r3_41p17_origin_handoff/origin_handoff.py',
        'phase168_r3_41p13_trust_boundary/verification.py',
        'phase168_r3_3_proof_narrative_model.py',
        'phase168_r3_4_link_bridge.py',
        'phase168_r3_5_model_renderer.py',
        'phase168_r3_27_typed_statement_projection.py'
    )
    $Before = @{}
    foreach ($Name in $Watched) {
        if (-not (Test-Path -LiteralPath $Name)) {
            throw "Missing prerequisite: $Name"
        }
        $Before[$Name] = (Get-FileHash -LiteralPath $Name -Algorithm SHA256).Hash
    }
    $AuditOut = Join-Path $Output 'audit_stdout.log'
    $AuditErr = Join-Path $Output 'audit_stderr.log'
    & python -B -m phase168_r3_41p18_origin_boundary_audit.audit 1> $AuditOut 2> $AuditErr
    $AuditExit = $LASTEXITCODE
    Get-Content -LiteralPath $AuditOut -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    if ((Test-Path -LiteralPath $AuditErr) -and (Get-Item -LiteralPath $AuditErr).Length -gt 0) {
        Get-Content -LiteralPath $AuditErr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
    }
    if ($AuditExit -ne 0) { throw "R3-41P18 audit failed: $AuditExit" }

    $Tests = @(
        '.\phase168_r3_41p18_origin_boundary_audit\tests\test_phase168_r3_41p18_origin_boundary_audit.py',
        '.\phase168_r3_41p17_origin_handoff\tests\test_phase168_r3_41p17_origin_handoff.py',
        '.\phase168_r3_41p16_origin_boundary_audit\tests\test_phase168_r3_41p16_origin_boundary_audit.py',
        '.\phase168_r3_41p15_complete_fail_closed\tests\test_phase168_r3_41p15_complete_fail_closed.py',
        '.\phase168_r3_41p13_trust_boundary\tests\test_phase168_r3_41p13_trust_boundary.py',
        '.\phase168_r3_41p12_publication_boundary_audit\tests\test_publication_gate.py',
        '.\tests\test_phase164_r8_r2_factory_contract.py',
        '.\tests\test_phase168_r3_4_link_bridge.py'
    )
    $TestOut = Join-Path $Output 'pytest_focused_stdout.log'
    $TestErr = Join-Path $Output 'pytest_focused_stderr.log'
    & python -B -m pytest -q --import-mode=importlib @Tests 1> $TestOut 2> $TestErr
    $TestExit = $LASTEXITCODE
    Get-Content -LiteralPath $TestOut -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    if ((Test-Path -LiteralPath $TestErr) -and (Get-Item -LiteralPath $TestErr).Length -gt 0) {
        Get-Content -LiteralPath $TestErr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
    }
    if ($TestExit -ne 0) { throw "R3-41P18 focused pytest failed: $TestExit" }

    & python -B -m phase168_r3_41p12_publication_boundary_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41P12 publication audit failed' }
    foreach ($Name in $Watched) {
        $After = (Get-FileHash -LiteralPath $Name -Algorithm SHA256).Hash
        if ($After -ne $Before[$Name]) { throw "Watched application file changed: $Name" }
    }
    Write-Host 'APPLICATION_SOURCE_UNCHANGED'
    $Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $Review = Join-Path $Output "review_bundle_$Stamp.zip"
    $Files = @(
        'audit.json', 'audit.md', 'audit_stdout.log', 'audit_stderr.log',
        'pytest_focused_stdout.log', 'pytest_focused_stderr.log'
    )
    $Present = @($Files | ForEach-Object { Join-Path $Output $_ } | Where-Object { Test-Path -LiteralPath $_ })
    Compress-Archive -LiteralPath $Present -DestinationPath $Review -CompressionLevel Optimal -Force
    Write-Host "REVIEW_BUNDLE $Review"
    Write-Host 'R3-41P18 AUDIT COMPLETE. EXPECTED BOUNDARY GAPS DOCUMENTED.'
    Write-Host 'STANDARD_WEB_PATH_UNCHANGED'
    Write-Host 'RENDERER_GUARDS_RETAINED'
    Write-Host 'FULL_PYTEST_NOT_RUN'
}
finally {
    Pop-Location
}
