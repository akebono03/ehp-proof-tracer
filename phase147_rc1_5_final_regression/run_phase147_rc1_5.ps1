$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 147 RC1-5 Final Regression"
Write-Host "RC1: Argument-method ownership"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$PreviousPythonPath = $env:PYTHONPATH
$PreviousPythonIoEncoding = $env:PYTHONIOENCODING
$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Phase 147 RC1 syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_exactness_selection.py" `
    ".\toda_group_proof_narrative_argument_multi_renderer.py" `
    ".\tests\test_phase147_rc1_argument_method_ownership.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "B. RC1 ownership focused regression..."
  python -m pytest -q `
    ".\tests\test_phase147_rc1_argument_method_ownership.py" `
    ".\tests\test_phase143_19_method_evidence.py" `
    ".\tests\test_phase143_25_relevant_groups.py" `
    ".\tests\test_phase143_28_exactness_selection.py" `
    ".\tests\test_phase143_34_argument_header_method.py" `
    ".\tests\test_phase143_36_argument_body_blocks.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "C. Generic Narrative regression..."
  python -m pytest -q `
    ".\tests\test_phase143_44_single_argument_narrative_renderer.py" `
    ".\tests\test_phase143_46_multi_argument_narrative_assembler.py" `
    ".\tests\test_phase144_5_generic_definition_order_equations.py" `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "D. Web group-proof Narrative regression..."
  python -m pytest -q `
    ".\tests\test_phase131_5_web_group_proof.py" `
    ".\tests\test_phase135_2_web_narrative_inline_formatting.py" `
    ".\tests\test_phase135_3_web_narrative_readability.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "E. Phase 147 RC1 boundary verification..."
  python "$PackageDir\verify_phase147_rc1_boundary.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "F. Repository-wide pytest..."
  Write-Host "This is intentionally run only now, at the end of Phase 147."
  python -m pytest tests -q --durations=50
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 147 RC1-5 FINAL REGRESSION: PASS"
  Write-Host ""
  Write-Host "Completion criteria satisfied:"
  Write-Host "  - RC1 ownership API focused tests pass"
  Write-Host "  - existing method/relevance/selection regressions pass"
  Write-Host "  - generic Narrative regressions pass"
  Write-Host "  - Web group-proof Narrative regressions pass"
  Write-Host "  - RC1/RC2 boundary remains intact"
  Write-Host "  - repository-wide pytest passes"
  Write-Host ""
  Write-Host "Phase boundary:"
  Write-Host "  Phase 147 / RC1 can be closed."
  Write-Host "  RC2 evidence exposure is intentionally unchanged."
  Write-Host "  RC3 ordering is intentionally unchanged."
  Write-Host "=============================================================="
}
finally {
  if ($null -eq $PreviousPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  }
  else {
    $env:PYTHONPATH = $PreviousPythonPath
  }

  if ($null -eq $PreviousPythonIoEncoding) {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  }
  else {
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
  }
}
