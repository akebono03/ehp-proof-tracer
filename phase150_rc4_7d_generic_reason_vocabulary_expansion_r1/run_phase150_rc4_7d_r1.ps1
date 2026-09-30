$ErrorActionPreference = "Stop"
$RepoRoot=(Get-Location).Path
$PackageDir=Join-Path $RepoRoot "phase150_rc4_7d_generic_reason_vocabulary_expansion_r1"
$env:PYTHONPATH=$RepoRoot; $env:PYTHONIOENCODING="utf-8"
try {
 Write-Host "A. Applying RC4-7D R1..."; python (Join-Path $PackageDir "apply_phase150_rc4_7d_r1.py"); if($LASTEXITCODE-ne 0){throw "apply failed"}
 Write-Host "B. Syntax preflight..."; python -m py_compile .\toda_group_proof_narrative_reasons.py .\toda_group_proof_narrative_reason_renderer.py .\tests\test_phase150_rc4_7d_generic_reason_vocabulary.py; if($LASTEXITCODE-ne 0){throw "syntax failed"}
 Write-Host "C. Focused tests..."; python -m pytest -q tests/test_phase150_rc4_7d_generic_reason_vocabulary.py; if($LASTEXITCODE-ne 0){throw "focused tests failed"}
 Write-Host "D. Related regressions..."; python -m pytest -q tests/test_phase143_46_multi_argument_narrative_assembler.py tests/test_phase143_53a_narrative_transitions.py tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py tests/test_phase148_rc2_4_repair_r5.py tests/test_phase148_rc2_4_repair_r5_r2.py tests/test_phase150_rc4_7a_cross_group_reference_normalization.py tests/test_phase150_rc4_7b_production_repair.py; if($LASTEXITCODE-ne 0){throw "regressions failed"}
 Write-Host "E. Visible Narrative snapshots..."; python (Join-Path $PackageDir "show_phase150_rc4_7d_narratives.py"); if($LASTEXITCODE-ne 0){throw "snapshot failed"}
 Write-Host "RC4-7D R1 completed. Full repository tests intentionally not run."
} finally { Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue; Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue }
