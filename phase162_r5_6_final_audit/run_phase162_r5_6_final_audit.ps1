$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
$files = @(
  "toda_general_reference_schema.py",
  "tests\test_phase162_r5_6_final_reference_format.py"
)
foreach ($file in $files) {
  $source = Join-Path (Join-Path $PSScriptRoot "files") $file
  $target = Join-Path (Get-Location) $file
  if (Test-Path $target) { Copy-Item $target ($target + ".phase162_r5_6_final_audit.bak") -Force }
  $directory = Split-Path $target -Parent
  if (!(Test-Path $directory)) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
  Copy-Item $source $target -Force
  Write-Host "Updated: $file"
}
$tests = @(
  "tests/test_phase162_r5_2_general_reference_schema.py",
  "tests/test_phase162_r5_6_final_reference_format.py",
  "tests/test_phase162_r5_6_repair4_fixed_statement_reuse.py",
  "tests/test_phase162_r5_6_repair3_reference_application_prose.py",
  "tests/test_phase161_r7_premise_provenance_validation.py"
)
python -B -m pytest -q @tests
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "=== E2 eta3 dependency audit (read-only) ==="
python -B (Join-Path $PSScriptRoot "audit_phase162_e2_dependency.py")
if ($LASTEXITCODE -ne 0) { throw "Dependency audit failed" }
Write-Host "Phase 162 final display audit complete. Full suite not run."
