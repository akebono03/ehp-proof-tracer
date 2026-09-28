param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

$ExpectedSha = "a2d9a4922bb728494d01ece912595aca93b835a6"
$HistoricalWorktree = Join-Path $RepoRoot ".phase144_6_r25_11_r6_r1_worktree"
$DiagnosticRoot = Join-Path $env:TEMP "ehp_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2"
$DiagnosticWorktree = Join-Path $DiagnosticRoot "worktree_a2d9a4922b"
$Targets = @(
  $HistoricalWorktree,
  $DiagnosticWorktree
)

function Remove-VerifiedWorktree {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Path
  )

  if (-not (Test-Path $Path)) {
    Write-Host ("cleanup skip missing: " + $Path)
    return
  }

  $oldErrorActionPreference = $ErrorActionPreference
  $head = $null
  $headExitCode = $null

  try {
    $ErrorActionPreference = "Continue"
    $head = & git -C $Path rev-parse HEAD 2>$null
    $headExitCode = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldErrorActionPreference
  }

  if ($headExitCode -ne 0) {
    $message = "cannot verify worktree HEAD: " + $Path
    throw $message
  }

  $headText = [string]$head
  $headText = $headText.Trim()

  if ($headText -ne $ExpectedSha) {
    $message = "refusing cleanup because HEAD differs: "
    $message = $message + $Path
    $message = $message + " HEAD="
    $message = $message + $headText
    throw $message
  }

  $removeExitCode = $null

  try {
    $ErrorActionPreference = "Continue"
    & git worktree remove --force $Path 1>$null 2>$null
    $removeExitCode = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldErrorActionPreference
  }

  if ($removeExitCode -ne 0) {
    $message = "verified worktree removal failed: "
    $message = $message + $Path
    $message = $message + " exit="
    $message = $message + $removeExitCode
    throw $message
  }

  Write-Host ("cleanup removed verified worktree: " + $Path)
}

Push-Location $RepoRoot

try {
  foreach ($target in $Targets) {
    Remove-VerifiedWorktree -Path $target
  }
}
finally {
  Pop-Location
}
