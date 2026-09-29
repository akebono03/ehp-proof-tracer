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
$AddPayload = Join-Path $RepairDir "payload\Measure-Commit-worktree-add.ps1.txt"
$Candidate = Join-Path $env:TEMP "ehp_r25_11_r6_r1_r2_r1_r2_r2_r3_locator_candidate.ps1"

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

$source = Get-Content -Path $Locator -Raw -Encoding UTF8
$removeReplacement = Get-Content -Path $RemovePayload -Raw -Encoding UTF8
$addReplacement = Get-Content -Path $AddPayload -Raw -Encoding UTF8

$removeStartMarker = "function Remove-TemporaryWorktree {"
$removeNextMarker = "function Write-PopulationCache {"
$removeStart = $source.IndexOf($removeStartMarker)
$removeNext = $source.IndexOf($removeNextMarker)

if ($removeStart -lt 0 -or $removeNext -le $removeStart) {
  throw "Remove-TemporaryWorktree replacement markers were not found."
}

$source = (
  $source.Substring(0, $removeStart)
  + $removeReplacement
  + "`r`n"
  + $source.Substring($removeNext)
)

$measureStart = $source.IndexOf("function Measure-Commit {")
if ($measureStart -lt 0) {
  throw "Measure-Commit was not found."
}

$collectorMarker = "  try {`r`n    `$collector = Join-Path"
$collectorIndex = $source.IndexOf($collectorMarker, $measureStart)

if ($collectorIndex -lt 0) {
  $collectorMarker = "  try {`n    `$collector = Join-Path"
  $collectorIndex = $source.IndexOf($collectorMarker, $measureStart)
}

if ($collectorIndex -lt 0) {
  throw "Measure-Commit collector boundary was not found."
}

$creationStart = $source.LastIndexOf(
  "    Invoke-WithRetry",
  $collectorIndex
)

if ($creationStart -lt $measureStart) {
  throw "Measure-Commit worktree creation block was not found."
}

$source = (
  $source.Substring(0, $creationStart)
  + $addReplacement
  + $source.Substring($collectorIndex)
)

Set-Content -Path $Candidate -Value $source -Encoding UTF8
Assert-PowerShellParses -Path $Candidate -Label "Candidate locator"

Copy-Item -Path $Candidate -Destination $Locator -Force
Assert-PowerShellParses -Path $Locator -Label "Installed locator"

Remove-Item -Path $Candidate -Force -ErrorAction SilentlyContinue

Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R3 scalar exit-code repair installed."
Write-Host "Changed function: Remove-TemporaryWorktree."
Write-Host "Changed method body region: Measure-Commit worktree-add action."
Write-Host "Production changes: none."
Write-Host "Existing project tests changed: none."
Write-Host "Expected historical population remains 190."
Write-Host "Existing population cache is preserved."
