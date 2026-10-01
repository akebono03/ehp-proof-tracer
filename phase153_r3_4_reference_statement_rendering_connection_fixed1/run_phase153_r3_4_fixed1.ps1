$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "Phase 153-R3-4 Fixed1 - Reference Statement Rendering Connection"
Write-Host "=============================================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_group_proof_narrative_renderer.py"))) {
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
    Write-Host "A. Applying minimal Phase153-R3-4 Fixed1 change..."
    python `
      (Join-Path $PackageRoot "apply_phase153_r3_4_fixed1.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Syntax check..."
    python -m py_compile `
      ".\toda_group_proof_narrative_references.py" `
      ".\toda_group_proof_narrative_contribution_renderer.py" `
      ".\toda_group_proof_narrative_renderer.py" `
      ".\tests\test_phase153_r3_4_reference_statement_rendering_connection.py"

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "C. Running targeted Phase153-R3-4 tests..."
    python -m pytest `
      ".\tests\test_phase153_r3_4_reference_statement_rendering_connection.py" `
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
    Write-Host "Phase153-R3-4 Fixed1 targeted tests passed."
    Write-Host "Full pytest was NOT run."
    Write-Host "Body duplicate suppression was NOT implemented."
    Write-Host "Unresolved reference renderers were NOT added."
    Write-Host "=============================================================================="
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONUTF8 = $PreviousPythonUtf8
}
