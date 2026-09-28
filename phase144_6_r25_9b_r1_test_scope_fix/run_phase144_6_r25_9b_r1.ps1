$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-9B-R1"
Write-Host "Focused test scope fix only"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Verifying R25-9B production repair is already present..."
python -c "from pathlib import Path; s=Path('toda_group_proof_narrative_semantics.py').read_text(encoding='utf-8-sig'); assert 'def build_toda_group_proof_narrative_semantic_closure_presentation(' in s; r=Path('toda_group_proof_narrative_renderer.py').read_text(encoding='utf-8-sig'); assert 'build_toda_group_proof_narrative_semantic_closure_presentation(' in r; print('R25-9B production repair: present')"
if ($LASTEXITCODE -ne 0) {
  throw "R25-9B production repair is missing."
}

Write-Host ""
Write-Host "B. Replacing only the over-specified R25-9B test..."
Copy-Item `
  (Join-Path $PatchRoot "test_phase144_6_r25_9b_nu_prime_definition_depth2.py") `
  (Join-Path $ProjectRoot "tests\test_phase144_6_r25_9b_nu_prime_definition_depth2.py") `
  -Force

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "C. Running R25-9B completion focused tests..."
  pytest -q `
    "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py" `
    "tests/test_phase144_6_r25_9a_r1_relocation_hidden.py" `
    "tests/test_phase144_6_r25_9a_pi5_suppression.py" `
    "tests/test_phase144_6_r4_supporting_fact_filtering.py" `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py" `
    "tests/test_phase144_6_r5_15u_evidence_integration.py" `
    "tests/test_phase132_9_web_group_proof_modes.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R25-9B-R1 focused tests failed."
  }

  Write-Host ""
  Write-Host "D. Production diff retained from R25-9A/R25-9B..."
  git diff -- `
    "toda_group_proof_narrative_semantics.py" `
    "toda_group_proof_narrative_renderer.py" `
    "toda_group_proof_narrative_argument_multi_renderer.py" `
    "toda_group_proof_narrative_argument_body_renderer.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-9B completion focused tests: PASS"
  Write-Host "Production changes in R1: none."
  Write-Host "Full suite intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
