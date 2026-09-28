$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$PatchRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker=Join-Path $ProjectRoot "tests\__init__.py"
$Created=$false
if (-not (Test-Path $Marker)) { New-Item $Marker -ItemType File -Force | Out-Null; $Created=$true }
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"
try {
  Write-Host "Phase 144-6 R13 body-boundary diagnosis R2"
  Write-Host "Production changes: none"
  python (Join-Path $PatchRoot "diagnose_phase144_6_r13_body_boundary_r2.py")
  if ($LASTEXITCODE -ne 0) { throw "R13 R2 diagnosis failed." }
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($Created) { Remove-Item $Marker -Force -ErrorAction SilentlyContinue }
}
