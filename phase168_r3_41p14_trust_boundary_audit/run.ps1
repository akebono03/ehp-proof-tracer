param([switch]$SkipTests)
$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -Path $Output -ItemType Directory -Force | Out-Null
Push-Location $Repo
try {
    Write-Host 'R3-41P14 AUDIT_ONLY: no application modules or existing tests will be modified.'
    if (-not (Test-Path '.\phase168_r3_41p13_trust_boundary\verification.py')) {
        throw 'R3-41P13 verification.py missing: install P13 before auditing.'
    }
    $Paths = @(
        'web_group_proof.py',
        'phase168_r3_3_proof_narrative_model.py',
        'phase168_r3_4_link_bridge.py',
        'phase168_r3_27_typed_statement_projection.py',
        'phase168_r3_5_model_renderer.py',
        'phase168_r3_41p13_trust_boundary/verification.py'
    )
    $OriginalHashes = @{}
    foreach ($Path in $Paths) {
        $OriginalHashes[$Path] = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
    }
    $AuditStdout = Join-Path $Output 'audit_stdout.log'
    $AuditStderr = Join-Path $Output 'audit_stderr.log'
    & python -B -m phase168_r3_41p14_trust_boundary_audit.audit 1> $AuditStdout 2> $AuditStderr
    $AuditExit = $LASTEXITCODE
    Get-Content -LiteralPath $AuditStdout -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    if ((Test-Path $AuditStderr) -and (Get-Item $AuditStderr).Length -gt 0) {
        Get-Content -LiteralPath $AuditStderr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
    }
    if ($AuditExit -ne 0) { throw 'R3-41P14 audit failed; inspect output/audit.md' }

    if (-not $SkipTests) {
        $Tests = @(
            '.\phase168_r3_41p14_trust_boundary_audit\tests\test_phase168_r3_41p14_trust_boundary_audit.py',
            '.\phase168_r3_41p13_trust_boundary\tests\test_phase168_r3_41p13_trust_boundary.py',
            '.\phase168_r3_41p12_publication_boundary_audit\tests\test_publication_gate.py',
            '.\tests\test_phase168_r3_4_link_bridge.py',
            '.\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py'
        )
        & python -B -m pytest -q --import-mode=importlib @Tests 2>&1 | Tee-Object -FilePath (Join-Path $Output 'pytest_focused.log')
        if ($LASTEXITCODE -ne 0) { throw 'R3-41P14 focused pytest failed' }
    }
    foreach ($Path in $Paths) {
        $After = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
        if ($After -ne $OriginalHashes[$Path]) {
            throw "Application file changed during audit: $Path"
        }
    }
    $Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $ReviewZip = Join-Path $Output "review_bundle_$Stamp.zip"
    $Names = @('audit.json', 'audit.md', 'audit_stdout.log', 'audit_stderr.log',
               'pytest_focused.log', 'pi3_2_current.md', 'pi4_3_current.md', 'pi5_4_current.md')
    $Present = @($Names | ForEach-Object { Join-Path $Output $_ } | Where-Object { Test-Path $_ })
    if ($Present.Count -gt 0) {
        Compress-Archive -LiteralPath $Present -DestinationPath $ReviewZip -CompressionLevel Optimal
        Write-Host "REVIEW_BUNDLE $ReviewZip"
    }
    Write-Host 'R3-41P14 AUDIT COMPLETE: expected gaps measured, not repaired.'
    Write-Host 'APPLICATION_SOURCE_UNCHANGED'
    Write-Host 'FULL_PYTEST_NOT_RUN'
}
finally {
    Pop-Location
}
