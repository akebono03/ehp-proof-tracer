$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 145 Resume R1 - group-proof default only"
Write-Host "=============================================================="
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"
try {
  Write-Host "A. Resume-safe apply..."
  python ".\phase145_group_proof_default_resume_r1\apply_phase145_resume_r1.py"
  if ($LASTEXITCODE -ne 0) { throw "Resume R1 apply failed." }

  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\main.py" ".\web_app.py" ".\web_group_proof.py" `
    ".\tests\test_phase145_group_proof_defaults.py" `
    ".\tests\test_phase132_7_group_proof_cli_modes.py" `
    ".\tests\test_phase131_4_group_result_proof_replay_cli.py" `
    ".\tests\test_phase132_9_web_group_proof_modes.py" `
    ".\tests\test_phase131_5_web_group_proof.py"
  if ($LASTEXITCODE -ne 0) { throw "Syntax preflight failed." }

  Write-Host "C. Focused tests only..."
  python -m pytest -q `
    ".\tests\test_phase145_group_proof_defaults.py" `
    ".\tests\test_phase132_7_group_proof_cli_modes.py" `
    ".\tests\test_phase131_4_group_result_proof_replay_cli.py" `
    ".\tests\test_phase132_9_web_group_proof_modes.py" `
    ".\tests\test_phase131_5_web_group_proof.py"
  if ($LASTEXITCODE -ne 0) { throw "Focused tests failed." }

  Write-Host "=============================================================="
  Write-Host "Phase 145 Resume R1 focused gate: PASS"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
