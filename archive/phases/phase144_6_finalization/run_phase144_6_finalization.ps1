$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$LogPath = Join-Path $PackageDir "phase144_6_finalization_output.txt"

Set-Location $RepoRoot

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

function Run-Step {
  param(
    [string]$Title,
    [scriptblock]$Action
  )

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host $Title
  Write-Host "=============================================================="

  & $Action
  if ($LASTEXITCODE -ne 0) {
    throw "$Title failed with exit code $LASTEXITCODE."
  }
}

try {
  Start-Transcript -Path $LogPath -Force | Out-Null

  Write-Host "=============================================================="
  Write-Host "Phase 144-6 Finalization"
  Write-Host "Production changes: none"
  Write-Host "Documentation changes: none in this measurement pass"
  Write-Host "Phase 145 result-reuse implementation: not included"
  Write-Host "=============================================================="

  Run-Step "A. Git / environment preflight" {
    git rev-parse --show-toplevel
    git branch --show-current
    git rev-parse HEAD
    python --version
    python -m pytest --version
    git status --short
  }

  Write-Host ""
  Write-Host "--------------------------------------------------------------"
  Write-Host "Phase 144-6 focused test inventory"
  Write-Host "--------------------------------------------------------------"

  $FocusedTests = @(
    Get-ChildItem `
      -Path (Join-Path $RepoRoot "tests") `
      -Filter "test_phase144_6*.py" `
      -File |
    Sort-Object Name |
    ForEach-Object { $_.FullName }
  )

  if ($FocusedTests.Count -eq 0) {
    throw "No tests/test_phase144_6*.py files were found."
  }

  Write-Host ("Focused test files: " + $FocusedTests.Count)
  foreach ($TestFile in $FocusedTests) {
    Write-Host ("  " + (Split-Path $TestFile -Leaf))
  }

  Run-Step "B. Phase 144-6 focused / regression tests" {
    python -m pytest @FocusedTests -q
  }

  Run-Step "C. Repository-wide Phase-final regression" {
    python -m pytest tests -q
  }

  Run-Step "D. Final Git status" {
    git status --short
    git diff --stat
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144-6 Finalization measurement: PASS"
  Write-Host "=============================================================="
  Write-Host "Technical investigation stop point: R25-30-R3"
  Write-Host "Confirmed phase boundary:"
  Write-Host "  - complete replay API belongs to Phase 144-6"
  Write-Host "  - depth=2 Narrative generic route belongs to Phase 144-6"
  Write-Host "  - Argument boundary / ownership model remains the Phase 144-6 model"
  Write-Host "  - remaining giant owned-entry proof-subtree expansion is deferred"
  Write-Host "  - result-reuse boundary design / implementation belongs to Phase 145"
  Write-Host ""
  Write-Host "No production or documentation file was modified by this runner."
  Write-Host "Return phase144_6_finalization_output.txt for the documentation-close pass."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue

  try {
    Stop-Transcript | Out-Null
  }
  catch {
  }
}
