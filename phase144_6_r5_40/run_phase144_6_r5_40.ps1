$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_40.py") -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_40.py") -Force
Copy-Item -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py") -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py") -Force

Write-Host "Phase 144-6-R5-40 audit files applied."
Write-Host "Production code changes: none."

Push-Location $RepoRoot
try {
  $RepoPath = (Get-Location).Path
  $TestsPath = Join-Path $RepoPath "tests"
  $env:PYTHONPATH = "$RepoPath;$TestsPath"
  pytest -q `
    ".\tests\test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py" `
    ".\tests\test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python ".\audit_phase144_6_r5_40.py"
  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
