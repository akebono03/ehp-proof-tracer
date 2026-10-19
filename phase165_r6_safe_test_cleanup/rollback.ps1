$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$source = Join-Path $root 'phase165_r6_audit_results\safe_test_cleanup\test_phase164_r7_statement_resolution.phase164_r7_r1_backup.py'
$destination = Join-Path $root 'tests\test_phase164_r7_statement_resolution.phase164_r7_r1_backup.py'
if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw 'Saved backup not found.' }
if (Test-Path -LiteralPath $destination) { throw 'Destination exists; refusing overwrite.' }
Copy-Item -LiteralPath $source -Destination $destination
if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash) { throw 'Restore verification failed.' }
Write-Host 'Restored the original backup-named test.'
