$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$R258Test = Join-Path $ProjectRoot "tests\test_phase144_6_r25_8_depth2_definition_provenance.py"
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-8R1-R1 semantic-route audit"
Write-Host "Known R4 suppression regression does not stop the audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Enforcing R25-8 rollback..."
git restore --source=HEAD -- "toda_upstream_bootstrap.py"
if ($LASTEXITCODE -ne 0) {
  throw "Failed to restore toda_upstream_bootstrap.py from HEAD."
}
if (Test-Path $R258Test) {
  Remove-Item $R258Test -Force
}

Write-Host ""
Write-Host "B. Per-file HEAD equality..."
$Files = @(
  "toda_upstream_bootstrap.py",
  "toda_group_proof_narrative_semantics.py",
  "toda_group_proof_narrative_arguments.py",
  "toda_group_proof_narrative_argument_local_body.py",
  "toda_group_proof_narrative_argument_multi_renderer.py",
  "toda_group_result_proof_replay.py",
  "toda_group_proof_presentation.py"
)

foreach ($File in $Files) {
  git diff --quiet HEAD -- $File
  if ($LASTEXITCODE -eq 0) {
    Write-Host "$File : HEAD"
  }
  else {
    Write-Host "$File : DIFFERS FROM HEAD"
    git diff -- $File
  }
}

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}
$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "C. Stable semantic controls..."
  pytest -q `
    "tests/test_phase143_1a_semantic_dependency.py" `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Stable semantic controls failed."
  }

  Write-Host ""
  Write-Host "D. Known R4 suppression control (diagnostic only)..."
  pytest -q `
    "tests/test_phase144_6_r4_supporting_fact_filtering.py::test_phase144_6_r4_hides_internal_supporting_group_facts"
  $R4Exit = $LASTEXITCODE
  if ($R4Exit -eq 0) {
    Write-Host "R4 suppression control: PASS"
  }
  else {
    Write-Host "R4 suppression control: FAIL (recorded; audit continues)"
  }

  Write-Host ""
  Write-Host "E. Running semantic selection-boundary audit..."
  python (Join-Path $PatchRoot "audit_phase144_6_r25_8r1_r1.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Semantic selection-boundary audit failed."
  }

  Write-Host ""
  Write-Host "F. Current frontier helper excerpt..."
  python -c "from pathlib import Path; p=Path('toda_group_proof_narrative_argument_multi_renderer.py'); s=p.read_text(encoding='utf-8'); a=s.index('def _toda_group_proof_narrative_argument_frontier_hidden_step_ids'); b=s.find('\ndef ', a+10); print(s[a:] if b < 0 else s[a:b])"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-8R1-R1 completed."
  Write-Host "Production changes: none after rollback."
  Write-Host "Full suite intentionally not run."
  Write-Host "STOP before production repair."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
