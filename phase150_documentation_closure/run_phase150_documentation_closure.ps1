$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Documentation Closure"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Documentation: 5 full files updated"
Write-Host "Full regression: NOT rerun"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying Phase 150 closure documentation..."
    python "$ScriptRoot\apply_phase150_documentation_closure.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host ""
    Write-Host "B. Verifying closure markers..."
    $Targets = @(
      ".\README.md",
      ".\docs\design.md",
      ".\docs\development_log.md",
      ".\docs\roadmap.md",
      ".\docs\proof_records.md"
    )
    foreach ($Target in $Targets) {
      $Match = Select-String -Path $Target -Pattern "<!-- PHASE150_CLOSURE -->" -SimpleMatch
      if (-not $Match) {
        throw "Phase 150 closure marker missing: $Target"
      }
      Write-Host "PASS: $Target"
    }

    Write-Host ""
    Write-Host "C. Git diff summary..."
    git diff --stat -- README.md docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md

    Write-Host ""
    Write-Host "D. Documentation diff..."
    git diff -- README.md docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "PHASE 150 DOCUMENTATION CLOSURE: APPLIED"
    Write-Host "Full regression: NOT rerun (10478/10478 already passed)"
    Write-Host "Next: Phase 151 All-Group Generic Baseline"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
