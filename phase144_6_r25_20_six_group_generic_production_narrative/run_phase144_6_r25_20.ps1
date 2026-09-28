$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload = Join-Path $PackageRoot "payload"
$TestTarget = Join-Path $RepoRoot "tests\test_phase144_6_r25_20_six_group_generic_production_narrative.py"
$ShowTarget = Join-Path $PackageRoot "show_phase144_6_r25_20_six_group_narratives.py"

Write-Host ("=" * 62)
Write-Host "Phase 144-6 R25-20 Six-Group Generic Production Narrative"
Write-Host "Production changes: none"
Write-Host ("=" * 62)

Write-Host ""
Write-Host "A. Installing R25-20 focused test and visualization harness..."
Copy-Item `
  -Path (Join-Path $Payload "test_phase144_6_r25_20_six_group_generic_production_narrative.py") `
  -Destination $TestTarget `
  -Force
Copy-Item `
  -Path (Join-Path $Payload "show_phase144_6_r25_20_six_group_narratives.py") `
  -Destination $ShowTarget `
  -Force

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\main.py" `
    ".\toda_group_result_proof_replay.py" `
    $TestTarget `
    $ShowTarget

  Write-Host ""
  Write-Host "C. R25-20 six-group production-route contract..."
  python -m pytest -q `
    $TestTarget

  Write-Host ""
  Write-Host "D. Replay regressions and R25-9B semantic-closure contract..."
  python -m pytest -q `
    ".\tests\test_phase131_3_group_result_proof_replay.py" `
    ".\tests\test_phase131_4_group_result_proof_replay_cli.py" `
    ".\tests\test_phase144_6_r25_9b_nu_prime_definition_depth2.py"

  Write-Host ""
  Write-Host "E. Rendering all six generic production Narratives..."
  python $ShowTarget

  Write-Host ""
  Write-Host ("=" * 62)
  Write-Host "R25-20 focused checks completed."
  Write-Host "Inspect:"
  Write-Host ".\phase144_6_r25_20_six_group_generic_production_narrative\outputs\six_group_generic_narratives.txt"
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host ("=" * 62)
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
