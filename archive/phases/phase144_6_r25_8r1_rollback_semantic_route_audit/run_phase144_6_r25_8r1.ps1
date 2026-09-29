$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$R258Test = Join-Path $ProjectRoot "tests\test_phase144_6_r25_8_depth2_definition_provenance.py"
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-8R1 rollback + semantic-route audit"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Rolling back only R25-8 changes..."
git restore --source=HEAD -- "toda_upstream_bootstrap.py"
if ($LASTEXITCODE -ne 0) {
  throw "Failed to restore toda_upstream_bootstrap.py from HEAD."
}

if (Test-Path $R258Test) {
  Remove-Item $R258Test -Force
}

Write-Host "R25-8 production change rolled back."
Write-Host "R25-8 temporary regression test removed."

Write-Host ""
Write-Host "B. Verifying canonical production baseline..."
git diff --exit-code -- `
  "toda_upstream_bootstrap.py" `
  "toda_group_proof_narrative_semantics.py" `
  "toda_group_proof_narrative_arguments.py" `
  "toda_group_proof_narrative_argument_multi_renderer.py"

if ($LASTEXITCODE -ne 0) {
  throw "Canonical production baseline differs from HEAD."
}

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "C. Running semantic-route focused controls..."
  pytest -q `
    "tests/test_phase143_1a_semantic_dependency.py" `
    "tests/test_phase144_6_r4_supporting_fact_filtering.py" `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Semantic-route focused controls failed."
  }

  Write-Host ""
  Write-Host "D. Running R25-8R1 semantic-route audit..."
  python (Join-Path $PatchRoot "audit_phase144_6_r25_8r1.py")

  if ($LASTEXITCODE -ne 0) {
    throw "R25-8R1 semantic-route audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-8R1 completed."
  Write-Host "Production code is back at HEAD."
  Write-Host "No new production repair applied."
  Write-Host "Full suite intentionally not run."
  Write-Host "STOP before the next repair."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
