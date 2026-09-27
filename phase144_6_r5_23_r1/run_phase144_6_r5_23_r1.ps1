$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Push-Location $RepoRoot
try {
  $Files = @(
    ".\audit_phase144_6_r5_20.py",
    ".\audit_phase144_6_r5_21.py",
    ".\audit_phase144_6_r5_22.py",
    ".\audit_phase144_6_r5_23.py"
  )

  foreach ($File in $Files) {
    if (-not (Test-Path $File)) {
      throw "Required audit file not found: $File"
    }

    $Content = Get-Content -Raw -Encoding UTF8 $File
    $Content = $Content.Replace(
      "from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (",
      "from test_phase144_6_r5_18_production_generic_proof_chain_foundation import ("
    )
    Set-Content -Path $File -Value $Content -Encoding UTF8
  }

  Write-Host "Phase 144-6-R5-23-R1 import repair applied."
  Write-Host "Changed audit-only imports in:"
  Write-Host "  audit_phase144_6_r5_20.py"
  Write-Host "  audit_phase144_6_r5_21.py"
  Write-Host "  audit_phase144_6_r5_22.py"
  Write-Host "  audit_phase144_6_r5_23.py"
  Write-Host "Production code changes: none."

  $RepoPath = (Get-Location).Path
  $TestsPath = Join-Path $RepoPath "tests"

  # Put the current checkout first and remove dependence on package-style
  # "tests.*" imports, which can resolve to another checkout on sys.path.
  $env:PYTHONPATH = "$RepoPath;$TestsPath"

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-23 targeted tests"
  Write-Host ("=" * 78)

  pytest -q `
    ".\tests\test_phase144_6_r5_21_missing_7_facts_generic_provider_audit.py" `
    ".\tests\test_phase144_6_r5_22_missing_4_facts_statement_structure_audit.py" `
    ".\tests\test_phase144_6_r5_23_missing_7_facts_generic_visibility_path_audit.py"

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-23 visibility-path audit"
  Write-Host ("=" * 78)

  python ".\audit_phase144_6_r5_23.py"
  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
