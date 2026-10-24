param([switch]$SkipTests)
$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -Path $Output -ItemType Directory -Force | Out-Null
Push-Location $Repo
try {
    Write-Host 'R3-41P16 AUDIT_ONLY: application source and existing tests are unchanged.'
    if (-not (Test-Path '.\phase168_r3_41p15_complete_fail_closed\tests\test_phase168_r3_41p15_complete_fail_closed.py')) {
        throw 'R3-41P15 files missing. Apply Phase 168 R3-41P15 before this audit.'
    }
    if (-not (Test-Path '.\phase168_r3_41p14_trust_boundary_audit\audit.py')) {
        throw 'R3-41P14 original audit module missing.'
    }
    $Watched = @(
        'web_group_proof.py',
        'phase165_r3_recursive_search.py',
        'phase165_r52_r2_search_adapter.py',
        'phase165_r52_r9_shared_math.py',
        'phase168_r3_3_proof_narrative_model.py',
        'phase168_r3_5_model_renderer.py',
        'phase168_r3_27_typed_statement_projection.py',
        'phase168_r3_41p13_trust_boundary/verification.py'
    )
    $Before = @{}
    foreach ($Path in $Watched) {
        $Before[$Path] = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
    }
    $AuditOut = Join-Path $Output 'audit_stdout.log'
    $AuditErr = Join-Path $Output 'audit_stderr.log'
    & python -B -m phase168_r3_41p16_origin_boundary_audit.audit 1> $AuditOut 2> $AuditErr
    $AuditExit = $LASTEXITCODE
    Get-Content -LiteralPath $AuditOut -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    if ((Test-Path $AuditErr) -and (Get-Item $AuditErr).Length -gt 0) {
        Get-Content -LiteralPath $AuditErr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
    }
    if ($AuditExit -ne 0) { throw "R3-41P16 origin audit failed: $AuditExit" }

    if (-not $SkipTests) {
        $Tests = @(
            '.\phase168_r3_41p16_origin_boundary_audit\tests\test_phase168_r3_41p16_origin_boundary_audit.py',
            '.\phase168_r3_41p15_complete_fail_closed\tests\test_phase168_r3_41p15_complete_fail_closed.py',
            '.\phase168_r3_41p14_trust_boundary_audit\tests\test_phase168_r3_41p14_trust_boundary_audit.py',
            '.\phase168_r3_41p13_trust_boundary\tests\test_phase168_r3_41p13_trust_boundary.py',
            '.\tests\test_phase165_r3_recursive_search.py',
            '.\tests\test_phase168_r3_4_link_bridge.py'
        )
        $PytestOut = Join-Path $Output 'pytest_focused_stdout.log'
        $PytestErr = Join-Path $Output 'pytest_focused_stderr.log'
        & python -B -m pytest -q --import-mode=importlib @Tests 1> $PytestOut 2> $PytestErr
        $TestExit = $LASTEXITCODE
        Get-Content -LiteralPath $PytestOut -Encoding UTF8 | ForEach-Object { Write-Host $_ }
        if ((Test-Path $PytestErr) -and (Get-Item $PytestErr).Length -gt 0) {
            Get-Content -LiteralPath $PytestErr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
        }
        if ($TestExit -ne 0) { throw "R3-41P16 focused pytest failed: $TestExit" }
    }

    foreach ($Path in $Watched) {
        $After = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
        if ($After -ne $Before[$Path]) {
            throw "A watched application file changed: $Path"
        }
    }
    $Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $Review = Join-Path $Output "review_bundle_$Stamp.zip"
    $Names = @('audit.json', 'audit.md', 'audit_stdout.log', 'audit_stderr.log',
               'pytest_focused_stdout.log', 'pytest_focused_stderr.log',
               'pi3_2_current.md', 'pi3_2_reference.txt', 'pi3_2_proof.txt',
               'pi4_3_current.md', 'pi4_3_reference.txt', 'pi4_3_proof.txt',
               'pi5_4_current.md', 'pi5_4_reference.txt', 'pi5_4_proof.txt')
    $Present = @($Names | ForEach-Object { Join-Path $Output $_ } | Where-Object { Test-Path -LiteralPath $_ })
    if ($Present.Count -gt 0) {
        Compress-Archive -LiteralPath $Present -DestinationPath $Review -CompressionLevel Optimal
        Write-Host "REVIEW_BUNDLE $Review"
    }
    Write-Host 'R3-41P16 AUDIT COMPLETE. No application source changed.'
    Write-Host 'FULL_PYTEST_NOT_RUN'
}
finally {
    Pop-Location
}
