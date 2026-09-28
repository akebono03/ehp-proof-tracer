$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_38.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_38.py") `
  -Force
Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py") `
  -Force

Write-Host "Phase 144-6-R5-38 R2 audit repair applied."
Write-Host "Repaired: Phase-36 direct-current-Narrative coverage exclusion."
Write-Host "Production code changes: none."

Push-Location $RepoRoot
try {
  $RepoPath = (Get-Location).Path
  $TestsPath = Join-Path $RepoPath "tests"
  $env:PYTHONPATH = "$RepoPath;$TestsPath"

  pytest -q `
    ".\tests\test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py" `
    ".\tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py"

  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  python ".\audit_phase144_6_r5_38.py"
  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
