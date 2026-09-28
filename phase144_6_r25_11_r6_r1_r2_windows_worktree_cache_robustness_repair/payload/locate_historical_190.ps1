param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot,

  [Parameter(Mandatory=$true)]
  [string]$PhaseDir
)

$ErrorActionPreference = "Stop"

$Expected = 190
$CachePath = Join-Path $PhaseDir "population_cache.tsv"
$Worktree = Join-Path $RepoRoot ".phase144_6_r25_11_r6_r1_worktree"
$CollectorSource = Join-Path $PhaseDir "collect_selected_total.py"
$FoundationPath = (
  "tests/test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"
)

$Pathspecs = @(
  "toda_group_proof_narrative_argument_multi_renderer.py",
  "toda_group_proof_narrative_argument_body_renderer.py",
  "toda_group_proof_narrative_contribution_ordering.py",
  "toda_group_proof_narrative_contribution_renderer.py",
  "toda_group_proof_narrative_hidden_bridge_semantics.py",
  "toda_group_proof_narrative_renderer.py",
  "toda_group_proof_narrative_semantics.py"
)

function Invoke-WithRetry {
  param(
    [Parameter(Mandatory=$true)]
    [scriptblock]$Action,

    [Parameter(Mandatory=$true)]
    [string]$Description,

    [int]$Attempts = 8,

    [int]$DelayMilliseconds = 400
  )

  $lastError = $null

  for ($attempt = 1; $attempt -le $Attempts; $attempt++) {
    try {
      & $Action
      return
    }
    catch {
      $lastError = $_
      if ($attempt -ge $Attempts) {
        break
      }

      Start-Sleep -Milliseconds (
        $DelayMilliseconds
        * $attempt
      )
    }
  }

  throw (
    "$Description failed after $Attempts attempts. " +
    "$($lastError.Exception.Message)"
  )
}

function Test-FoundationAtCommit {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Sha
  )

  & git cat-file `
    -e `
    "${Sha}:$FoundationPath" `
    2>$null

  return (
    $LASTEXITCODE
    -eq 0
  )
}

function Remove-TemporaryWorktree {
  if (-not (Test-Path $Worktree)) {
    & git worktree prune --expire now 2>$null | Out-Null
    return
  }

  $oldPrompt = $env:GIT_TERMINAL_PROMPT
  $env:GIT_TERMINAL_PROMPT = "0"

  try {
    Invoke-WithRetry `
      -Description "temporary worktree removal" `
      -Action {
        & git worktree remove `
          --force `
          $Worktree `
          2>$null `
          | Out-Null

        if ($LASTEXITCODE -ne 0) {
          throw (
            "git worktree remove exit code " +
            "$LASTEXITCODE"
          )
        }
      }
  }
  finally {
    if ($null -eq $oldPrompt) {
      Remove-Item Env:GIT_TERMINAL_PROMPT `
        -ErrorAction SilentlyContinue
    }
    else {
      $env:GIT_TERMINAL_PROMPT = $oldPrompt
    }
  }

  Invoke-WithRetry `
    -Description "git worktree prune" `
    -Action {
      & git worktree prune `
        --expire now `
        2>$null `
        | Out-Null

      if ($LASTEXITCODE -ne 0) {
        throw (
          "git worktree prune exit code " +
          "$LASTEXITCODE"
        )
      }
    }
}

function Write-PopulationCache {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Sha,

    [Parameter(Mandatory=$true)]
    [string]$Result
  )

  $line = "$Sha`t$Result"
  $tempPath = (
    $CachePath
    + ".tmp."
    + $PID
  )

  Invoke-WithRetry `
    -Description "population cache update" `
    -Action {
      $existing = @()

      if (Test-Path $CachePath) {
        $existing = @(
          Get-Content `
            -Path $CachePath `
            -Encoding UTF8
        )
      }

      $filtered = @(
        $existing
        | Where-Object {
          -not $_.StartsWith(
            "$Sha`t"
          )
        }
      )

      $newContent = @(
        $filtered
        + $line
      )

      Set-Content `
        -Path $tempPath `
        -Value $newContent `
        -Encoding UTF8

      Move-Item `
        -Path $tempPath `
        -Destination $CachePath `
        -Force
    }

  if (Test-Path $tempPath) {
    Remove-Item `
      -Path $tempPath `
      -Force `
      -ErrorAction SilentlyContinue
  }
}

$cache = @{}
if (Test-Path $CachePath) {
  Invoke-WithRetry `
    -Description "population cache read" `
    -Action {
      $cacheLines = @(
        Get-Content `
          -Path $CachePath `
          -Encoding UTF8
      )
    }

  foreach ($line in $cacheLines) {
    $parts = $line -split "`t", 3
    if ($parts.Count -ge 2) {
      $cache[$parts[0]] = $parts[1]
    }
  }
}

function Get-CandidateCommits {
  $gitArguments = @(
    "log",
    "--format=%H`t%s",
    "--reverse",
    "--all",
    "--"
  ) + $Pathspecs

  $lines = & git @gitArguments
  if ($LASTEXITCODE -ne 0) {
    throw (
      "git log failed with exit code " +
      "$LASTEXITCODE"
    )
  }

  $seen = @{}
  $rows = @()

  foreach ($line in $lines) {
    $parts = $line -split "`t", 2
    if ($parts.Count -ne 2) {
      continue
    }

    $sha = $parts[0]
    if ($seen.ContainsKey($sha)) {
      continue
    }

    $seen[$sha] = $true
    $rows += [PSCustomObject]@{
      Sha = $sha
      Subject = $parts[1]
    }
  }

  return $rows
}

function Measure-Commit {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Sha
  )

  if ($cache.ContainsKey($Sha)) {
    return [PSCustomObject]@{
      Status = "cached"
      Result = $cache[$Sha]
    }
  }

  if (-not (Test-FoundationAtCommit -Sha $Sha)) {
    $result = "UNAVAILABLE:foundation"
    Write-PopulationCache `
      -Sha $Sha `
      -Result $result
    $cache[$Sha] = $result

    return [PSCustomObject]@{
      Status = "measured"
      Result = $result
    }
  }

  Remove-TemporaryWorktree

  $oldPrompt = $env:GIT_TERMINAL_PROMPT
  $env:GIT_TERMINAL_PROMPT = "0"

  try {
    Invoke-WithRetry `
      -Description "temporary worktree creation for $Sha" `
      -Action {
        & git worktree add `
          --detach `
          $Worktree `
          $Sha `
          2>$null `
          | Out-Null

        if ($LASTEXITCODE -ne 0) {
          throw (
            "git worktree add exit code " +
            "$LASTEXITCODE"
          )
        }
      }
  }
  finally {
    if ($null -eq $oldPrompt) {
      Remove-Item Env:GIT_TERMINAL_PROMPT `
        -ErrorAction SilentlyContinue
    }
    else {
      $env:GIT_TERMINAL_PROMPT = $oldPrompt
    }
  }

  try {
    $collector = Join-Path `
      $Worktree `
      "_r25_11_r6_r1_collector.py"

    Copy-Item `
      $CollectorSource `
      $collector `
      -Force

    Push-Location $Worktree
    try {
      $env:PYTHONPATH = $Worktree
      $env:PYTHONUTF8 = "1"

      $collectorOutput = @(
        & python `
          ".\_r25_11_r6_r1_collector.py" `
          2>&1
      )
      $collectorExitCode = $LASTEXITCODE
    }
    finally {
      Remove-Item Env:PYTHONPATH `
        -ErrorAction SilentlyContinue
      Remove-Item Env:PYTHONUTF8 `
        -ErrorAction SilentlyContinue
      Pop-Location
    }

    if ($collectorExitCode -ne 0) {
      $lastOutputLine = (
        $collectorOutput
        | Select-Object -Last 1
      )
      $result = (
        "UNAVAILABLE:"
        + $lastOutputLine
      )
    }
    else {
      $totalLines = @(
        $collectorOutput
        | Where-Object {
          $_ -like "TOTAL=*"
        }
      )
      $result = (
        $totalLines
        | Select-Object -Last 1
      )

      if (-not $result) {
        $result = "UNAVAILABLE:no-total"
      }
    }
  }
  finally {
    Remove-TemporaryWorktree
  }

  Write-PopulationCache `
    -Sha $Sha `
    -Result $result
  $cache[$Sha] = $result

  return [PSCustomObject]@{
    Status = "measured"
    Result = $result
  }
}

function Parse-Total {
  param(
    [string]$Result
  )

  if ($Result -match "^TOTAL=(\d+);") {
    return [int]$Matches[1]
  }

  return $null
}

$candidates = Get-CandidateCommits

Write-Host "=============================================================================="
Write-Host "A. Historical production-changing commit candidates"
Write-Host "=============================================================================="
Write-Host "candidate_count=$($candidates.Count)"
Write-Host "expected_selected=$Expected"
Write-Host "cache=$CachePath"

$measurable = @()
$exact = @()

Write-Host ""
Write-Host "=============================================================================="
Write-Host "B. Population localization"
Write-Host "=============================================================================="

foreach ($candidate in $candidates) {
  $measurement = Measure-Commit `
    -Sha $candidate.Sha
  $total = Parse-Total `
    -Result $measurement.Result

  if ($null -eq $total) {
    Write-Host (
      "$($candidate.Sha.Substring(0, 10)) " +
      "status=$($measurement.Status) " +
      "$($measurement.Result) " +
      "subject=$($candidate.Subject)"
    )
    continue
  }

  $row = [PSCustomObject]@{
    Sha = $candidate.Sha
    Subject = $candidate.Subject
    Total = $total
    Result = $measurement.Result
    Status = $measurement.Status
  }
  $measurable += $row

  $marker = ""
  if ($total -eq $Expected) {
    $marker = " <== EXACT_190"
    $exact += $row
  }

  Write-Host (
    "$($candidate.Sha.Substring(0, 10)) " +
    "selected=$total " +
    "status=$($measurement.Status)" +
    "$marker " +
    "subject=$($candidate.Subject)"
  )
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "C. Exact-190 localization result"
Write-Host "=============================================================================="

if ($exact.Count -eq 0) {
  Write-Host "EXACT_190_COUNT=0"
  Write-Host "No historical commit in the production-changing candidate set reproduced 190."
  Write-Host "Do not run a 190->192 exact-delta comparison yet."
  exit 4
}

Write-Host "EXACT_190_COUNT=$($exact.Count)"
foreach ($row in $exact) {
  Write-Host "EXACT_190_SHA=$($row.Sha)"
  Write-Host "EXACT_190_SUBJECT=$($row.Subject)"
  Write-Host "EXACT_190_COUNTS=$($row.Result)"
}

$firstExact = $exact[0]
$index = -1

for ($i = 0; $i -lt $measurable.Count; $i++) {
  if ($measurable[$i].Sha -eq $firstExact.Sha) {
    $index = $i
    break
  }
}

Write-Host ""
Write-Host "First exact-190 measurable neighbors:"

if ($index -gt 0) {
  $previous = $measurable[$index - 1]
  Write-Host (
    "PREVIOUS_SHA=$($previous.Sha) " +
    "selected=$($previous.Total) " +
    "subject=$($previous.Subject)"
  )
}

Write-Host (
  "CURRENT_SHA=$($firstExact.Sha) " +
  "selected=$($firstExact.Total) " +
  "subject=$($firstExact.Subject)"
)

if (
  $index -ge 0 -and
  $index + 1 -lt $measurable.Count
) {
  $next = $measurable[$index + 1]
  Write-Host (
    "NEXT_SHA=$($next.Sha) " +
    "selected=$($next.Total) " +
    "subject=$($next.Subject)"
  )
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "D. Localization completion"
Write-Host "=============================================================================="
Write-Host "Historical exact-190 commit localization: PASS"
Write-Host "No production changes."
Write-Host "No existing test changes."
Write-Host "No full pytest."
exit 0
