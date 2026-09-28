$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$PatchRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker=Join-Path $ProjectRoot "tests\__init__.py"
$Created=$false

Write-Host "Phase 144-6 R18 duplicate-owner diagnosis"
Write-Host "Production changes: none"

if (-not (Test-Path $Marker)) {
  New-Item $Marker -ItemType File -Force | Out-Null
  $Created=$true
}
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"
try {
  python (Join-Path $PatchRoot "diagnose_phase144_6_r18_duplicate_owner.py")
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($Created) { Remove-Item $Marker -Force -ErrorAction SilentlyContinue }
}
