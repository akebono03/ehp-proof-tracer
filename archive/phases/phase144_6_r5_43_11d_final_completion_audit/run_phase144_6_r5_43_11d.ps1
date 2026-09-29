$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Copy-Item `
  -Path (Join-Path $PhaseDir "audit_phase144_6_r5_43_11d.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_43_11d.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PhaseDir "test_phase144_6_r5_43_11d_final_completion_audit.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_43_11d_final_completion_audit.py") `
  -Force

Write-Host "Phase 144-6-R5-43-11D final completion audit applied."
Write-Host "Production code changes: none."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = "$(Get-Location);$(Join-Path (Get-Location) 'tests')"

  pytest -q ".\tests\test_phase144_6_r5_43_11d_final_completion_audit.py"
  if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Final completion test failed. Printing inventory."
    python ".\audit_phase144_6_r5_43_11d.py"
    exit $LASTEXITCODE
  }

  python ".\audit_phase144_6_r5_43_11d.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
