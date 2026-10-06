$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 repair8 failure audit repair1"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

$OriginalPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($OriginalPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = $RepoRoot + [IO.Path]::PathSeparator + $OriginalPythonPath
}

try {
  Write-Host "[1/3] Syntax-check audit script"

  python -m py_compile `
    ".\phase159_r1_7c_r4_repair8_failure_decomposition_audit_repair1\audit_phase159_r1_7c_r4_repair8_failures_repair1.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Audit script syntax check failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[2/3] Render target Narratives and classify failures"

  python ".\phase159_r1_7c_r4_repair8_failure_decomposition_audit_repair1\audit_phase159_r1_7c_r4_repair8_failures_repair1.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Failure decomposition audit failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[3/3] Show pi6_3 diagnostics"

  Get-Content `
    ".\phase159_r1_7c_r4_repair8_failure_decomposition_audit_repair1\output\pi6_3_diagnostics.txt" `
    -Encoding UTF8

  Write-Host ""
  Write-Host "=== pi6_3 Reference section ==="

  $pi6Path = ".\phase159_r1_7c_r4_repair8_failure_decomposition_audit_repair1\output\pi6_3.md"
  $pi6 = Get-Content $pi6Path -Encoding UTF8

  $proofIndex = (
    Select-String `
      -Path $pi6Path `
      -Pattern "^## 証明$" |
    Select-Object -First 1
  ).LineNumber

  if ($proofIndex) {
    $pi6[0..($proofIndex - 2)]
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Audit complete"
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}
