$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "Phase 153-R3-6 - Unresolved Reference Statement Rendering"
Write-Host "=============================================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_group_proof_generic_narrative_renderer.py"))) {
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
    Write-Host "A. Applying minimal Phase153-R3-6 changes..."
    python `
      (Join-Path $PackageRoot "apply_phase153_r3_6.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Syntax check..."
    python -m py_compile `
      ".\toda_group_proof_generic_narrative_renderer.py" `
      ".\tests\test_phase153_r3_6_unresolved_reference_statement_rendering.py"

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "C. Running targeted Phase153-R3-6 tests..."
    python -m pytest `
      ".\tests\test_phase153_r3_6_unresolved_reference_statement_rendering.py" `
      ".\tests\test_phase153_r3_5_reference_body_duplicate_suppression.py" `
      ".\tests\test_phase153_r3_4_reference_statement_rendering_connection.py" `
      ".\tests\test_phase153_r3_3_reference_statement_selection.py" `
      ".\tests\test_phase153_r2_public_reference_semantic_fact.py" `
      ".\tests\test_phase144_6_r3_structured_references.py" `
      ".\tests\test_phase144_6_r3_production_references.py" `
      -q

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "=============================================================================="
    Write-Host "Phase153-R3-6 targeted tests passed."
    Write-Host "The 37 previously unresolved reference steps are semantic-renderable."
    Write-Host "Full pytest was NOT run."
    Write-Host "No proof facts, selection rules, or ownership rules were changed."
    Write-Host "=============================================================================="
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONUTF8 = $PreviousPythonUtf8
}
