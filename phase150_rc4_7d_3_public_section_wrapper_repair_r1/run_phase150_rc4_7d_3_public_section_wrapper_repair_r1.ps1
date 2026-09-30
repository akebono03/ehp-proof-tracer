$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7D-3 Public Section Wrapper Repair R1"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PackageDir = Join-Path $RepoRoot "phase150_rc4_7d_3_public_section_wrapper_repair_r1"
$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "A. Applying minimal public section-wrapper repair..."
  python (Join-Path $PackageDir "apply_phase150_rc4_7d_3_public_section_wrapper_repair_r1.py")
  if ($LASTEXITCODE -ne 0) { throw "section-wrapper repair failed" }

  Write-Host "B. Syntax/import preflight..."
  python -m py_compile ".\toda_group_proof_narrative_renderer.py"
  if ($LASTEXITCODE -ne 0) { throw "syntax preflight failed" }
  python -c "import toda_group_proof_narrative_renderer; import web_group_proof"
  if ($LASTEXITCODE -ne 0) { throw "import preflight failed" }

  Write-Host "C. RC4-7A public Reference-section contract..."
  python -m pytest -q tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
  if ($LASTEXITCODE -ne 0) { throw "RC4-7A contract regression remains" }

  Write-Host "D. RC4-7D-3 focused route tests..."
  python -m pytest -q tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py
  if ($LASTEXITCODE -ne 0) { throw "RC4-7D-3 focused tests failed" }

  Write-Host "E. RC4-7D reason regression tests..."
  $ReasonTests = @(
    "tests/test_phase150_rc4_7d_generic_reason_vocabulary.py",
    "tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py"
  ) | Where-Object { Test-Path $_ }
  if ($ReasonTests.Count -gt 0) {
    python -m pytest -q $ReasonTests
    if ($LASTEXITCODE -ne 0) { throw "RC4-7D reason regressions failed" }
  }

  Write-Host "F. Related Web/Narrative regressions..."
  $RelatedTests = @(
    "tests/test_phase135_1_web_narrative_display_math.py",
    "tests/test_phase135_3_web_narrative_readability.py",
    "tests/test_phase143_46_multi_argument_narrative_assembler.py",
    "tests/test_phase143_53a_narrative_transitions.py",
    "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py"
  ) | Where-Object { Test-Path $_ }
  if ($RelatedTests.Count -gt 0) {
    python -m pytest -q $RelatedTests
    if ($LASTEXITCODE -ne 0) { throw "related Web/Narrative regressions failed" }
  }

  Write-Host "G. Visible Web Narrative snapshots..."
  python (Join-Path $PackageDir "show_phase150_rc4_7d_3_web_narratives.py")
  if ($LASTEXITCODE -ne 0) { throw "Web Narrative snapshot failed" }

  Write-Host "=============================================================="
  Write-Host "RC4-7D-3 Public Section Wrapper Repair R1 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
