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

Write-Host "=============================================================="
Write-Host "Phase 153 Closure Repair R13 Syntax Repair R1"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/4] Restore + repair renderer"
Invoke-NativeChecked `
  -Label "restore + repair renderer" `
  -Command {
    python "$PackageDir\apply_phase153_closure_repair_r13_syntax_repair_r1.py"
  }

Write-Host ""
Write-Host "[2/4] Compile"
Invoke-NativeChecked `
  -Label "py_compile" `
  -Command {
    python -m py_compile `
      ".\toda_group_proof_narrative_references.py" `
      ".\toda_group_proof_narrative_renderer.py" `
      ".\tests\test_phase153_closure_repair_r13_syntax_repair_r1.py" `
      "$PackageDir\audit_phase153_closure_repair_r13_syntax_repair_r1.py"
  }

Write-Host ""
Write-Host "[3/4] Focused smoke pytest"
Invoke-NativeChecked `
  -Label "focused smoke pytest" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase153_closure_repair_r13_syntax_repair_r1.py"
  }

Write-Host ""
Write-Host "[4/4] Smoke audit"
Invoke-NativeChecked `
  -Label "smoke audit" `
  -Command {
    python "$PackageDir\audit_phase153_closure_repair_r13_syntax_repair_r1.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "R13 syntax repair completed successfully."
Write-Host "Do NOT run full pytest yet."
Write-Host "Next: rerun the R13 focused tests + 112-group closure audit."
Write-Host "=============================================================="
