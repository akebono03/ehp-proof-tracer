$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditDir = Join-Path $ProjectRoot "phase144_2_definition_relevance_audit"

$env:PYTHONPATH = $ProjectRoot

try {
    python (Join-Path $AuditDir "audit_phase144_2_definition_relevance.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-2 definition relevance audit failed with exit code $LASTEXITCODE"
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
