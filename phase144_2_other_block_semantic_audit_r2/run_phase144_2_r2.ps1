$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditDir = Join-Path $ProjectRoot "phase144_2_other_block_semantic_audit_r2"
$AuditScript = Join-Path $AuditDir "audit_phase144_2_r2.py"
$OutputFile = Join-Path $AuditDir "phase144_2_r2_output.txt"

if (-not (Test-Path $AuditScript)) {
    throw "Audit script not found: $AuditScript"
}

Write-Host ("=" * 78)
Write-Host "Phase 144-2 OTHER block / semantic renderer audit R2"
Write-Host ("=" * 78)

$env:PYTHONPATH = $ProjectRoot

try {
    python $AuditScript 2>&1 | Tee-Object -FilePath $OutputFile

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-2 R2 audit failed with exit code $LASTEXITCODE"
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host ("=" * 78)
Write-Host "Phase 144-2 R2 audit complete"
Write-Host "Output: $OutputFile"
Write-Host ("=" * 78)
