$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5d repair1 - Web/Markdown representation normalization"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Run lightweight normalization tests"
python -m pytest `
  ".\phase158_r5_5d_repair1_web_markdown_representation_normalization\test_phase158_r5_5d_repair1.py" `
  -q

if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run normalized current-corpus generic public sequence cross-audit"
python `
  ".\phase158_r5_5d_repair1_web_markdown_representation_normalization\audit_phase158_r5_5d_repair1.py"

if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5d repair1 audit complete"
Write-Host "No production code was changed."
Write-Host "No repository-wide pytest was run."
Write-Host "=============================================================="
