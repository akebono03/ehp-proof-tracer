$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Copy-Item `
  -Path (Join-Path $PhaseDir "audit_phase144_6_r5_43_11a.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_43_11a.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PhaseDir "test_phase144_6_r5_43_11a_insertion_failure_classification_audit.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_43_11a_insertion_failure_classification_audit.py") `
  -Force

Write-Host "Phase 144-6-R5-43-11A insertion failure classification audit applied."
Write-Host "Production code changes: none."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = "$(Get-Location);$(Join-Path (Get-Location) 'tests')"

  pytest -q ".\tests\test_phase144_6_r5_43_11a_insertion_failure_classification_audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  python ".\audit_phase144_6_r5_43_11a.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
