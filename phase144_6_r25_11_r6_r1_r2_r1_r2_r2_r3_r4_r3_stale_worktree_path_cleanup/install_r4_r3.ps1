param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot,

  [Parameter(Mandatory=$true)]
  [string]$RepairDir
)

$ErrorActionPreference = "Stop"

$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$Payload = Join-Path $RepairDir "payload\Remove-TemporaryWorktree.ps1.txt"
$Candidate = Join-Path $env:TEMP "ehp_r25_11_r6_r1_r4_r3_locator_candidate.ps1"

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
$replacement = Get-Content -Path $Payload -Raw -Encoding UTF8
$startMarker = "function Remove-TemporaryWorktree {"
$nextMarker = "function Read-PopulationCache {"
$start = $source.IndexOf($startMarker)
$next = $source.IndexOf($nextMarker)

if ($start -lt 0) {
  throw "Remove-TemporaryWorktree marker was not found."
}

if ($next -le $start) {
  throw "Read-PopulationCache boundary was not found after Remove-TemporaryWorktree."
}

$prefix = $source.Substring(0, $start)
$suffix = $source.Substring($next)
$updated = $prefix + $replacement
$updated = $updated + "`r`n"
$updated = $updated + $suffix

Set-Content -Path $Candidate -Value $updated -Encoding UTF8

$candidateSource = Get-Content -Path $Candidate -Raw -Encoding UTF8

if (-not $candidateSource.Contains("function Read-PopulationCache {")) {
  throw "candidate lost Read-PopulationCache"
}

if (-not $candidateSource.Contains('$addExitCode = $LASTEXITCODE')) {
  throw "candidate lost scalar add exit-code repair"
}

if (-not $candidateSource.Contains('$Expected = 190')) {
  throw "candidate lost expected population 190"
}

Write-Host "Candidate preservation preflight: PASS"
Assert-PowerShellParses -Path $Candidate -Label "Candidate locator"

Copy-Item -Path $Candidate -Destination $Locator -Force
Assert-PowerShellParses -Path $Locator -Label "Installed locator"

Remove-Item -Path $Candidate -Force -ErrorAction SilentlyContinue

Write-Host "R4-R3 stale worktree path cleanup repair installed."
Write-Host "Changed function: Remove-TemporaryWorktree."
Write-Host "Measure-Commit changed: no."
Write-Host "Read-PopulationCache changed: no."
Write-Host "Production changes: none."
Write-Host "Expected historical population remains 190."
