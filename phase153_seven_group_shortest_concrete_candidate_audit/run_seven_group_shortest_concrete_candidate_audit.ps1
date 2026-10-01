$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "7-Group Shortest Concrete Candidate Audit"
Write-Host "=============================================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_calculation.py"))) {
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
      (Join-Path $PackageRoot "audit_seven_group_shortest_concrete_candidates.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Import/API preflight..."
    python -c "from standard_production_repository import build_standard_production_proof_repository; from repository_proof_scope import build_repository_proof_scope; from toda_group_proof_narrative_references import extract_toda_group_proof_step_literature_reference; print('7-group audit imports passed.')"

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "C. Auditing shortest concrete candidates..."
    python `
      (Join-Path $PackageRoot "audit_seven_group_shortest_concrete_candidates.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "=============================================================================="
    Write-Host "7-group shortest concrete candidate audit complete."
    Write-Host "Production files were NOT changed."
    Write-Host "Tests were NOT changed."
    Write-Host "Full pytest was NOT run."
    Write-Host ""
    Write-Host "Please paste the console report."
    Write-Host "=============================================================================="
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONUTF8 = $PreviousPythonUtf8
}
