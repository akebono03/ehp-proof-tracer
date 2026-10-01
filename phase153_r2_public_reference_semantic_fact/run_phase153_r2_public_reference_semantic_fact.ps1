$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================="
Write-Host "Phase 153-R2 Public Narrative Repair"
Write-Host "Reference marker + semantic fact"
Write-Host "=============================================================="
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
  Write-Host "A. Applying minimal production change..."
  python `
    (Join-Path $PackageRoot "apply_phase153_r2_public_reference_semantic_fact.py")
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "B. Syntax check..."
  python -m py_compile `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase153_r2_public_reference_semantic_fact.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "C. Existing R2 semantic regression..."
  python -m pytest -q `
    ".\tests\test_phase153_r2_toda45_map_property_semantic.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "D. Existing reference normalization regression..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "E. Phase153-R2 public Narrative focused regression..."
  python -m pytest -q `
    ".\tests\test_phase153_r2_public_reference_semantic_fact.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase153-R2 public Narrative focused checks passed."
  Write-Host "Whole repository pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
  $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
  $env:PYTHONUTF8 = $PreviousPythonUtf8
}
