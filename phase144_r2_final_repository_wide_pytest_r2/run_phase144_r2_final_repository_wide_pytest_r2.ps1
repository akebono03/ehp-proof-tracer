$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path
$TestsDir = Join-Path $RepoRoot "tests"
$Marker = Join-Path $TestsDir "__init__.py"
$BackupMarker = Join-Path $PackageRoot "__init__.py.pre_final_backup"
$Transcript = Join-Path $PackageRoot "phase144_r2_final_repository_wide_pytest_r2.log"
$CollectionFile = Join-Path $PackageRoot "phase144_r2_final_collection_r2.txt"

$OldPythonPath = $env:PYTHONPATH
$OldEncoding = $env:PYTHONIOENCODING
$MarkerExisted = Test-Path $Marker
$MarkerTracked = $false
$MarkerBackedUp = $false
$CreatedMarker = $false
$PytestExit = $null

Start-Transcript -Path $Transcript -Force | Out-Null

try {
  Write-Host "=============================================================="
  Write-Host "Phase 144 R2 Final Repository-Wide Pytest R2"
  Write-Host "Runner-only repair: safe tests/__init__.py tracked detection"
  Write-Host "Canonical scope: tests/"
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Documentation changes: none"
  Write-Host "=============================================================="

  Write-Host ""
  Write-Host "A. Repository preflight..."
  Write-Host "Repo: $RepoRoot"
  git branch --show-current
  git rev-parse HEAD
  python --version
  python -m pytest --version

  Write-Host ""
  Write-Host "git status before final suite:"
  git status --short

  if (-not (Test-Path $TestsDir)) {
    throw "tests directory not found: $TestsDir"
  }

  $TrackedMarkerOutput = @(git ls-files -- "tests/__init__.py")
  $MarkerTracked = (
    $TrackedMarkerOutput.Count -gt 0 -and
    $TrackedMarkerOutput[0].Trim() -eq "tests/__init__.py"
  )

  Write-Host ""
  Write-Host "tests/__init__.py existed before runner: $MarkerExisted"
  Write-Host "tests/__init__.py tracked by git: $MarkerTracked"

  if ($MarkerExisted -and -not $MarkerTracked) {
    Copy-Item $Marker $BackupMarker -Force
    Remove-Item $Marker -Force
    $MarkerBackedUp = $true
    Write-Host "Untracked pre-existing tests/__init__.py backed up temporarily."
  }

  if (-not (Test-Path $Marker)) {
    New-Item -ItemType File -Path $Marker -Force | Out-Null
    $CreatedMarker = $true
    Write-Host "Temporary tests/__init__.py created for package imports."
  } else {
    Write-Host "Tracked tests/__init__.py retained."
  }

  $env:PYTHONPATH = "$RepoRoot;$TestsDir"
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host ""
  Write-Host "PYTHONPATH=$env:PYTHONPATH"

  Write-Host ""
  Write-Host "B. Dual import preflight..."
  python -c "import main; import tests.test_phase143_19_method_evidence; import tests.test_phase75_515_pi15_8_final_group; import tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation; print('Dual import preflight: PASS')"
  if ($LASTEXITCODE -ne 0) {
    throw "Dual import preflight failed. Repository-wide pytest was not started."
  }

  Write-Host ""
  Write-Host "C. Canonical collection preflight..."
  & python -m pytest tests --collect-only -q *> $CollectionFile
  $CollectionExit = $LASTEXITCODE
  if ($CollectionExit -ne 0) {
    Get-Content $CollectionFile
    throw "Collection preflight failed. Repository-wide pytest was not started."
  }

  Get-Content $CollectionFile | Select-Object -Last 5 | ForEach-Object {
    Write-Host $_
  }

  Write-Host ""
  Write-Host "D. Running the ONE final repository-wide suite..."
  Write-Host "Command: python -m pytest tests -q"
  Write-Host "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
  Write-Host ""

  & python -m pytest tests -q
  $PytestExit = $LASTEXITCODE

  Write-Host ""
  Write-Host "Finished: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
  Write-Host "pytest exit code: $PytestExit"

  if ($PytestExit -ne 0) {
    Write-Host ""
    Write-Host "FINAL SUITE: FAIL"
    Write-Host "Do not rerun the whole suite. Use the failure summary for focused repair."
    exit $PytestExit
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144 R2 final repository-wide pytest: PASS"
  Write-Host "This is the final whole-suite run for Phase 144."
  Write-Host "=============================================================="
}
finally {
  if ($null -eq $OldPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONPATH = $OldPythonPath
  }

  if ($null -eq $OldEncoding) {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONIOENCODING = $OldEncoding
  }

  if ($CreatedMarker -and (Test-Path $Marker)) {
    Remove-Item $Marker -Force
  }

  if ($MarkerBackedUp -and (Test-Path $BackupMarker)) {
    Copy-Item $BackupMarker $Marker -Force
    Remove-Item $BackupMarker -Force
    Write-Host "Original untracked tests/__init__.py restored."
  }

  Stop-Transcript | Out-Null
}
