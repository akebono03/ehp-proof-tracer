$ErrorActionPreference = "Stop"
$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host ("=" * 78)
Write-Host "Phase 144-6-R5-15D supporting-evidence minimum depth audit"
Write-Host ("=" * 78)
$env:PYTHONPATH = $repoRoot
try {
    python (Join-Path $scriptDir "audit_phase144_6_r5_15d.py")
    if ($LASTEXITCODE -ne 0) { throw "Phase 144-6-R5-15D audit failed." }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
