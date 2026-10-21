$ErrorActionPreference = 'Stop'
$target = '.\phase166_r3af_goal_source\tests\test_r3af.py'
if (-not (Test-Path $target)) { throw "Missing original test: $target" }
$backupDir = '.\phase166_r3af_test_fixture_fix_backups'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$backup = Join-Path $backupDir ('test_r3af_' + (Get-Date -Format 'yyyyMMddTHHmmss') + '.py')
Copy-Item $target $backup
Copy-Item '.\phase166_r3af_test_fixture_fix\test_r3af.py' $target -Force
Write-Host "PATCHED: $target"
Write-Host "BACKUP: $backup"
python -m pytest -q phase166_r3af_goal_source/tests/test_r3af.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AF focused tests failed' }
Write-Host 'R3-AF focused tests PASS; full pytest NOT run.'
