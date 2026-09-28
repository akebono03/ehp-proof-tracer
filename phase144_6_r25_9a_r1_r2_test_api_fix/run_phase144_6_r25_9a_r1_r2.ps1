$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-9A-R1-R2"
Write-Host "Test API repair only"
Write-Host "Production changes in this package: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Verifying both production repairs are already present..."

python -c "from pathlib import Path; s=Path('toda_group_proof_narrative_argument_multi_renderer.py').read_text(encoding='utf-8-sig'); assert 'ESTABLISH_DEFINITION' in s; print('R25-9A frontier source: present')"
if ($LASTEXITCODE -ne 0) {
  throw "R25-9A frontier repair verification failed."
}

python -c "from pathlib import Path; s=Path('toda_group_proof_narrative_argument_body_renderer.py').read_text(encoding='utf-8-sig'); anchor='context_hidden_step_ids is None'; assert s.count(anchor) >= 2; print('R25-9A-R1 relocation hidden filter: present')"
if ($LASTEXITCODE -ne 0) {
  throw "R25-9A-R1 relocation repair verification failed."
}

Write-Host ""
Write-Host "B. Replacing only the broken R25-9A-R1 test..."
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
  Write-Host "C. Running R25-9A-R1-R2 focused tests..."
  pytest -q `
    "tests/test_phase144_6_r25_9a_r1_relocation_hidden.py" `
    "tests/test_phase144_6_r25_9a_pi5_suppression.py" `
    "tests/test_phase144_6_r4_supporting_fact_filtering.py" `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py" `
    "tests/test_phase144_6_r5_15u_evidence_integration.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R25-9A-R1-R2 focused tests failed."
  }

  Write-Host ""
  Write-Host "D. Current production diff..."
  git diff -- `
    "toda_group_proof_narrative_argument_multi_renderer.py" `
    "toda_group_proof_narrative_argument_body_renderer.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-9A-R1-R2 focused tests: PASS"
  Write-Host "Production changes in R2 package: none."
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
