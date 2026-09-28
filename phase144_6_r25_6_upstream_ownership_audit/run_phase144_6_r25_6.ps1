$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-6 upstream ownership audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Verifying production baseline..."
git diff --exit-code -- `
  "main.py" `
  "toda_group_proof_narrative_argument_multi_renderer.py"

if ($LASTEXITCODE -ne 0) {
  throw "Production baseline differs from HEAD."
}

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "B. Running related focused tests..."
  pytest -q `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py" `
    "tests/test_phase144_6_r5_28_narrative_contribution_ownership_audit.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Related focused tests failed."
  }

  Write-Host ""
  Write-Host "C. Running upstream ownership audit..."
  python (Join-Path $PatchRoot "audit_phase144_6_r25_6.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Upstream ownership audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-6 completed."
  Write-Host "Production changes: none."
  Write-Host "Full suite intentionally not run."
  Write-Host "STOP before any production repair."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
