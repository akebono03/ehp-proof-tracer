$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "Phase 153-R3-2 Fixed1 - Reference Statement Selection / Ownership Audit"
Write-Host "=============================================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_group_proof_narrative_renderer.py"))) {
    throw "Run this script from C:\Users\oomae\Dropbox\Python\fitz\ehp_proof"
}

Write-Host "Repository root:"
Write-Host "  $RepoRoot"

$PreviousPythonPath = $env:PYTHONPATH
$PreviousPythonIoEncoding = $env:PYTHONIOENCODING
$PreviousPythonUtf8 = $env:PYTHONUTF8

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
    $env:PYTHONPATH = $RepoRoot
}
else {
    $env:PYTHONPATH = $RepoRoot + [IO.Path]::PathSeparator + $PreviousPythonPath
}

$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

try {
    Write-Host ""
    Write-Host "A. Syntax check..."
    python -m py_compile `
      (Join-Path $PackageRoot "audit_phase153_r3_2_reference_statement_selection_ownership.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Import/API preflight..."
    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"

    python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_proof_narrative_renderer import _render_group_proof_narrative_latex, render_toda_group_proof_narrative_markdown; from toda_group_proof_narrative_references import build_toda_group_proof_narrative_reference_entries; from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_closure_presentation; print('Import/API preflight passed.')" 2>&1

    $PreflightExitCode = $LASTEXITCODE
    $ErrorActionPreference = $PreviousErrorActionPreference

    if ($PreflightExitCode -ne 0) {
        Write-Host ""
        Write-Host "Import/API preflight failed."
        Write-Host "No production files were changed."
        exit $PreflightExitCode
    }

    Write-Host ""
    Write-Host "C. Running 112-group selection / ownership audit..."
    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"

    python `
      (Join-Path $PackageRoot "audit_phase153_r3_2_reference_statement_selection_ownership.py") `
      2>&1 | Tee-Object `
      -FilePath (Join-Path $PackageRoot "audit_run_output.txt")

    $AuditExitCode = $LASTEXITCODE
    $ErrorActionPreference = $PreviousErrorActionPreference

    if ($AuditExitCode -ne 0) {
        Write-Host ""
        Write-Host "Audit failed. The traceback is shown above and saved in:"
        Write-Host "  .\phase153_r3_2_reference_statement_selection_ownership_audit_fixed1\audit_run_output.txt"
        Write-Host "No production files were changed."
        exit $AuditExitCode
    }

    Write-Host ""
    Write-Host "=============================================================================="
    Write-Host "Audit complete."
    Write-Host "Production files were NOT changed."
    Write-Host "Full pytest was NOT run."
    Write-Host ""
    Write-Host "Please paste the console summary."
    Write-Host "=============================================================================="
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONUTF8 = $PreviousPythonUtf8
}
