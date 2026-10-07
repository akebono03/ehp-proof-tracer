$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$PreviousPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = "$RepoRoot;$PreviousPythonPath"
}

try {
  Write-Host "=============================================================="
  Write-Host "Phase 159 R1-7c R4 repair9 R9-A stage audit"
  Write-Host "AUDIT ONLY - no production changes"
  Write-Host "=============================================================="
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/2] Syntax check current production"
  python -m py_compile ".\toda_group_proof_narrative_contribution_renderer.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Current production syntax check failed."
  }

  Write-Host ""
  Write-Host "[2/2] Trace pi_6^3 through contribution-renderer stages"
  python ".\phase159_r1_7c_r4_repair9_r9a_stage_audit\audit_phase159_r1_7c_r4_repair9_r9a_stage.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R9-A stage audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R9-A stage audit completed."
  Write-Host "Production code was NOT modified."
  Write-Host "No pytest was run."
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
