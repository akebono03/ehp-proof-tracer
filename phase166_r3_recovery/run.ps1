$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$BackupDir = Join-Path $Root 'phase166_r3_order_only_backups'
$Stamp = '20261019T233533Z'
$Main = 'phase165_r3_recursive_search.py'
$Test = 'test_phase165_r52_r15_ordered_citation.py'
$MainBackup = Join-Path $BackupDir ($Main + '.' + $Stamp + '.bak')
$TestBackup = Join-Path $BackupDir ($Test + '.' + $Stamp + '.bak')
$MainTarget = Join-Path $Root $Main
$TestTarget = Join-Path $Root 'phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py'
if (-not (Test-Path $MainBackup)) { throw "Original backup not found: $MainBackup" }
if (-not (Test-Path $TestBackup)) { throw "Original test backup not found: $TestBackup" }
if (-not (Test-Path $MainTarget) -or -not (Test-Path $TestTarget)) { throw 'Target file missing' }
$Head = Get-Content -Path $MainTarget -Raw -Encoding UTF8
if ($Head -notmatch 'Eligibility depends on source order') { throw 'Current search file does not match R3 order-only patch: refusing unsafe rollback' }
$Recovery = Join-Path $Root 'phase166_r3_recovery_backups'
New-Item -ItemType Directory -Path $Recovery -Force | Out-Null
$Time = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
Copy-Item $MainTarget (Join-Path $Recovery ($Main + '.' + $Time + '.before_restore'))
Copy-Item $TestTarget (Join-Path $Recovery ($Test + '.' + $Time + '.before_restore'))
Copy-Item $MainBackup $MainTarget -Force
Copy-Item $TestBackup $TestTarget -Force
if ((Get-FileHash $MainBackup -Algorithm SHA256).Hash -ne (Get-FileHash $MainTarget -Algorithm SHA256).Hash) { throw 'Main restore hash mismatch' }
if ((Get-FileHash $TestBackup -Algorithm SHA256).Hash -ne (Get-FileHash $TestTarget -Algorithm SHA256).Hash) { throw 'Test restore hash mismatch' }
Write-Host 'RESTORED: R3 order-only patch reverted (main and existing test)'
Set-Location $Root
python -m pytest -q tests/test_phase165_r3_recursive_search.py phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
Write-Host 'Targeted tests PASS. Full pytest NOT run.'
Write-Host 'Please re-check Web pi_3^2; recovery is NOT established until the actual Web proof is verified.'
