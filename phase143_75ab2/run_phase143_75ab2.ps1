$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  Write-Host "=============================================================================="
  Write-Host "Phase 143-75AB-2 Whitehead correction 26-occurrence cross-audit"
  Write-Host "=============================================================================="

  Write-Host ""
  Write-Host "[1] Canonical first-class structure"
  python ".\phase143_75ab2\audit_phase143_75ab2.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "[2] Current 112-group / 11033-node fallback inventory"
  $inventoryCandidates = @(
    ".\phase143_75u\audit_phase143_75u.py",
    ".\phase143_75u\audit_phase143_75u_remaining_rule_name_fallbacks.py",
    ".\phase143_75t\audit_phase143_75t.py"
  )

  $inventory = $null
  foreach ($candidate in $inventoryCandidates) {
    if (Test-Path $candidate) {
      $inventory = $candidate
      break
    }
  }

  if ($null -eq $inventory) {
    $found = Get-ChildItem `
      -Path "." `
      -Recurse `
      -Filter "audit_phase143_75u*.py" `
      -File `
      -ErrorAction SilentlyContinue |
      Select-Object -First 1

    if ($null -ne $found) {
      $inventory = $found.FullName
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
  Write-Host "Phase 143-75AB-2 completion criteria"
  Write-Host "=============================================================================="
  Write-Host "Confirm in the output:"
  Write-Host "  scanned groups: 112"
  Write-Host "  scanned presentation nodes: 11033"
  Write-Host "  TodaLemma54WhiteheadCorrectionDataStatement: 26 occurrences, 21 groups"
  Write-Host "  rule: 26 x Toda Lemma 5.4 Whitehead correction data"
  Write-Host "  canonical fields:"
  Write-Host "    whitehead_square"
  Write-Host "    sign_parameter"
  Write-Host "    hopf_positive_value"
  Write-Host "    suspension_zero_relation"
  Write-Host "  current semantic rendering: None"
  Write-Host ""
  Write-Host "No source files were changed."
  Write-Host "No pytest was run."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
