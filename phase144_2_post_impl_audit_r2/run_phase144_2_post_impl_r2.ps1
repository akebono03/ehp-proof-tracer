$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditDir = Join-Path $ProjectRoot "phase144_2_post_impl_audit_r2"

$env:PYTHONPATH = $ProjectRoot

try {
    python (Join-Path $AuditDir "audit_phase144_2_post_impl_r2.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-2 post-implementation audit R2 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
