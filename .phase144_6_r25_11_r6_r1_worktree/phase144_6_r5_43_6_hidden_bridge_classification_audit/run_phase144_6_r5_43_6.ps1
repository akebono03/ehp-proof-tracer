$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Copy-Item `
  -Path (Join-Path $PhaseDir "audit_phase144_6_r5_43_6.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_43_6.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PhaseDir "test_phase144_6_r5_43_6.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_43_6.py") `
  -Force

Write-Host "Phase 144-6-R5-43-6 audit files applied."
Write-Host "Production code changes: none."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = "$(Get-Location);$(Join-Path (Get-Location) 'tests')"

  pytest -q ".\tests\test_phase144_6_r5_43_6.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  python ".\audit_phase144_6_r5_43_6.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
