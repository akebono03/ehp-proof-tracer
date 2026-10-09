$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$files = Join-Path $bundle "files"
$names = @(
  "phase162_validated_proof_presentation.py",
  "tests/test_phase162_r2_validated_proof_presentation.py",
  "tests/test_phase162_r3_2_reference_display.py"
)
foreach ($name in $names) {
  $from = Join-Path $files $name
  $to = Join-Path $repo $name
  $parent = Split-Path -Parent $to
  if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
  Copy-Item -LiteralPath $from -Destination $to -Force
  Write-Host "Updated: $to"
}
python -B -m pytest -q tests/test_phase162_r2_validated_proof_presentation.py tests/test_phase162_r3_2_reference_display.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Phase 162 R3-2 focused checks finished. Full test suite not run."
