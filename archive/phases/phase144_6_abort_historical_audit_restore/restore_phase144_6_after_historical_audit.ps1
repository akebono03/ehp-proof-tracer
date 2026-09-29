$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir

Write-Host "=============================================================="
Write-Host "Phase 144-6 Historical Audit Abort / Restore"
Write-Host "Production files are not modified."
Write-Host "No git reset / git clean is used."
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Removing audit worktree registration if present..."

  $auditWorktree = Join-Path $RepoRoot ".phase144_6_r25_11_r6_r1_worktree"
  $normalizedAuditWorktree = [System.IO.Path]::GetFullPath($auditWorktree)
  $registered = $false

  $oldErrorActionPreference = $ErrorActionPreference
  try {
    $ErrorActionPreference = "Continue"
    $worktreeLines = & git worktree list --porcelain 2>$null
    $listExitCode = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldErrorActionPreference
  }

  if ($listExitCode -ne 0) {
    throw "git worktree list failed with exit code $listExitCode"
  }

  foreach ($line in $worktreeLines) {
    if ($line -like "worktree *") {
      $registeredPath = $line.Substring(9)
      $normalizedRegistered = [System.IO.Path]::GetFullPath($registeredPath)

      if ($normalizedRegistered -eq $normalizedAuditWorktree) {
        $registered = $true
      }
    }
  }

  if ($registered) {
    $oldErrorActionPreference = $ErrorActionPreference
    try {
      $ErrorActionPreference = "Continue"
      & git worktree remove --force $auditWorktree 1>$null 2>$null
      $removeExitCode = $LASTEXITCODE
    }
    finally {
      $ErrorActionPreference = $oldErrorActionPreference
    }

    if ($removeExitCode -ne 0) {
      Write-Host "Git worktree remove returned $removeExitCode; continuing with guarded local cleanup."
    }
  }

  if (Test-Path $auditWorktree) {
    $leaf = Split-Path -Leaf $auditWorktree
    if ($leaf -ne ".phase144_6_r25_11_r6_r1_worktree") {
      throw "Audit worktree guard failed."
    }
    Remove-Item -LiteralPath $auditWorktree -Recurse -Force
  }

  & git worktree prune --expire now
  if ($LASTEXITCODE -ne 0) {
    throw "git worktree prune failed."
  }

  Write-Host "Audit worktree cleanup: PASS"

  Write-Host ""
  Write-Host "B. Removing historical-localization audit directory..."

  $historicalAudit = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
  if (Test-Path $historicalAudit) {
    Remove-Item -LiteralPath $historicalAudit -Recurse -Force
  }

  Write-Host "Historical localization audit removed."

  Write-Host ""
  Write-Host "C. Removing this repair package directory after completion is optional."
  Write-Host "It contains no production code."

  Write-Host ""
  Write-Host "D. Current git status:"
  git status --short

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Restore complete."
  Write-Host "Production code was not reverted because the historical audit"
  Write-Host "never modified production code."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Pop-Location
}
