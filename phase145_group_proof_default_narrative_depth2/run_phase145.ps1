$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 - group-proof default only"
Write-Host "default mode=narrative, depth=2"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying minimal Phase 145 change..."
    python ".\phase145_group_proof_default_narrative_depth2\apply_phase145.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145 apply failed."
    }

    Write-Host ""
    Write-Host "B. Syntax preflight..."
    python -m py_compile `
      ".\main.py" `
      ".\web_app.py" `
      ".\web_group_proof.py" `
      ".\tests\test_phase145_group_proof_defaults.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145 syntax preflight failed."
    }

    Write-Host ""
    Write-Host "C. Focused Phase 145 tests only..."
    python -m pytest -q `
      ".\tests\test_phase145_group_proof_defaults.py" `
      ".\tests\test_phase132_7_group_proof_cli_modes.py" `
      ".\tests\test_phase131_4_group_result_proof_replay_cli.py" `
      ".\tests\test_phase132_9_web_group_proof_modes.py" `
      ".\tests\test_phase131_5_web_group_proof.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145 focused tests failed."
    }

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 145 focused implementation gate: PASS"
    Write-Host "Repository-wide pytest: NOT RUN"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
