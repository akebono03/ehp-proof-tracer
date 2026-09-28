$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Phase 144-6 R21 local body-renderer context capture"
Write-Host "Production changes: none"
Write-Host ""

python (Join-Path $PatchRoot "capture_phase144_6_r21_local_body_context.py")
if ($LASTEXITCODE -ne 0) {
  throw "R21 local body context capture failed."
}
