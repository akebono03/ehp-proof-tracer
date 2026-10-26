$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Root = Split-Path -Parent $Package
Set-Location $Root
$env:PYTHONPATH = $Root
$env:PYTHONDONTWRITEBYTECODE = '1'

Write-Host 'Phase 169 R3B: verified finite cyclic suspension transport frontier'
Write-Host 'Git HEAD:'
& git rev-parse --short HEAD
Write-Host '[1/4] Guarded single-production-file replacement'
& python -B "$Package\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host '[2/4] Focused pytest only (no full suite)'
& python -B -m pytest `
    "$Package\tests\test_phase169_r3b_finite_cyclic_suspension.py" `
    '.\phase165_r12_r24_web_search_connection\tests\test_phase165_r12_r24_web_search_connection.py' `
    '.\tests\test_phase165_r12_r5_structure_bridge.py' `
    '.\tests\test_phase165_r3_recursive_search.py' `
    '.\tests\test_phase161_r3_backward_goal_schema.py' `
    -q --tb=short
$TestCode = $LASTEXITCODE
Write-Host "R3B_FOCUSED_PYTEST_EXIT_CODE=$TestCode"
if ($TestCode -ne 0) {
    Write-Warning 'Focused tests failed; attempting guarded restore from reviewed backup.'
    $Backup = Join-Path $Package 'output\phase165_r12_r24_web_search_connection.py.before'
    $Target = Join-Path $Root 'phase165_r12_r24_web_search_connection.py'
    $Full = Join-Path $Package 'full_files\phase165_r12_r24_web_search_connection.py'
    if ((Test-Path $Backup) -and (Test-Path $Full)) {
        $CurrentHash = (Get-FileHash -Algorithm SHA256 $Target).Hash
        $PatchedHash = (Get-FileHash -Algorithm SHA256 $Full).Hash
        if ($CurrentHash -eq $PatchedHash) {
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            Write-Host 'RESTORED: production file from R3B backup.'
        } else {
            Write-Warning 'Target changed after patch; automatic restore skipped to preserve modifications.'
        }
    }
    exit $TestCode
}

Write-Host '[3/4] Actual typed-proof frontier audit'
& python -B "$Package\audit.py"
$AuditCode = $LASTEXITCODE
Write-Host "R3B_AUDIT_EXIT_CODE=$AuditCode"
if ($AuditCode -ne 0) {
    Write-Warning 'Frontier audit failed; attempting guarded restore from reviewed backup.'
    $Backup = Join-Path $Package 'output\phase165_r12_r24_web_search_connection.py.before'
    $Target = Join-Path $Root 'phase165_r12_r24_web_search_connection.py'
    $Full = Join-Path $Package 'full_files\phase165_r12_r24_web_search_connection.py'
    if ((Test-Path $Backup) -and (Test-Path $Full)) {
        $CurrentHash = (Get-FileHash -Algorithm SHA256 $Target).Hash
        $PatchedHash = (Get-FileHash -Algorithm SHA256 $Full).Hash
        if ($CurrentHash -eq $PatchedHash) {
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            Write-Host 'RESTORED: production file from R3B backup.'
        } else {
            Write-Warning 'Target changed after patch; automatic restore skipped.'
        }
    }
    exit $AuditCode
}
Write-Host '[4/4] Completion summary'
Write-Host 'R3B_COMPLETE: one production module, verified proposals only; full suite NOT run.'
