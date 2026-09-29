$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$PatchRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker=Join-Path $ProjectRoot "tests\__init__.py"
$Created=$false
if (-not (Test-Path $Marker)) { New-Item $Marker -ItemType File -Force | Out-Null; $Created=$true }
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"
try {
  Write-Host "Phase 144-6 R14 import-origin preflight"
  Write-Host "Production changes: none"
  python (Join-Path $PatchRoot "check_phase144_6_r14_import_origins.py")
  if ($LASTEXITCODE -ne 0) { throw "R14 import-origin preflight failed." }
  Write-Host ""
  Write-Host "Pytest collect-only origin check..."
  pytest --collect-only -q `
    "tests/test_phase143_57c_step_derivation_connector.py::test_phase143_57c_pi6_3_first_local_derivation_is_grouped" `
    "tests/test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi8_5_direct_premise_is_not_left_at_argument_start"
  if ($LASTEXITCODE -ne 0) { throw "R14 pytest collect-only failed." }
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($Created) { Remove-Item $Marker -Force -ErrorAction SilentlyContinue }
}
