$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$target = Join-Path $repo 'phase165_r3_recursive_search.py'
$source = Join-Path $repo 'phase166_r3_lookup_gate_fix\backups\phase165_r3_recursive_search_20261019T150915Z.py'
if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw "Target not found: $target" }
if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Original backup not found: $source. No changes made." }
$timestamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$rollbackDir = Join-Path $PSScriptRoot 'backups'
New-Item -ItemType Directory -Path $rollbackDir -Force | Out-Null
$preRollback = Join-Path $rollbackDir "phase165_r3_recursive_search_before_rollback_$timestamp.py"
Copy-Item -LiteralPath $target -Destination $preRollback -ErrorAction Stop
$originalHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
Copy-Item -LiteralPath $source -Destination $target -Force -ErrorAction Stop
$restoredHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
if ($restoredHash -ne $originalHash) { throw 'Restored file hash mismatch' }
Write-Host "RESTORED: $target"
Write-Host "SOURCE: $source"
Write-Host "PRE-ROLLBACK BACKUP: $preRollback"
Write-Host "SHA256: $restoredHash"
Push-Location $repo
try {
  python -m py_compile '.\phase165_r3_recursive_search.py'
  if ($LASTEXITCODE -ne 0) { throw 'Python compile failed after restoration' }
  Write-Host 'Rollback file restored and syntax checked. Full pytest NOT run.'
  Write-Host 'NOTE: This reverts the R3 citation gate change and its security restrictions; proof restoration is not yet verified.'
} finally { Pop-Location }
