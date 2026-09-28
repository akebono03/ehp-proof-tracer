$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$PatchRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"
try {
  Write-Host "Phase 144-6 R12 compact argument diagnosis"
  Write-Host "Production changes: none"
  python (Join-Path $PatchRoot "diagnose_phase144_6_r12.py")
  if ($LASTEXITCODE -ne 0) { throw "R12 diagnosis failed." }
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
