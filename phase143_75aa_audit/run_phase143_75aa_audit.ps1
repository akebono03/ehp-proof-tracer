$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Get-Location).Path

try {
  $audit = Get-ChildItem `
    -Path ".\phase143_75z" `
    -Filter "audit_phase143_75z*.py" `
    -File `
    -ErrorAction Stop |
    Select-Object -First 1

  if ($null -eq $audit) {
    throw "Phase 143-75Z audit script was not found under .\phase143_75z."
  }

  Write-Host "=============================================================================="
  Write-Host "Phase 143-75AA completion audit"
  Write-Host "Reusing the Phase 143-75Z population and target audit"
  Write-Host "=============================================================================="
  Write-Host ("audit script: " + $audit.FullName)
  Write-Host ""

  python $audit.FullName

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "Expected after Phase 143-75AA:"
  Write-Host "  scanned groups: 112"
  Write-Host "  scanned presentation nodes: 11033"
  Write-Host "  target occurrences: 26"
  Write-Host "  target rule-name fallbacks: 0"
  Write-Host "  existing statement semantic renderings: 26"
  Write-Host "  errors: 0"
  Write-Host ""
  Write-Host "If these values match, the target-specific completion criterion is satisfied."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
