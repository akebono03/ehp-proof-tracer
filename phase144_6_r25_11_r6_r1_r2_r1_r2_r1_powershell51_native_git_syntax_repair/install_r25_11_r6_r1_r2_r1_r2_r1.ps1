param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot,

  [Parameter(Mandatory=$true)]
  [string]$RepairDir
)

$ErrorActionPreference = "Stop"

$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$FunctionPayload = Join-Path $RepairDir "payload\Test-FoundationAtCommit.ps1.txt"
$Candidate = Join-Path $env:TEMP "ehp_r25_11_r6_r1_r2_r1_r2_r1_locator_candidate.ps1"

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
      Write-Host $parseError.Message
    }

    throw "$Label parser preflight failed."
  }

  Write-Host "$Label parser preflight: PASS"
}

if (-not (Test-Path $Locator)) {
  throw "Missing historical locator: $Locator"
}

if (-not (Test-Path $FunctionPayload)) {
  throw "Missing function payload: $FunctionPayload"
}

$source = Get-Content -Path $Locator -Raw -Encoding UTF8
$replacement = Get-Content -Path $FunctionPayload -Raw -Encoding UTF8

$startMarker = "function Test-FoundationAtCommit {"
$nextMarker = "function Remove-TemporaryWorktree {"

$startIndex = $source.IndexOf($startMarker)
$nextIndex = $source.IndexOf($nextMarker)

if ($startIndex -lt 0) {
  throw "Test-FoundationAtCommit start marker was not found."
}

if ($nextIndex -lt 0) {
  throw "Remove-TemporaryWorktree marker was not found."
}

if ($nextIndex -le $startIndex) {
  throw "Locator function markers are out of order."
}

$prefix = $source.Substring(0, $startIndex)
$suffix = $source.Substring($nextIndex)
$candidateSource = $prefix + $replacement + "`r`n" + $suffix

Set-Content `
  -Path $Candidate `
  -Value $candidateSource `
  -Encoding UTF8

Write-Host "Candidate locator created without modifying installed locator."
Assert-PowerShellParses `
  -Path $Candidate `
  -Label "Candidate locator"

Copy-Item `
  -Path $Candidate `
  -Destination $Locator `
  -Force

Assert-PowerShellParses `
  -Path $Locator `
  -Label "Installed locator"

Remove-Item `
  -Path $Candidate `
  -Force `
  -ErrorAction SilentlyContinue

Write-Host "R25-11-R6-R1-R2-R1-R2-R1 syntax repair installed transactionally."
Write-Host "Changed locator function: Test-FoundationAtCommit."
Write-Host "Production changes: none."
Write-Host "Existing project tests changed: none."
Write-Host "Expected historical population remains 190."
Write-Host "Existing population cache is preserved."
