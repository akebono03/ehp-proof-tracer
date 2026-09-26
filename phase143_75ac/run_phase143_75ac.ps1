$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  Write-Host "=============================================================================="
  Write-Host "Phase 143-75AC Hopf odd multiple 20-occurrence cross-audit"
  Write-Host "=============================================================================="

  Write-Host ""
  Write-Host "[1] Canonical first-class structure"
  python ".\phase143_75ac\audit_phase143_75ac.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "[2] Current 112-group / 11033-node fallback inventory"

  $inventoryCandidates = @(
    ".\phase143_75u\audit_phase143_75u_remaining_fallbacks.py",
    ".\phase143_75u\audit_phase143_75u.py"
  )

  $inventory = $null
  foreach ($candidate in $inventoryCandidates) {
    if (Test-Path $candidate) {
      $inventory = $candidate
      break
    }
  }

  if ($null -eq $inventory) {
    throw "Could not locate the Phase 143-75U remaining-fallback audit."
  }

  Write-Host ("inventory audit: " + $inventory)
  python $inventory
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "=============================================================================="
  Write-Host "Phase 143-75AC audit criteria"
  Write-Host "=============================================================================="
  Write-Host "Confirm:"
  Write-Host "  scanned groups: 112"
  Write-Host "  scanned presentation nodes: 11033"
  Write-Host "  current total fallback count: 236"
  Write-Host "  TodaLemma54HopfOddMultipleStatement: 20 occurrences, 18 groups"
  Write-Host "  20 x Toda 4.8 Lemma 5.4 Hopf odd multiple"
  Write-Host "  canonical fields: alpha_star, parameter, generator"
  Write-Host "  current semantic rendering: None"
  Write-Host ""
  Write-Host "No source files were changed."
  Write-Host "No pytest was run."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
