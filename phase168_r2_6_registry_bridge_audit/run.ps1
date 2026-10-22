$ErrorActionPreference = "Stop"

$Repo = (Get-Location).Path
$AuditDir = Join-Path $Repo "phase168_r2_6_registry_bridge_audit"

if (-not (Test-Path (Join-Path $Repo "phase165_r52_r9_shared_math.py"))) {
    throw "Run this script from the ehp-proof-tracer repository root."
}

Write-Host "R2-6: production code is not modified."
Write-Host "Repository: $Repo"

python -m pytest `
  ".\phase168_r2_6_registry_bridge_audit\tests\test_audit_registry_bridge.py" `
  -q

python -m phase168_r2_6_registry_bridge_audit.audit_registry_bridge

Write-Host ""
Write-Host "R2-6 completed. Inspect:"
Write-Host "  .\phase168_r2_6_registry_bridge_audit\output\registry_bridge_audit.json"
Write-Host "  .\phase168_r2_6_registry_bridge_audit\output\registry_bridge_audit.csv"
