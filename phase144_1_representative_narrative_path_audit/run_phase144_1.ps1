$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditDir = Join-Path $ProjectRoot "phase144_1_representative_narrative_path_audit"
$AuditScript = Join-Path $AuditDir "audit_phase144_1.py"
$OutputFile = Join-Path $AuditDir "phase144_1_output.txt"

if (-not (Test-Path $AuditScript)) {
    throw "Audit script not found: $AuditScript"
}

Write-Host ("=" * 78)
Write-Host "Phase 144-1 representative Narrative generation path audit"
Write-Host ("=" * 78)

$env:PYTHONPATH = $ProjectRoot

try {
    python $AuditScript 2>&1 | Tee-Object -FilePath $OutputFile

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-1 audit failed with exit code $LASTEXITCODE"
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host ("=" * 78)
Write-Host "Phase 144-1 audit complete"
Write-Host "Output: $OutputFile"
Write-Host ("=" * 78)
