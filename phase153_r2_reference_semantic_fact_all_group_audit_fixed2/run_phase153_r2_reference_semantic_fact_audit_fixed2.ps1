$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================="
Write-Host "Phase 153-R2 Follow-up Audit Fixed2"
Write-Host "Reference-only / Reference + Semantic Fact / Unresolved"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_group_proof_narrative_renderer.py"))) {
  throw "Run this script from C:\Users\oomae\Dropbox\Python\fitz\ehp_proof"
}

$PreviousPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = $RepoRoot + [IO.Path]::PathSeparator + $PreviousPythonPath
}

try {
  Write-Host "A. Syntax check..."
  python -m py_compile `
    (Join-Path $PackageRoot "audit_phase153_r2_reference_semantic_fact.py")
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "B. Import/API preflight..."
  $PreviousErrorActionPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"

  python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step; from toda_group_proof_narrative_provenance_catalog import is_toda_group_proof_narrative_provenance_only_statement; from toda_group_proof_narrative_references import extract_toda_group_proof_step_literature_reference; from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_closure_presentation; print('Import/API preflight passed.')" 2>&1

  $PreflightExitCode = $LASTEXITCODE
  $ErrorActionPreference = $PreviousErrorActionPreference

  if ($PreflightExitCode -ne 0) {
    Write-Host ""
    Write-Host "Import/API preflight failed."
    Write-Host "No production files were changed."
    exit $PreflightExitCode
  }

  Write-Host ""
  Write-Host "C. Running 112-group audit..."
  $PreviousErrorActionPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"

  python `
    (Join-Path $PackageRoot "audit_phase153_r2_reference_semantic_fact.py") `
    2>&1 | Tee-Object `
    -FilePath (Join-Path $PackageRoot "audit_run_output.txt")

  $AuditExitCode = $LASTEXITCODE
  $ErrorActionPreference = $PreviousErrorActionPreference

  if ($AuditExitCode -ne 0) {
    Write-Host ""
    Write-Host "Audit failed. The full Python traceback is shown above and saved in:"
    Write-Host "  .\phase153_r2_reference_semantic_fact_all_group_audit_fixed2\audit_run_output.txt"
    Write-Host "No production files were changed."
    exit $AuditExitCode
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Audit complete."
  Write-Host "Production files were NOT changed."
  Write-Host "Full pytest was NOT run."
  Write-Host ""
  Write-Host "Please paste the console summary."
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
