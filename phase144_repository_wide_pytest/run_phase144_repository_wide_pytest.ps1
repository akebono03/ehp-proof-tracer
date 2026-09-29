$ErrorActionPreference="Stop"

$PackageRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot=(Get-Location).Path
$TestsDir=Join-Path $RepoRoot "tests"
$Marker=Join-Path $TestsDir "__init__.py"
$CreatedMarker=$false
$Output=Join-Path $PackageRoot "phase144_repository_wide_pytest_output.txt"

$OldPythonPath=$env:PYTHONPATH
$OldEncoding=$env:PYTHONIOENCODING

Write-Host "=============================================================="
Write-Host "Phase 144 Repository-Wide Pytest"
Write-Host "FINAL whole-suite run for Phase 144"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Documentation changes: none"
Write-Host "=============================================================="

Start-Transcript -Path $Output -Force | Out-Null

try {
  Write-Host ""
  Write-Host "A. Repository / environment preflight"
  Write-Host "--------------------------------------------------------------"
  git rev-parse --show-toplevel
  git branch --show-current
  git rev-parse HEAD
  python --version
  python -m pytest --version
  git status --short

  if (-not (Test-Path $TestsDir)) {
    throw "tests directory was not found: $TestsDir"
  }

  if (-not (Test-Path $Marker)) {
    New-Item -ItemType File -Path $Marker -Force | Out-Null
    $CreatedMarker=$true
    Write-Host "Temporary package marker created: tests/__init__.py"
  } else {
    Write-Host "Existing tests/__init__.py preserved."
  }

  $env:PYTHONPATH="$RepoRoot;$TestsDir"
  $env:PYTHONIOENCODING="utf-8"

  Write-Host ""
  Write-Host "B. Import preflight"
  Write-Host "--------------------------------------------------------------"
  python -c "import tests.test_phase143_19_method_evidence; import test_phase143_19_method_evidence; print('Dual import preflight: PASS')"
  if ($LASTEXITCODE -ne 0) {
    throw "Dual import preflight failed. Repository-wide pytest was NOT started."
  }

  Write-Host ""
  Write-Host "C. Phase 144 FINAL repository-wide pytest"
  Write-Host "--------------------------------------------------------------"
  Write-Host "Command: python -m pytest -q"
  Write-Host ""

  python -m pytest -q
  $PytestExit=$LASTEXITCODE

  Write-Host ""
  if ($PytestExit -ne 0) {
    throw "Repository-wide pytest failed with exit code $PytestExit."
  }

  Write-Host "=============================================================="
  Write-Host "Phase 144 repository-wide pytest: PASS"
  Write-Host "=============================================================="
}
finally {
  if ($null -eq $OldPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONPATH=$OldPythonPath
  }

  if ($null -eq $OldEncoding) {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONIOENCODING=$OldEncoding
  }

  if ($CreatedMarker -and (Test-Path $Marker)) {
    Remove-Item $Marker -Force
    Write-Host ""
    Write-Host "Temporary package marker removed: tests/__init__.py"
  }

  Stop-Transcript | Out-Null
}

Write-Host ""
Write-Host ("Output: " + $Output)
