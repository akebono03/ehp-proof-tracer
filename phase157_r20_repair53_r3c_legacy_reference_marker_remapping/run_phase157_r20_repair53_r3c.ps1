$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r3c - legacy Reference marker remapping"
Write-Host "=============================================================="
Write-Host "Production change:"
Write-Host "  toda_group_proof_narrative_renderer.py"
Write-Host "Focused pytest only; repository-wide pytest is NOT run."
Write-Host ""

Write-Host "[1/4] Apply repair53-r3c"
python ".\phase157_r20_repair53_r3c_legacy_reference_marker_remapping\apply_phase157_r20_repair53_r3c.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3c apply failed."
}

Write-Host ""
Write-Host "[2/4] Compile changed production file and focused test"
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3c compile check failed."
}

Write-Host ""
Write-Host "[3/4] Run repair53-r3c focused tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3c focused tests failed."
}

Write-Host ""
Write-Host "[4/4] Re-run repair53-r3 focused tests when present"
$R3Tests = Get-ChildItem `
  -Path ".\tests" `
  -Filter "*repair53*r3*.py" `
  -File `
  -ErrorAction SilentlyContinue |
  Where-Object {
    $_.Name -ne "test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py"
  }

if ($R3Tests.Count -gt 0) {
  $Args = @("-m", "pytest")
  foreach ($TestFile in $R3Tests) {
    $Args += $TestFile.FullName
  }
  $Args += "-q"

  & python @Args

  if ($LASTEXITCODE -ne 0) {
    throw "existing repair53-r3 focused tests failed."
  }
}
else {
  Write-Host "No existing repair53-r3 test file was found; skipped."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r3c verification completed"
Write-Host "Repository-wide pytest: NOT RUN (reserved for Phase 157 end)"
Write-Host "=============================================================="
