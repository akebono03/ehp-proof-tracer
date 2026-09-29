$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$AuditRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker=Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker=$false
$Output=Join-Path $AuditRoot "phase144_6_r25_10_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-10 Final Regression Ownership Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

python -m py_compile `
  "toda_group_proof_narrative_semantics.py" `
  "toda_group_proof_narrative_renderer.py" `
  "toda_group_proof_narrative_argument_multi_renderer.py" `
  "toda_group_proof_narrative_argument_body_renderer.py"
if($LASTEXITCODE -ne 0){throw "Production syntax preflight failed."}

git diff --check
if($LASTEXITCODE -ne 0){throw "git diff --check failed."}

git diff --quiet HEAD -- "toda_upstream_bootstrap.py"
if($LASTEXITCODE -ne 0){throw "toda_upstream_bootstrap.py differs from HEAD."}
Write-Host "Preflight: PASS"

if(-not(Test-Path $Marker)){
  New-Item -Path $Marker -ItemType File -Force|Out-Null
  $CreatedMarker=$true
}
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"

try{
  Write-Host ""
  Write-Host "Running ownership audit..."
  python (Join-Path $AuditRoot "audit_phase144_6_r25_10.py") 2>&1 |
    Tee-Object -FilePath $Output
  if($LASTEXITCODE -ne 0){throw "R25-10 ownership audit failed."}

  Write-Host ""
  Write-Host "Representative failing tests (expected to remain failing in audit-only R25-10)..."
  pytest -q `
    "tests/test_phase144_6_pi6_generic_production_route.py" `
    "tests/test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py" `
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py" `
    "tests/test_phase144_6_r5_43_r2_recursive_repr_repair.py"
  Write-Host "Representative failures are diagnostic only; no repair was applied."

  Write-Host ""
  Write-Host "Audit output: $Output"
  Write-Host "=============================================================="
  Write-Host "R25-10 audit complete."
  Write-Host "Production changes: none."
  Write-Host "Full suite intentionally not run."
  Write-Host "=============================================================="
}
finally{
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if($CreatedMarker){Remove-Item $Marker -Force -ErrorAction SilentlyContinue}
}
