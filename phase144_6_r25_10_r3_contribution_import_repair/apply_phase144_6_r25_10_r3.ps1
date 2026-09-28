$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$Target = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit\audit_phase144_6_r25_10.py"

if (-not (Test-Path $Target)) {
  throw "R25-10 audit script not found: $Target"
}

$Text = Get-Content -Raw -Encoding UTF8 $Target

$Old = "from toda_group_proof_narrative_contributions import build_toda_group_proof_narrative_ordered_contributions"
$New = "from toda_group_proof_narrative_contribution_ordering import build_toda_group_proof_narrative_ordered_contributions"

if (-not $Text.Contains($Old)) {
  if ($Text.Contains($New)) {
    Write-Host "R25-10-R3 import repair is already applied."
    exit 0
  }
  throw "Expected obsolete contribution import was not found."
}

$Text = $Text.Replace($Old, $New)

Set-Content `
  -Path $Target `
  -Value $Text `
  -Encoding UTF8

Write-Host "R25-10-R3 contribution-ordering import repair applied."
Write-Host "Production changes: none."
Write-Host "Existing tests changed: none."
