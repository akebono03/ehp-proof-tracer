$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-9B"
Write-Host "nu-prime definition depth=2 selection repair"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Verifying R25-9A production repairs remain present..."
python -c "from pathlib import Path; s=Path('toda_group_proof_narrative_argument_multi_renderer.py').read_text(encoding='utf-8-sig'); assert 'ESTABLISH_DEFINITION' in s; print('R25-9A frontier repair: present')"
if ($LASTEXITCODE -ne 0) {
  throw "R25-9A frontier repair is missing."
}
python -c "from pathlib import Path; s=Path('toda_group_proof_narrative_argument_body_renderer.py').read_text(encoding='utf-8-sig'); assert s.count('context_hidden_step_ids is None') >= 2; print('R25-9A relocation hidden filter: present')"
if ($LASTEXITCODE -ne 0) {
  throw "R25-9A relocation repair is missing."
}

Write-Host ""
Write-Host "B. Verifying upstream proof construction remains HEAD..."
git diff --quiet HEAD -- "toda_upstream_bootstrap.py"
if ($LASTEXITCODE -ne 0) {
  throw "toda_upstream_bootstrap.py differs from HEAD."
}
Write-Host "toda_upstream_bootstrap.py : HEAD"

Write-Host ""
Write-Host "C. Applying R25-9B semantic selection closure..."
python (Join-Path $PatchRoot "apply_phase144_6_r25_9b.py")
if ($LASTEXITCODE -ne 0) {
  throw "R25-9B apply failed."
}

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
  Write-Host "D. Running R25-9B focused tests..."
  pytest -q `
    "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py" `
    "tests/test_phase144_6_r25_9a_r1_relocation_hidden.py" `
    "tests/test_phase144_6_r25_9a_pi5_suppression.py" `
    "tests/test_phase144_6_r4_supporting_fact_filtering.py" `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py" `
    "tests/test_phase144_6_r5_15u_evidence_integration.py" `
    "tests/test_phase132_9_web_group_proof_modes.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R25-9B focused tests failed."
  }

  Write-Host ""
  Write-Host "E. Production diff..."
  git diff -- `
    "toda_group_proof_narrative_semantics.py" `
    "toda_group_proof_narrative_renderer.py" `
    "toda_group_proof_narrative_argument_multi_renderer.py" `
    "toda_group_proof_narrative_argument_body_renderer.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-9B focused repair completed."
  Write-Host "Source replay depth remains unchanged."
  Write-Host "Trace/Outline production paths were not changed."
  Write-Host "Full suite intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
