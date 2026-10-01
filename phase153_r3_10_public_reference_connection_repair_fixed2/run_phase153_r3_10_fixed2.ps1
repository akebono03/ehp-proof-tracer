$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "Phase 153-R3-10 Fixed2 - Route-Neutral Public Reference Verification"
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
    Write-Host "A. Applying test-only Phase153-R3-10 Fixed2..."
    python `
      (Join-Path $PackageRoot "apply_phase153_r3_10_fixed2.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Syntax check..."
    python -m py_compile `
      ".\tests\test_phase153_r3_10_public_reference_connection_repair.py"

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "C. Running targeted Phase153-R3-10 tests..."
    python -m pytest `
      ".\tests\test_phase153_r3_10_public_reference_connection_repair.py" `
      ".\tests\test_phase153_r3_9_remaining_reference_renderer_coverage.py" `
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
    Write-Host "Phase153-R3-10 Fixed2 targeted tests passed."
    Write-Host "Public Reference verification is route-neutral."
    Write-Host "The pi6^3 route is accepted without requiring a ## 証明 heading."
    Write-Host "Production files were NOT changed by Fixed2."
    Write-Host "Full pytest was NOT run."
    Write-Host "Reference/body ownership was NOT changed."
    Write-Host "=============================================================================="
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONUTF8 = $PreviousPythonUtf8
}
