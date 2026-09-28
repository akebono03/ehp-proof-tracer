param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$Candidate = Join-Path $env:TEMP "ehp_r4_r4_locator_candidate.ps1"

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

$oldBlock = @'
      $collectorOutput = & python ".\_r25_11_r6_r1_collector.py" 2>&1
      $collectorExitCode = $LASTEXITCODE
'@

$newBlock = @'
      $collectorOldErrorActionPreference = $ErrorActionPreference

      try {
        $ErrorActionPreference = "Continue"
        $collectorOutput = & python ".\_r25_11_r6_r1_collector.py" 2>&1
        $collectorExitCode = $LASTEXITCODE
      }
      finally {
        $ErrorActionPreference = $collectorOldErrorActionPreference
      }
'@

$occurrences = ([regex]::Matches(
  $source,
  [regex]::Escape($oldBlock)
)).Count

if ($occurrences -ne 1) {
  throw ("expected exactly one collector native-call block; found " + $occurrences)
}

$updated = $source.Replace($oldBlock, $newBlock)
Set-Content -Path $Candidate -Value $updated -Encoding UTF8
$candidateSource = Get-Content -Path $Candidate -Raw -Encoding UTF8

if (-not $candidateSource.Contains('$collectorOldErrorActionPreference = $ErrorActionPreference')) {
  throw "candidate collector EAP preservation missing"
}

if (-not $candidateSource.Contains('$collectorExitCode = $LASTEXITCODE')) {
  throw "candidate collector scalar exit-code capture missing"
}

if (-not $candidateSource.Contains('$result = "UNAVAILABLE:" + $lastOutputLine')) {
  throw "candidate collector failure conversion missing"
}

if (-not $candidateSource.Contains('& git worktree prune --expire now 1>$null 2>$null')) {
  throw "candidate lost prune contract"
}

if (-not $candidateSource.Contains("function Read-PopulationCache {")) {
  throw "candidate lost Read-PopulationCache"
}

if (-not $candidateSource.Contains('$addExitCode = $LASTEXITCODE')) {
  throw "candidate lost worktree-add scalar exit-code repair"
}

if (-not $candidateSource.Contains('$Expected = 190')) {
  throw "candidate lost expected population 190"
}

Write-Host "Candidate preservation preflight: PASS"
Assert-PowerShellParses -Path $Candidate -Label "Candidate locator"
Copy-Item -Path $Candidate -Destination $Locator -Force
Assert-PowerShellParses -Path $Locator -Label "Installed locator"
Remove-Item -Path $Candidate -Force -ErrorAction SilentlyContinue

Write-Host "R4-R4 collector native error handling installed."
Write-Host "Changed block: Measure-Commit collector native call only."
Write-Host "Collector Python changed: no."
Write-Host "Production changes: none."
Write-Host "Expected historical population remains 190."
