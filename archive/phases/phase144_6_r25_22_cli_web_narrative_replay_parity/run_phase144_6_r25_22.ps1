$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-22 CLI / Web Generic Narrative Replay Parity"
Write-Host "Narrative input-path parity only"
Write-Host "=============================================================="
Write-Host ""

Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host "A. Applying minimal Web Narrative replay repair..."
  python `
    ".\phase144_6_r25_22_cli_web_narrative_replay_parity\apply_phase144_6_r25_22.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22 production repair failed."
  }
  Write-Host ""

  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\web_group_proof.py" `
    ".\phase144_6_r25_22_cli_web_narrative_replay_parity\test_phase144_6_r25_22.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22 syntax preflight failed."
  }
  Write-Host ""

  Write-Host "C. R25-22 focused CLI/Web Narrative parity tests..."
  pytest -q `
    ".\phase144_6_r25_22_cli_web_narrative_replay_parity\test_phase144_6_r25_22.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22 focused parity tests failed."
  }
  Write-Host ""

  Write-Host "D. Existing Web group-proof regressions..."
  pytest -q `
    ".\tests\test_phase131_5_web_group_proof.py" `
    ".\tests\test_phase135_2_web_narrative_inline_formatting.py" `
    ".\tests\test_phase135_3_web_narrative_readability.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22 existing Web regressions failed."
  }
  Write-Host ""

  Write-Host "E. Existing generic pi6 production-route regression..."
  pytest -q `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22 generic pi6 route regression failed."
  }
  Write-Host ""

  Write-Host "=============================================================="
  Write-Host "R25-22 focused checks completed."
  Write-Host "Expected Web result:"
  Write-Host "  pi_6^3 / depth 2 / Narrative shows numbered equations"
  Write-Host "  and dependency prose such as (1) and (2)."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Pop-Location
}
