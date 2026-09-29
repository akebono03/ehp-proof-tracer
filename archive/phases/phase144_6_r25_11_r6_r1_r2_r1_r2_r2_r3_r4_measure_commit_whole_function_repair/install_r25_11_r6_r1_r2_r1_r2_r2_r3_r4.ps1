param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot,

  [Parameter(Mandatory=$true)]
  [string]$RepairDir
)

$ErrorActionPreference = "Stop"

$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$RemovePayload = Join-Path $RepairDir "payload\Remove-TemporaryWorktree.ps1.txt"
$MeasurePayload = Join-Path $RepairDir "payload\Measure-Commit.ps1.txt"
$Candidate = Join-Path $env:TEMP "ehp_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_locator_candidate.ps1"

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
    Write-Host "$Label parser errors:"

    foreach ($parseError in $parseErrors) {
      $lineNumber = $parseError.Extent.StartLineNumber
      $columnNumber = $parseError.Extent.StartColumnNumber
      $errorText = $parseError.Extent.Text
      $message = "line=" + $lineNumber
      $message = $message + " column=" + $columnNumber
      $message = $message + " text=[" + $errorText + "] "
      $message = $message + $parseError.Message
      Write-Host $message
    }

    throw "$Label parser preflight failed."
  }

  Write-Host "$Label parser preflight: PASS"
}

function Replace-FunctionByNextFunction {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Source,

    [Parameter(Mandatory=$true)]
    [string]$FunctionMarker,

    [Parameter(Mandatory=$true)]
    [string]$NextFunctionMarker,

    [Parameter(Mandatory=$true)]
    [string]$Replacement
  )

  $start = $Source.IndexOf($FunctionMarker)
  $next = $Source.IndexOf($NextFunctionMarker)

  if ($start -lt 0) {
    throw ("Function marker not found: " + $FunctionMarker)
  }

  if ($next -le $start) {
    throw ("Next function marker not found after target: " + $NextFunctionMarker)
  }

  $prefix = $Source.Substring(0, $start)
  $suffix = $Source.Substring($next)
  $updated = $prefix + $Replacement
  $updated = $updated + "`r`n"
  $updated = $updated + $suffix
  return $updated
}

function Assert-CandidateStructure {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Source
  )

  $measureCount = (
    [regex]::Matches(
      $Source,
      [regex]::Escape("function Measure-Commit {")
    )
  ).Count

  $parseCount = (
    [regex]::Matches(
      $Source,
      [regex]::Escape("function Parse-Total {")
    )
  ).Count

  if ($measureCount -ne 1) {
    throw ("candidate Measure-Commit count=" + $measureCount)
  }

  if ($parseCount -ne 1) {
    throw ("candidate Parse-Total count=" + $parseCount)
  }

  if (-not $Source.Contains('$addExitCode = $LASTEXITCODE')) {
    throw "candidate scalar add exit-code assignment missing"
  }

  if (-not $Source.Contains('$Expected = 190')) {
    throw "candidate expected historical population 190 missing"
  }

  Write-Host "Candidate structural preflight: PASS"
}

$source = Get-Content -Path $Locator -Raw -Encoding UTF8
$removeReplacement = Get-Content -Path $RemovePayload -Raw -Encoding UTF8
$measureReplacement = Get-Content -Path $MeasurePayload -Raw -Encoding UTF8

$source = Replace-FunctionByNextFunction `
  -Source $source `
  -FunctionMarker "function Remove-TemporaryWorktree {" `
  -NextFunctionMarker "function Write-PopulationCache {" `
  -Replacement $removeReplacement

$source = Replace-FunctionByNextFunction `
  -Source $source `
  -FunctionMarker "function Measure-Commit {" `
  -NextFunctionMarker "function Parse-Total {" `
  -Replacement $measureReplacement

Assert-CandidateStructure -Source $source

Set-Content -Path $Candidate -Value $source -Encoding UTF8
Assert-PowerShellParses -Path $Candidate -Label "Candidate locator"

Copy-Item -Path $Candidate -Destination $Locator -Force
Assert-PowerShellParses -Path $Locator -Label "Installed locator"

Remove-Item -Path $Candidate -Force -ErrorAction SilentlyContinue

Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R3-R4 whole-function repair installed."
Write-Host "Changed function: Remove-TemporaryWorktree."
Write-Host "Changed function: Measure-Commit."
Write-Host "Production changes: none."
Write-Host "Existing project tests changed: none."
Write-Host "Expected historical population remains 190."
Write-Host "Existing population cache is preserved."
