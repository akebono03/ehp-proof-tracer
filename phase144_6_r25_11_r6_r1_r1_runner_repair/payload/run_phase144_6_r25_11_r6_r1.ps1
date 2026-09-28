$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir
$Locator = Join-Path $PhaseDir "locate_historical_190.ps1"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R1 runner repair"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONUTF8 = "1"

  Write-Host ""
  Write-Host "A. Python syntax preflight..."
  python -m py_compile `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\collect_selected_total.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r1.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Python syntax preflight failed with exit code $LASTEXITCODE"
  }

  Write-Host ""
  Write-Host "B. PowerShell parser preflight..."
  $parseErrors = $null
  $parseTokens = $null
  [void][System.Management.Automation.Language.Parser]::ParseFile(
    $Locator,
    [ref]$parseTokens,
    [ref]$parseErrors
  )

  if ($parseErrors.Count -ne 0) {
    foreach ($parseError in $parseErrors) {
      Write-Host $parseError.Message
    }
    throw "PowerShell parser preflight failed."
  }

  Write-Host "PowerShell parser preflight: PASS"

  Write-Host ""
  Write-Host "C. Lightweight runner-repair tests..."
  pytest -q `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r1.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Runner-repair tests failed with exit code $LASTEXITCODE"
  }

  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue

  Write-Host ""
  Write-Host "D. Historical 190 localization..."
  & powershell `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File $Locator `
    -RepoRoot $RepoRoot `
    -PhaseDir $PhaseDir

  $localizationExitCode = $LASTEXITCODE
  if ($localizationExitCode -ne 0) {
    throw (
      "Historical 190 localization failed or stopped " +
      "with exit code $localizationExitCode."
    )
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R6-R1-R1 completed."
  Write-Host "Please paste Sections B-D from the localization output."
  Write-Host "Population measurements are cached for reruns."
  Write-Host "No production files were modified."
  Write-Host "No existing tests were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  Pop-Location
}
