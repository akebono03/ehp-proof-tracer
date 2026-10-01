$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 153-R4.1 - Focused Test Baseline Repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "A. Applying focused-test baseline repair..."
python "$PackageDir\apply_phase153_r4_1_focused_test_baseline_repair.py"

Write-Host ""
Write-Host "B. Running the five repaired Phase 153 test files..."
python -m pytest -q `
  ".\tests\test_phase153_r2_public_reference_semantic_fact.py" `
  ".\tests\test_phase153_r3_4_reference_statement_rendering_connection.py" `
  ".\tests\test_phase153_r3_5_reference_body_duplicate_suppression.py" `
  ".\tests\test_phase153_r3_6_unresolved_reference_statement_rendering.py" `
  ".\tests\test_phase153_r3_9_remaining_reference_renderer_coverage.py"

Write-Host ""
Write-Host "C. Running all locally present Phase 153 focused tests..."
$Phase153Tests = Get-ChildItem `
  -Path ".\tests" `
  -Filter "test_phase153_*.py" `
  -File `
  -ErrorAction SilentlyContinue

if ($Phase153Tests.Count -eq 0) {
  throw "No tests\test_phase153_*.py files found."
}

$Phase153Paths = @(
  $Phase153Tests |
    ForEach-Object {
      $_.FullName
    }
)

python -m pytest -q @Phase153Paths

Write-Host ""
Write-Host "D. Re-running R4 audit-package focused tests when present..."
$R4Test = ".\phase153_r4_n2_reference_ancestry_audit\test_phase153_r4_n2_reference_ancestry_audit.py"

if (Test-Path $R4Test) {
  python -m pytest -q $R4Test
}
else {
  Write-Host "R4 audit package not found; skipping."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R4.1 completed."
Write-Host "Production code was not modified."
Write-Host "Full pytest is intentionally deferred to the end of Phase 153."
Write-Host "Next boundary: R5 Reference selection implementation."
Write-Host "=============================================================="
