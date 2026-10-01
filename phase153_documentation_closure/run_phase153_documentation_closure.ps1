$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

function Invoke-NativeChecked {
  param(
    [Parameter(Mandatory = $true)]
    [scriptblock]$Command,
    [Parameter(Mandatory = $true)]
    [string]$Label
  )

  & $Command

  if ($LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE."
  }
}

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 153 Documentation Closure"
Write-Host "=============================================================="

Write-Host ""
Write-Host "[1/4] Apply documentation closure"
Invoke-NativeChecked `
  -Label "documentation apply" `
  -Command {
    python "$PackageDir\apply_phase153_documentation_closure.py"
  }

Write-Host ""
Write-Host "[2/4] Compile documentation scripts"
Invoke-NativeChecked `
  -Label "script compile" `
  -Command {
    python -m py_compile `
      "$PackageDir\apply_phase153_documentation_closure.py" `
      "$PackageDir\verify_phase153_documentation_closure.py"
  }

Write-Host ""
Write-Host "[3/4] Verify full-file outputs"
Invoke-NativeChecked `
  -Label "documentation verification" `
  -Command {
    python "$PackageDir\verify_phase153_documentation_closure.py"
  }

Write-Host ""
Write-Host "[4/4] Git diff summary"
git diff --stat -- `
  README.md `
  docs/design.md `
  docs/development_log.md `
  docs/roadmap.md `
  docs/proof_records.md

Write-Host ""
git status --short -- `
  README.md `
  docs/design.md `
  docs/development_log.md `
  docs/roadmap.md `
  docs/proof_records.md

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153 documentation closure completed."
Write-Host "No pytest was run."
Write-Host "Full updated documents:"
Write-Host "  .\phase153_documentation_closure\output_full_documents\"
Write-Host "=============================================================="
