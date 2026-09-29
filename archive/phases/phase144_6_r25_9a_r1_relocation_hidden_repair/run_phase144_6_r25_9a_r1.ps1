$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-9A-R1"
Write-Host "Relocated hidden-step repair"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Verifying R25-9A frontier repair is present..."
$FrontierSource = Get-Content `
  "toda_group_proof_narrative_argument_multi_renderer.py" `
  -Raw
$Expected = @"
  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    for proof_step in direct_premise_steps:
"@
if (-not $FrontierSource.Contains($Expected)) {
  throw "R25-9A frontier repair is not present."
}
Write-Host "R25-9A frontier repair: present"

Write-Host ""
Write-Host "B. Verifying R25-8 remains rolled back..."
git diff --quiet HEAD -- "toda_upstream_bootstrap.py"
if ($LASTEXITCODE -ne 0) {
  throw "toda_upstream_bootstrap.py differs from HEAD."
}
Write-Host "toda_upstream_bootstrap.py : HEAD"

Write-Host ""
Write-Host "C. Applying relocation hidden-step repair..."
python (Join-Path $PatchRoot "apply_phase144_6_r25_9a_r1.py")
if ($LASTEXITCODE -ne 0) {
  throw "R25-9A-R1 apply failed."
}

Copy-Item `
  (Join-Path $PatchRoot "test_phase144_6_r25_9a_r1_relocation_hidden.py") `
  (Join-Path $ProjectRoot "tests\test_phase144_6_r25_9a_r1_relocation_hidden.py") `
  -Force

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "D. Running R25-9A-R1 focused tests..."
  pytest -q `
    "tests/test_phase144_6_r25_9a_r1_relocation_hidden.py" `
    "tests/test_phase144_6_r25_9a_pi5_suppression.py" `
    "tests/test_phase144_6_r4_supporting_fact_filtering.py" `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py" `
    "tests/test_phase144_6_r5_15u_evidence_integration.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R25-9A-R1 focused tests failed."
  }

  Write-Host ""
  Write-Host "E. Production diff..."
  git diff -- `
    "toda_group_proof_narrative_argument_multi_renderer.py" `
    "toda_group_proof_narrative_argument_body_renderer.py" `
    "tests/test_phase144_6_r25_9a_pi5_suppression.py" `
    "tests/test_phase144_6_r25_9a_r1_relocation_hidden.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-9A-R1 focused repair completed."
  Write-Host "nu-prime depth=2 repair was NOT attempted."
  Write-Host "Full suite intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
