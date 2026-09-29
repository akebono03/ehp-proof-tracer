param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot,

  [Parameter(Mandatory=$true)]
  [string]$RepairDir
)

$ErrorActionPreference = "Stop"

$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$Payload = Join-Path $RepairDir "payload\Read-PopulationCache.ps1.txt"
$Candidate = Join-Path $env:TEMP "ehp_r25_11_r6_r1_r4_r2_locator_candidate.ps1"

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
      $lineNumber = $parseError.Extent.StartLineNumber
      $columnNumber = $parseError.Extent.StartColumnNumber
      $message = "line=" + $lineNumber
      $message = $message + " column=" + $columnNumber
      $message = $message + " "
      $message = $message + $parseError.Message
      Write-Host $message
    }

    throw "$Label parser preflight failed."
  }

  Write-Host "$Label parser preflight: PASS"
}

$source = Get-Content -Path $Locator -Raw -Encoding UTF8
$replacement = Get-Content -Path $Payload -Raw -Encoding UTF8

if ($source.Contains("function Read-PopulationCache {")) {
  Write-Host "Read-PopulationCache already present; no insertion required."
  Set-Content -Path $Candidate -Value $source -Encoding UTF8
}
else {
  $marker = "function Write-PopulationCache {"
  $index = $source.IndexOf($marker)

  if ($index -lt 0) {
    throw "Write-PopulationCache insertion marker was not found."
  }

  $prefix = $source.Substring(0, $index)
  $suffix = $source.Substring($index)
  $updated = $prefix + $replacement
  $updated = $updated + "`r`n"
  $updated = $updated + $suffix
  Set-Content -Path $Candidate -Value $updated -Encoding UTF8
}

$candidateSource = Get-Content -Path $Candidate -Raw -Encoding UTF8

$readCount = (
  [regex]::Matches(
    $candidateSource,
    [regex]::Escape("function Read-PopulationCache {")
  )
).Count

$writeCount = (
  [regex]::Matches(
    $candidateSource,
    [regex]::Escape("function Write-PopulationCache {")
  )
).Count

$measureCount = (
  [regex]::Matches(
    $candidateSource,
    [regex]::Escape("function Measure-Commit {")
  )
).Count

if ($readCount -ne 1) {
  throw ("candidate Read-PopulationCache count=" + $readCount)
}

if ($writeCount -ne 1) {
  throw ("candidate Write-PopulationCache count=" + $writeCount)
}

if ($measureCount -ne 1) {
  throw ("candidate Measure-Commit count=" + $measureCount)
}

if (-not $candidateSource.Contains('$addExitCode = $LASTEXITCODE')) {
  throw "candidate lost R4 scalar add exit-code repair"
}

if (-not $candidateSource.Contains('$Expected = 190')) {
  throw "candidate lost expected historical population 190"
}

Write-Host "Candidate helper-chain structural preflight: PASS"
Assert-PowerShellParses -Path $Candidate -Label "Candidate locator"

Copy-Item -Path $Candidate -Destination $Locator -Force
Assert-PowerShellParses -Path $Locator -Label "Installed locator"

Remove-Item -Path $Candidate -Force -ErrorAction SilentlyContinue

Write-Host "Read-PopulationCache restoration installed."
Write-Host "Remove-TemporaryWorktree changed: no."
Write-Host "Measure-Commit changed: no."
Write-Host "Production changes: none."
Write-Host "Population cache contents changed: no."
Write-Host "Expected historical population remains 190."
