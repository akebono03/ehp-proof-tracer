param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$Candidate = Join-Path $env:TEMP "ehp_r4_r5_r1_locator_candidate.ps1"

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
  $isRegistered = Get-RegisteredAuditWorktreeState

  if ($isRegistered) {
'@

$newBlock = @'
  $isRegistered = $false
  $isRegistered = Get-RegisteredAuditWorktreeState

  if ($isRegistered) {
'@

$occurrences = ([regex]::Matches(
  $source,
  [regex]::Escape($oldBlock)
)).Count

if ($occurrences -ne 1) {
  throw ("expected exactly one registration assignment block; found " + $occurrences)
}

$updated = $source.Replace($oldBlock, $newBlock)
Set-Content -Path $Candidate -Value $updated -Encoding UTF8
$candidateSource = Get-Content -Path $Candidate -Raw -Encoding UTF8

$required = @(
  '$isRegistered = $false',
  '$isRegistered = Get-RegisteredAuditWorktreeState',
  '$stillRegistered = Get-RegisteredAuditWorktreeState',
  'Remove-StaleAuditWorktreePath',
  '& git worktree prune --expire now 1>$null 2>$null',
  '$collectorExitCode = $LASTEXITCODE',
  'function Read-PopulationCache {',
  '$Expected = 190'
)

foreach ($item in $required) {
  if (-not $candidateSource.Contains($item)) {
    throw ("candidate preservation check missing: " + $item)
  }
}

Write-Host "Candidate compatibility preflight: PASS"
Assert-PowerShellParses -Path $Candidate -Label "Candidate locator"
Copy-Item -Path $Candidate -Destination $Locator -Force
Assert-PowerShellParses -Path $Locator -Label "Installed locator"
Remove-Item -Path $Candidate -Force -ErrorAction SilentlyContinue

Write-Host "R4-R5-R1 registration contract compatibility installed."
Write-Host "Semantic cleanup behavior changed: no."
Write-Host "Production changes: none."
Write-Host "Expected historical population remains 190."
