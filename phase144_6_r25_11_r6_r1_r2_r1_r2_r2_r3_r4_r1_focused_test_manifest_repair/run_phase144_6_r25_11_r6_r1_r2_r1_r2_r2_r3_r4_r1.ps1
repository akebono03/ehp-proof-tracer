$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$R3TestSource = Join-Path $RepairDir "payload\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3.py"
$R3TestTarget = Join-Path $TargetDir "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3.py"
$R4TestSource = Join-Path $RepairDir "payload\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4.py"
$R4TestTarget = Join-Path $TargetDir "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4.py"

function Assert-PowerShellParses {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Path,

    [Parameter(Mandatory=$true)]
    [string]$Label
  )

  $parseErrors = $null
  $parseTokens = $null

  [void][System.Management.Automation.Language.Parser]::ParseFile(
    $Path,
    [ref]$parseTokens,
    [ref]$parseErrors
  )

  if ($parseErrors.Count -ne 0) {
    foreach ($parseError in $parseErrors) {
      Write-Host $parseError.Message
    }

    throw "$Label parser preflight failed."
  }

  Write-Host "$Label parser preflight: PASS"
}

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R4-R1"
Write-Host "Focused Test Manifest Repair"
Write-Host "Production changes: none"
Write-Host "Locator changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Verifying already-installed R4 locator..."
  Assert-PowerShellParses -Path $Locator -Label "Installed locator"

  $locatorSource = Get-Content -Path $Locator -Raw -Encoding UTF8

  if (-not $locatorSource.Contains('$addExitCode = $LASTEXITCODE')) {
    throw "Installed locator does not contain the R4 scalar add exit-code repair."
  }

  if (-not $locatorSource.Contains('$Expected = 190')) {
    throw "Installed locator no longer contains expected historical population 190."
  }

  Write-Host "Installed R4 scalar exit-code repair: PRESENT"
  Write-Host "Expected historical population 190: PRESENT"

  Write-Host ""
  Write-Host "B. Installing required audit-only tests..."
  Copy-Item -Path $R3TestSource -Destination $R3TestTarget -Force
  Copy-Item -Path $R4TestSource -Destination $R4TestTarget -Force
  Write-Host "R3 scalar exit-code audit test: PRESENT"
  Write-Host "R4 whole-function audit test: PRESENT"

  Write-Host ""
  Write-Host "C. Discovering historical-localization audit tests..."
  $testFiles = Get-ChildItem `
    -Path $TargetDir `
    -Filter "test_*.py" `
    -File |
    Sort-Object Name

  if ($testFiles.Count -eq 0) {
    throw "No historical-localization audit tests were found."
  }

  foreach ($testFile in $testFiles) {
    Write-Host ("test=" + $testFile.Name)
  }

  Write-Host ("focused_test_file_count=" + $testFiles.Count)

  Write-Host ""
  Write-Host "D. Running focused historical-localization audit directory..."
  $env:PYTHONPATH = $RepoRoot

  pytest -q $TargetDir

  $testExitCode = $LASTEXITCODE
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($testExitCode -ne 0) {
    throw "Focused historical-localization tests failed with exit code $testExitCode"
  }

  Write-Host ""
  Write-Host "E. Resuming historical 190 localization..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $Locator `
    -RepoRoot $RepoRoot `
    -PhaseDir $TargetDir

  $localizationExitCode = $LASTEXITCODE

  if ($localizationExitCode -ne 0) {
    throw "Historical 190 localization stopped with exit code $localizationExitCode"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R3-R4-R1 completed."
  Write-Host "No production files were modified."
  Write-Host "No locator functions were modified."
  Write-Host "No full project pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
