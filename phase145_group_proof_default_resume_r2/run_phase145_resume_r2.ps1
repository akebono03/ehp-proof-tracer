$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 145 Resume R2"
Write-Host "Preserve explicit legacy Trace Web test"
Write-Host "=============================================================="
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"
try {
  Write-Host "A. Applying one-test repair..."
  python ".\phase145_group_proof_default_resume_r2\apply_phase145_resume_r2.py"
  if ($LASTEXITCODE -ne 0) { throw "Resume R2 apply failed." }

  Write-Host "B. Syntax preflight..."
  python -m py_compile ".\tests\test_phase131_5_web_group_proof.py"
  if ($LASTEXITCODE -ne 0) { throw "Syntax preflight failed." }

  Write-Host "C. Re-running Phase 145 focused tests..."
  python -m pytest -q `
    ".\tests\test_phase145_group_proof_defaults.py" `
    ".\tests\test_phase132_7_group_proof_cli_modes.py" `
    ".\tests\test_phase131_4_group_result_proof_replay_cli.py" `
    ".\tests\test_phase132_9_web_group_proof_modes.py" `
    ".\tests\test_phase131_5_web_group_proof.py"
  if ($LASTEXITCODE -ne 0) { throw "Focused tests failed." }

  Write-Host "=============================================================="
  Write-Host "Phase 145 Resume R2 focused gate: PASS"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
