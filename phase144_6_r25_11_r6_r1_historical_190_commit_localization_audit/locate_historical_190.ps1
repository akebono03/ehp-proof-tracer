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
$FoundationPath = "tests/test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"

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
  $attempt = 1

  while ($attempt -le $Attempts) {
    try {
      & $Action
      return
    }
    catch {
      $lastError = $_

      if ($attempt -ge $Attempts) {
        break
      }

      $delay = $DelayMilliseconds * $attempt
      Start-Sleep -Milliseconds $delay
      $attempt = $attempt + 1
    }
  }

  $message = $lastError.Exception.Message
  throw "$Description failed after $Attempts attempts. $message"
}

function Test-FoundationAtCommit {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Sha
  )

  $commitObjectName = $Sha + "^{commit}"
  $commitStderrName = "ehp_r25_11_r6_r1_commit_" + $PID + ".stderr.txt"
  $commitStderrPath = Join-Path $env:TEMP $commitStderrName
  $oldErrorActionPreference = $ErrorActionPreference
  $commitExitCode = $null

  try {
    $ErrorActionPreference = "Continue"
    & git cat-file -e $commitObjectName 2>$commitStderrPath
    $commitExitCode = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldErrorActionPreference
  }

  if ($commitExitCode -ne 0) {
    $commitStderrText = ""

    if (Test-Path $commitStderrPath) {
      $commitStderrLines = Get-Content -Path $commitStderrPath -Encoding UTF8
      $commitStderrText = $commitStderrLines -join " "
      Remove-Item $commitStderrPath -Force -ErrorAction SilentlyContinue
    }

    $message = "git commit-object check failed for " + $Sha
    $message = $message + " with exit code " + $commitExitCode
    $message = $message + ": " + $commitStderrText
    throw $message
  }

  if (Test-Path $commitStderrPath) {
    Remove-Item $commitStderrPath -Force -ErrorAction SilentlyContinue
  }

  $foundationObjectName = "${Sha}:$FoundationPath"
  $foundationStderrName = "ehp_r25_11_r6_r1_foundation_" + $PID + ".stderr.txt"
  $foundationStderrPath = Join-Path $env:TEMP $foundationStderrName
  $foundationExitCode = $null

  try {
    $ErrorActionPreference = "Continue"
    & git cat-file -e $foundationObjectName 2>$foundationStderrPath
    $foundationExitCode = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldErrorActionPreference
  }

  if ($foundationExitCode -eq 0) {
    if (Test-Path $foundationStderrPath) {
      Remove-Item $foundationStderrPath -Force -ErrorAction SilentlyContinue
    }

    return $true
  }

  if (Test-Path $foundationStderrPath) {
    Remove-Item $foundationStderrPath -Force -ErrorAction SilentlyContinue
  }

  return $false
}

function Remove-TemporaryWorktree {
  if (-not (Test-Path $Worktree)) {
    return
  }

  function Get-RegisteredAuditWorktreeState {
    $oldErrorActionPreference = $ErrorActionPreference
    $registeredLines = $null
    $listExitCode = $null

    try {
      $ErrorActionPreference = "Continue"
      $registeredLines = & git worktree list --porcelain 2>$null
      $listExitCode = $LASTEXITCODE
    }
    finally {
      $ErrorActionPreference = $oldErrorActionPreference
    }

    if ($listExitCode -ne 0) {
      $message = "git worktree list exit code "
      $message = $message + $listExitCode
      throw $message
    }

    $normalizedTarget = [System.IO.Path]::GetFullPath($Worktree)

    foreach ($registeredLine in $registeredLines) {
      if ($registeredLine -like "worktree *") {
        $registeredPath = $registeredLine.Substring(9)
        $normalizedRegistered = [System.IO.Path]::GetFullPath($registeredPath)

        if ($normalizedRegistered -eq $normalizedTarget) {
          return $true
        }
      }
    }

    return $false
  }

  function Remove-StaleAuditWorktreePath {
    if (-not (Test-Path $Worktree)) {
      return
    }

    $normalizedTarget = [System.IO.Path]::GetFullPath($Worktree)
    $expectedLeaf = ".phase144_6_r25_11_r6_r1_worktree"
    $actualLeaf = Split-Path -Leaf $normalizedTarget

    if ($actualLeaf -ne $expectedLeaf) {
      $message = "refusing unregistered path cleanup outside audit worktree: "
      $message = $message + $normalizedTarget
      throw $message
    }

    Invoke-WithRetry `
      -Description "stale unregistered audit worktree path cleanup" `
      -Action {
        Remove-Item `
          -LiteralPath $normalizedTarget `
          -Recurse `
          -Force `
          -ErrorAction Stop
      }
  }

  $isRegistered = $false
  $isRegistered = Get-RegisteredAuditWorktreeState

  if ($isRegistered) {
    $oldPrompt = $env:GIT_TERMINAL_PROMPT
    $env:GIT_TERMINAL_PROMPT = "0"
    $removeExitCode = $null

    try {
      $oldErrorActionPreference = $ErrorActionPreference

      try {
        $ErrorActionPreference = "Continue"
        & git worktree remove --force $Worktree 1>$null 2>$null
        $removeExitCode = $LASTEXITCODE
      }
      finally {
        $ErrorActionPreference = $oldErrorActionPreference
      }
    }
    finally {
      if ($null -eq $oldPrompt) {
        Remove-Item Env:GIT_TERMINAL_PROMPT -ErrorAction SilentlyContinue
      }
      else {
        $env:GIT_TERMINAL_PROMPT = $oldPrompt
      }
    }

    if ($removeExitCode -ne 0) {
      $stillRegistered = Get-RegisteredAuditWorktreeState

      if ($stillRegistered) {
        $message = "git worktree remove exit code "
        $message = $message + $removeExitCode
        throw $message
      }

      Remove-StaleAuditWorktreePath
    }
  }
  else {
    Remove-StaleAuditWorktreePath
  }

  Invoke-WithRetry `
    -Description "git worktree prune" `
    -Action {
      $oldErrorActionPreference = $ErrorActionPreference
      $pruneExitCode = $null

      try {
        $ErrorActionPreference = "Continue"
        & git worktree prune --expire now 1>$null 2>$null
        $pruneExitCode = $LASTEXITCODE
      }
      finally {
        $ErrorActionPreference = $oldErrorActionPreference
      }

      if ($pruneExitCode -ne 0) {
        $message = "git worktree prune exit code "
        $message = $message + $pruneExitCode
        throw $message
      }
    }
}

function Read-PopulationCache {
  $result = @()

  if (-not (Test-Path $CachePath)) {
    return $result
  }

  Invoke-WithRetry `
    -Description "population cache read" `
    -Action {
      $script:cacheReadLines = Get-Content -Path $CachePath -Encoding UTF8
    }

  foreach ($line in $script:cacheReadLines) {
    $result += $line
  }

  return $result
}

function Write-PopulationCache {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Sha,

    [Parameter(Mandatory=$true)]
    [string]$Result
  )

  $line = "$Sha`t$Result"
  $tempPath = $CachePath + ".tmp." + $PID

  try {
    Invoke-WithRetry `
      -Description "population cache update" `
      -Action {
        $existing = @()

        if (Test-Path $CachePath) {
          $existing = Get-Content -Path $CachePath -Encoding UTF8
        }

        $filtered = @()

        foreach ($existingLine in $existing) {
          if (-not $existingLine.StartsWith("$Sha`t")) {
            $filtered += $existingLine
          }
        }

        $newContent = @()

        foreach ($filteredLine in $filtered) {
          $newContent += $filteredLine
        }

        $newContent += $line

        Set-Content `
          -Path $tempPath `
          -Value $newContent `
          -Encoding UTF8

        Move-Item `
          -Path $tempPath `
          -Destination $CachePath `
          -Force
      }
  }
  finally {
    if (Test-Path $tempPath) {
      Remove-Item `
        -Path $tempPath `
        -Force `
        -ErrorAction SilentlyContinue
    }
  }
}

$cache = @{}
$cacheLines = Read-PopulationCache

foreach ($line in $cacheLines) {
  $parts = $line -split "`t", 3

  if ($parts.Count -ge 2) {
    $cache[$parts[0]] = $parts[1]
  }
}

function Get-CandidateCommits {
  $gitArguments = @(
    "log",
    "--format=%H`t%s",
    "--reverse",
    "--all",
    "--"
  )

  foreach ($pathspec in $Pathspecs) {
    $gitArguments += $pathspec
  }

  $lines = & git @gitArguments
  $exitCode = $LASTEXITCODE

  if ($exitCode -ne 0) {
    throw "git log failed with exit code $exitCode"
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

    $row = New-Object PSObject
    Add-Member -InputObject $row -MemberType NoteProperty -Name Sha -Value $sha
    Add-Member -InputObject $row -MemberType NoteProperty -Name Subject -Value $parts[1]
    $rows += $row
  }

  return $rows
}

function Measure-Commit {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Sha
  )

  if ($cache.ContainsKey($Sha)) {
    $cachedRow = New-Object PSObject
    Add-Member -InputObject $cachedRow -MemberType NoteProperty -Name Status -Value "cached"
    Add-Member -InputObject $cachedRow -MemberType NoteProperty -Name Result -Value $cache[$Sha]
    return $cachedRow
  }

  $hasFoundation = Test-FoundationAtCommit -Sha $Sha

  if (-not $hasFoundation) {
    $result = "UNAVAILABLE:foundation"

    Write-PopulationCache `
      -Sha $Sha `
      -Result $result

    $cache[$Sha] = $result

    $missingRow = New-Object PSObject
    Add-Member -InputObject $missingRow -MemberType NoteProperty -Name Status -Value "measured"
    Add-Member -InputObject $missingRow -MemberType NoteProperty -Name Result -Value $result
    return $missingRow
  }

  Remove-TemporaryWorktree

  $oldPrompt = $env:GIT_TERMINAL_PROMPT
  $env:GIT_TERMINAL_PROMPT = "0"

  try {
    Invoke-WithRetry `
      -Description "temporary worktree creation for $Sha" `
      -Action {
        $oldErrorActionPreference = $ErrorActionPreference
        $addExitCode = $null

        try {
          $ErrorActionPreference = "Continue"
          & git worktree add --detach $Worktree $Sha 1>$null 2>$null
          $addExitCode = $LASTEXITCODE
        }
        finally {
          $ErrorActionPreference = $oldErrorActionPreference
        }

        if ($addExitCode -ne 0) {
          $message = "git worktree add exit code "
          $message = $message + $addExitCode
          throw $message
        }
      }
  }
  finally {
    if ($null -eq $oldPrompt) {
      Remove-Item Env:GIT_TERMINAL_PROMPT -ErrorAction SilentlyContinue
    }
    else {
      $env:GIT_TERMINAL_PROMPT = $oldPrompt
    }
  }

  try {
    $collector = Join-Path $Worktree "_r25_11_r6_r1_collector.py"
    Copy-Item $CollectorSource $collector -Force

    Push-Location $Worktree

    try {
      $env:PYTHONPATH = $Worktree
      $env:PYTHONUTF8 = "1"

      $collectorOldErrorActionPreference = $ErrorActionPreference

      try {
        $ErrorActionPreference = "Continue"
        $collectorOutput = & python ".\_r25_11_r6_r1_collector.py" 2>&1
        $collectorExitCode = $LASTEXITCODE
      }
      finally {
        $ErrorActionPreference = $collectorOldErrorActionPreference
      }
    }
    finally {
      Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
      Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
      Pop-Location
    }

    if ($collectorExitCode -ne 0) {
      $lastOutputLine = $collectorOutput | Select-Object -Last 1
      $result = "UNAVAILABLE:" + $lastOutputLine
    }
    else {
      $totalLines = $collectorOutput | Where-Object { $_ -like "TOTAL=*" }
      $result = $totalLines | Select-Object -Last 1

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

  $measuredRow = New-Object PSObject
  Add-Member -InputObject $measuredRow -MemberType NoteProperty -Name Status -Value "measured"
  Add-Member -InputObject $measuredRow -MemberType NoteProperty -Name Result -Value $result
  return $measuredRow
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
  $measurement = Measure-Commit -Sha $candidate.Sha
  $total = Parse-Total -Result $measurement.Result

  if ($null -eq $total) {
    $shortSha = $candidate.Sha.Substring(0, 10)
    Write-Host "$shortSha status=$($measurement.Status) $($measurement.Result) subject=$($candidate.Subject)"
    continue
  }

  $row = New-Object PSObject
  Add-Member -InputObject $row -MemberType NoteProperty -Name Sha -Value $candidate.Sha
  Add-Member -InputObject $row -MemberType NoteProperty -Name Subject -Value $candidate.Subject
  Add-Member -InputObject $row -MemberType NoteProperty -Name Total -Value $total
  Add-Member -InputObject $row -MemberType NoteProperty -Name Result -Value $measurement.Result
  Add-Member -InputObject $row -MemberType NoteProperty -Name Status -Value $measurement.Status
  $measurable += $row

  $marker = ""

  if ($total -eq $Expected) {
    $marker = " <== EXACT_190"
    $exact += $row
  }

  $shortSha = $candidate.Sha.Substring(0, 10)
  Write-Host "$shortSha selected=$total status=$($measurement.Status)$marker subject=$($candidate.Subject)"
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
$i = 0

while ($i -lt $measurable.Count) {
  if ($measurable[$i].Sha -eq $firstExact.Sha) {
    $index = $i
    break
  }

  $i = $i + 1
}

Write-Host ""
Write-Host "First exact-190 measurable neighbors:"

if ($index -gt 0) {
  $previous = $measurable[$index - 1]
  Write-Host "PREVIOUS_SHA=$($previous.Sha) selected=$($previous.Total) subject=$($previous.Subject)"
}

Write-Host "CURRENT_SHA=$($firstExact.Sha) selected=$($firstExact.Total) subject=$($firstExact.Subject)"

$nextIndex = $index + 1

if (($index -ge 0) -and ($nextIndex -lt $measurable.Count)) {
  $next = $measurable[$nextIndex]
  Write-Host "NEXT_SHA=$($next.Sha) selected=$($next.Total) subject=$($next.Subject)"
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









