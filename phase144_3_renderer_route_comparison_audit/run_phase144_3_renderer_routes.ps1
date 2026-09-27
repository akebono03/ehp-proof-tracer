$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditDir = Join-Path $ProjectRoot "phase144_3_renderer_route_comparison_audit"

$env:PYTHONPATH = $ProjectRoot

try {
    python (Join-Path $AuditDir "audit_phase144_3_renderer_routes.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-3 renderer route comparison audit failed with exit code $LASTEXITCODE"
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Detailed output:"
Write-Host (Join-Path $AuditDir "output")
