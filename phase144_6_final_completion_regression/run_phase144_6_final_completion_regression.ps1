$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$Marker=Join-Path $ProjectRoot "tests\__init__.py"
$Created=$false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Completion Regression"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "=============================================================="

if (-not (Test-Path $Marker)) {
  New-Item $Marker -ItemType File -Force | Out-Null
  $Created=$true
}
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"

$Tests=@(
  ".\tests\test_phase144_6_pi6_generic_production_route.py",
  ".\tests\test_phase144_6_r3_structured_references.py",
  ".\tests\test_phase144_6_r3_production_references.py",
  ".\tests\test_phase144_6_r4_supporting_fact_filtering.py",
  ".\tests\test_phase144_6_r5_18_production_generic_proof_chain_foundation.py",
  ".\tests\test_phase144_6_r5_19_proof_chain_narrative_integration.py",
  ".\tests\test_phase144_6_r5_20_pi6_3_proof_chain_generic_parity.py",
  ".\tests\test_phase143_57c_step_derivation_connector.py",
  ".\tests\test_phase143_61b_direct_premise_narrative.py",
  ".\tests\test_phase143_61b_r_semantic_suppression_priority.py",
  ".\tests\test_phase144_5_generic_definition_order_equations.py"
)

try {
  foreach ($Test in $Tests) {
    if (-not (Test-Path $Test)) {
      throw "Required final regression file not found: $Test"
    }
  }

  pytest -q $Tests
  if ($LASTEXITCODE -ne 0) {
    throw "Phase 144-6 final completion regression failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144-6 final completion regression: PASS"
  Write-Host "=============================================================="
  Write-Host "Completion boundary verified:"
  Write-Host "  - pi_6^3 public Narrative uses generic production route"
  Write-Host "  - structured references remain intact"
  Write-Host "  - supporting-fact frontier filtering remains intact"
  Write-Host "  - Generic ProofChain foundation/integration remains intact"
  Write-Host "  - pi_6^3 generic parity remains intact"
  Write-Host "  - direct-premise relocation has no confirmed duplicates"
  Write-Host "  - Phase 144-5 equation-reference contract remains intact"
  Write-Host ""
  Write-Host "No full pytest was run by this package."
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($Created) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
