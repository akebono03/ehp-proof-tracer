$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "Phase 153-R3-3 - Representative Reference Statement Selection Rule"
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
    Write-Host "A. Applying minimal Phase153-R3-3 changes..."
    python `
      (Join-Path $PackageRoot "apply_phase153_r3_3.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Syntax check..."
    python -m py_compile `
      (Join-Path $RepoRoot "toda_group_proof_narrative_references.py") `
      (Join-Path $RepoRoot "tests\test_phase153_r3_3_reference_statement_selection.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "C. Running targeted Phase153-R3-3 tests..."
    python -m pytest `
      ".\tests\test_phase153_r3_3_reference_statement_selection.py" `
      ".\tests\test_phase144_6_r3_structured_references.py" `
      ".\tests\test_phase144_6_r3_production_references.py" `
      ".\tests\test_phase153_r2_public_reference_semantic_fact.py" `
      -q

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "=============================================================================="
    Write-Host "Phase153-R3-3 targeted tests passed."
    Write-Host "Full pytest was NOT run."
    Write-Host "Public Reference section rendering is intentionally unchanged in R3-3."
    Write-Host "=============================================================================="
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONUTF8 = $PreviousPythonUtf8
}
