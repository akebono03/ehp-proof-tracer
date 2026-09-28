$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Phase 144-6 R20 local multi-renderer context capture"
Write-Host "Production changes: none"
Write-Host ""

python (Join-Path $PatchRoot "capture_phase144_6_r20_local_multi_context.py")
if ($LASTEXITCODE -ne 0) {
  throw "R20 local context capture failed."
}
