$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Target = Join-Path $Root 'phase165_r3_recursive_search.py'
$Backup = Join-Path $Root 'phase166_r3c_ordered_search\backups\phase165_r3_recursive_search.py.20261020T024237Z.bak'
if (-not (Test-Path -LiteralPath $Backup -PathType Leaf)) { throw "Expected R3-C backup not found. No changes made: $Backup" }
if (-not (Test-Path -LiteralPath $Target -PathType Leaf)) { throw "Target missing. No changes made: $Target" }
$Current = Get-Content -LiteralPath $Target -Raw -Encoding UTF8
if ($Current -notmatch 'R3-C: one ordered fixed-reference lookup') { throw 'Current search is not the R3-C version. No changes made.' }
$Stored = Get-Content -LiteralPath $Backup -Raw -Encoding UTF8
if ($Stored -notmatch 'def reconstruct_registered_goal\(' -or $Stored -notmatch 'def _typed_reference_steps\(') { throw 'Backup content invalid. No changes made.' }
$Saved = Join-Path $PSScriptRoot 'phase165_r3_recursive_search_before_restore.py.bak'
Copy-Item -LiteralPath $Target -Destination $Saved -Force
Copy-Item -LiteralPath $Backup -Destination $Target -Force
$ActualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Target).Hash
$ExpectedHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Backup).Hash
if ($ActualHash -ne $ExpectedHash) { Copy-Item -LiteralPath $Saved -Destination $Target -Force; throw 'Restored file checksum mismatch: rolled back' }
Push-Location $Root
try {
  python -m pytest -q tests/test_phase165_r3_recursive_search.py
  if ($LASTEXITCODE -ne 0) { throw 'Existing focused recursive search tests failed' }
  Write-Host 'R3-C ROLLED BACK; focused tests PASS; full pytest NOT run.'
  Write-Host 'Please recheck Web pi_3^2 narrative; rollback alone does not certify proof restoration.'
} finally { Pop-Location }
