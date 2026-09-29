$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146-7 Generic Argument Purpose Prose"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TestTarget = Join-Path $RepoRoot "tests\test_phase146_7_generic_argument_purpose_prose.py"

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying minimal production change..."
    python "$ScriptDir\apply_phase146_7.py"
    if ($LASTEXITCODE -ne 0) { throw "Production patch failed." }

    Write-Host ""
    Write-Host "B. Installing focused Phase 146-7 tests..."
    Copy-Item `
      "$ScriptDir\test_phase146_7_generic_argument_purpose_prose.py" `
      $TestTarget `
      -Force

    Write-Host ""
    Write-Host "C. Syntax preflight..."
    python -m py_compile `
      ".\toda_group_proof_narrative_argument_renderer.py" `
      $TestTarget
    if ($LASTEXITCODE -ne 0) { throw "Syntax preflight failed." }

    Write-Host ""
    Write-Host "D. Focused Phase 146-7 tests..."
    pytest -q `
      ".\tests\test_phase146_7_generic_argument_purpose_prose.py" `
      ".\tests\test_phase143_19_method_evidence.py"
    if ($LASTEXITCODE -ne 0) { throw "Focused tests failed." }

    Write-Host ""
    Write-Host "E. Existing pi_6^3 public-route regression..."
    pytest -q ".\tests\test_phase144_6_public_route_cutover.py"
    if ($LASTEXITCODE -ne 0) { throw "Public-route regression failed." }

    Write-Host ""
    Write-Host "F. Current pi_6^3 Narrative purpose line..."
    python main.py group-proof 3 3 --depth 2 --mode narrative |
      Select-String "位数を決定するために"
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 146-7 focused verification complete."
Write-Host "Full suite intentionally not run."
Write-Host "=============================================================="
