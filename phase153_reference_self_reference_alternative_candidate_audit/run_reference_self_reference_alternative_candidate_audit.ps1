$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "Reference Self-Reference Alternative Candidate Audit"
Write-Host "=============================================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_group_proof_narrative_references.py"))) {
    throw "Run this script from C:\Users\oomae\Dropbox\Python\fitz\ehp_proof"
}

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
    Write-Host "A. Syntax check..."
    python -m py_compile `
      (Join-Path $PackageRoot "audit_reference_self_reference_alternatives.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Import/API preflight..."
    python -c "from toda_group_proof_narrative_references import build_toda_group_proof_narrative_reference_entries, select_toda_group_proof_narrative_reference_statement_steps; print('Import/API preflight passed.')"

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "C. Auditing the 8 confirmed self-reference groups..."
    python `
      (Join-Path $PackageRoot "audit_reference_self_reference_alternatives.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "=============================================================================="
    Write-Host "Alternative-candidate audit complete."
    Write-Host "Production files were NOT changed."
    Write-Host "Tests were NOT changed."
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
