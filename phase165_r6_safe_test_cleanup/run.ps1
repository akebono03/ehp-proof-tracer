$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$backupTest = Join-Path $root 'tests\test_phase164_r7_statement_resolution.phase164_r7_r1_backup.py'
$activeTest = Join-Path $root 'tests\test_phase164_r7_statement_resolution.py'
$resultDir = Join-Path $root 'phase165_r6_audit_results\safe_test_cleanup'
New-Item -ItemType Directory -Path $resultDir -Force | Out-Null
$reportPath = Join-Path $resultDir 'audit_result.json'
$report = [ordered]@{ phase = '165 R6'; status = 'PENDING'; removed = @(); active_test = 'tests/test_phase164_r7_statement_resolution.py'; full_pytest_run = $false }
try {
    if (-not (Test-Path -LiteralPath $activeTest -PathType Leaf)) { throw 'Active counterpart missing; deletion prohibited.' }
    if (-not (Test-Path -LiteralPath $backupTest -PathType Leaf)) {
        $report.status = 'ALREADY_ABSENT'
        Write-Host 'Backup-named test already absent. No deletion performed.'
    } else {
        $header = (Get-Content -LiteralPath $backupTest -TotalCount 1)
        if ($header -ne '"""Phase 164 R7: synthetic identities only; no mathematical certification."""') { throw 'Backup test signature differs; manual review required.' }
        $fileName = Split-Path -Leaf $backupTest
        $saved = Join-Path $resultDir $fileName
        if (Test-Path -LiteralPath $saved) { throw 'Backup destination already exists; refusing overwrite.' }
        Copy-Item -LiteralPath $backupTest -Destination $saved
        if ((Get-FileHash -LiteralPath $backupTest -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $saved -Algorithm SHA256).Hash) { throw 'Backup verification failed.' }
        Remove-Item -LiteralPath $backupTest -Force
        $report.removed = @('tests/test_phase164_r7_statement_resolution.phase164_r7_r1_backup.py')
        $report.status = 'REMOVED_BACKUP_TEST'
        Write-Host 'Removed one backup-named test after verified backup.'
    }
} catch {
    $report.status = 'BLOCKED'
    $report.error = $_.Exception.Message
    Write-Host "BLOCKED: $($_.Exception.Message)"
} finally {
    $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportPath -Encoding UTF8
    Write-Host "Report: $reportPath"
}
if ($report.status -eq 'BLOCKED') { exit 1 }
Write-Host 'Run targeted regression for the retained active test:'
& python -m pytest -q $activeTest
$testCode = $LASTEXITCODE
if ($testCode -ne 0) { Write-Host "Targeted regression FAILED (exit $testCode). Restore using rollback.ps1 if needed."; exit $testCode }
Write-Host 'Targeted regression PASS; full pytest NOT run; Phase closure PENDING.'
