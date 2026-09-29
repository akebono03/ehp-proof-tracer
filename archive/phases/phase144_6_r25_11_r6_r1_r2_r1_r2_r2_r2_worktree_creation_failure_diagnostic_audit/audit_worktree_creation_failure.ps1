param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

$TargetSha = "a2d9a4922bb728494d01ece912595aca93b835a6"
$ShortSha = $TargetSha.Substring(0, 10)
$DiagnosticRoot = Join-Path $env:TEMP "ehp_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2"
$DiagnosticWorktree = Join-Path $DiagnosticRoot ("worktree_" + $ShortSha)
$StdoutPath = Join-Path $DiagnosticRoot "worktree_add.stdout.txt"
$StderrPath = Join-Path $DiagnosticRoot "worktree_add.stderr.txt"

function Write-Section {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Title
  )

  Write-Host ""
  Write-Host "=============================================================================="
  Write-Host $Title
  Write-Host "=============================================================================="
}

function Invoke-NativeCapture {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Description,

    [Parameter(Mandatory=$true)]
    [scriptblock]$Command,

    [Parameter(Mandatory=$true)]
    [string]$StdoutFile,

    [Parameter(Mandatory=$true)]
    [string]$StderrFile
  )

  $oldErrorActionPreference = $ErrorActionPreference

  try {
    $ErrorActionPreference = "Continue"
    & $Command 1>$StdoutFile 2>$StderrFile
    $exitCode = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldErrorActionPreference
  }

  Write-Host ($Description + " exit_code=" + $exitCode)

  if (Test-Path $StdoutFile) {
    Write-Host "--- stdout ---"
    Get-Content -Path $StdoutFile -Encoding UTF8
  }

  if (Test-Path $StderrFile) {
    Write-Host "--- stderr ---"
    Get-Content -Path $StderrFile -Encoding UTF8
  }

  return $exitCode
}

Write-Section "A. Diagnostic boundary"
Write-Host ("repo_root=" + $RepoRoot)
Write-Host ("target_sha=" + $TargetSha)
Write-Host ("diagnostic_root=" + $DiagnosticRoot)
Write-Host ("diagnostic_worktree=" + $DiagnosticWorktree)
Write-Host "mutation_policy=no prune, no metadata deletion, no locator/cache changes"

if (-not (Test-Path $DiagnosticRoot)) {
  New-Item -ItemType Directory -Path $DiagnosticRoot | Out-Null
}

Write-Section "B. Repository identity and target commit"

Push-Location $RepoRoot

try {
  $repoTop = & git rev-parse --show-toplevel
  $repoTopExit = $LASTEXITCODE
  Write-Host ("rev_parse_toplevel_exit=" + $repoTopExit)
  Write-Host ("repo_top=" + $repoTop)

  $gitDir = & git rev-parse --git-dir
  $gitDirExit = $LASTEXITCODE
  Write-Host ("rev_parse_git_dir_exit=" + $gitDirExit)
  Write-Host ("git_dir=" + $gitDir)

  $insideWorktree = & git rev-parse --is-inside-work-tree
  Write-Host ("inside_work_tree=" + $insideWorktree)

  $oldErrorActionPreference = $ErrorActionPreference

  try {
    $ErrorActionPreference = "Continue"
    & git cat-file -e ($TargetSha + "^{commit}") 2>$null
    $targetCommitExit = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldErrorActionPreference
  }

  Write-Host ("target_commit_exists_exit=" + $targetCommitExit)

  $subject = & git show -s --format=%s $TargetSha
  $subjectExit = $LASTEXITCODE
  Write-Host ("target_subject_exit=" + $subjectExit)
  Write-Host ("target_subject=" + $subject)

  Write-Section "C. Current registered worktrees"
  & git worktree list --porcelain
  $worktreeListExit = $LASTEXITCODE
  Write-Host ("worktree_list_exit=" + $worktreeListExit)

  Write-Section "D. Diagnostic path pre-state"
  Write-Host ("diagnostic_root_exists=" + (Test-Path $DiagnosticRoot))
  Write-Host ("diagnostic_worktree_exists=" + (Test-Path $DiagnosticWorktree))

  if (Test-Path $DiagnosticWorktree) {
    Write-Host "diagnostic_worktree_preexisting_entries:"
    Get-ChildItem -Force -Path $DiagnosticWorktree | Select-Object FullName, Mode, Length
  }

  Write-Section "E. Git worktree metadata directory"
  $resolvedGitDir = $gitDir

  if (-not [System.IO.Path]::IsPathRooted($resolvedGitDir)) {
    $resolvedGitDir = Join-Path $RepoRoot $resolvedGitDir
  }

  $worktreesMetadataDir = Join-Path $resolvedGitDir "worktrees"
  Write-Host ("worktrees_metadata_dir=" + $worktreesMetadataDir)
  Write-Host ("worktrees_metadata_exists=" + (Test-Path $worktreesMetadataDir))

  if (Test-Path $worktreesMetadataDir) {
    Get-ChildItem -Force -Path $worktreesMetadataDir | Select-Object Name, FullName, Mode

    foreach ($entry in Get-ChildItem -Force -Path $worktreesMetadataDir) {
      $gitdirFile = Join-Path $entry.FullName "gitdir"
      $lockedFile = Join-Path $entry.FullName "locked"

      if (Test-Path $gitdirFile) {
        Write-Host ("metadata_gitdir[" + $entry.Name + "]=")
        Get-Content -Path $gitdirFile -Encoding UTF8
      }

      if (Test-Path $lockedFile) {
        Write-Host ("metadata_locked[" + $entry.Name + "]=")
        Get-Content -Path $lockedFile -Encoding UTF8
      }
    }
  }

  Write-Section "F. Single controlled worktree-add attempt"

  if (Test-Path $DiagnosticWorktree) {
    Write-Host "SKIP_ADD: diagnostic path already exists; no destructive cleanup performed."
    $addExitCode = 9001
  }
  else {
    $addExitCode = Invoke-NativeCapture `
      -Description "git worktree add --detach" `
      -Command {
        git worktree add --detach $DiagnosticWorktree $TargetSha
      } `
      -StdoutFile $StdoutPath `
      -StderrFile $StderrPath
  }

  Write-Section "G. Post-attempt state"
  Write-Host ("worktree_add_exit=" + $addExitCode)
  Write-Host ("diagnostic_worktree_exists_after=" + (Test-Path $DiagnosticWorktree))
  & git worktree list --porcelain
  $postListExit = $LASTEXITCODE
  Write-Host ("post_worktree_list_exit=" + $postListExit)

  Write-Section "H. Conservative cleanup"

  if ($addExitCode -eq 0) {
    $cleanupStdout = Join-Path $DiagnosticRoot "worktree_remove.stdout.txt"
    $cleanupStderr = Join-Path $DiagnosticRoot "worktree_remove.stderr.txt"

    $removeExitCode = Invoke-NativeCapture `
      -Description "git worktree remove --force" `
      -Command {
        git worktree remove --force $DiagnosticWorktree
      } `
      -StdoutFile $cleanupStdout `
      -StderrFile $cleanupStderr

    Write-Host ("worktree_remove_exit=" + $removeExitCode)
  }
  else {
    Write-Host "No cleanup mutation performed because diagnostic add did not succeed."
  }

  Write-Section "I. Diagnostic summary"
  Write-Host ("TARGET_SHA=" + $TargetSha)
  Write-Host ("TARGET_COMMIT_EXIT=" + $targetCommitExit)
  Write-Host ("WORKTREE_ADD_EXIT=" + $addExitCode)
  Write-Host ("DIAGNOSTIC_WORKTREE=" + $DiagnosticWorktree)
  Write-Host ("DIAGNOSTIC_ROOT=" + $DiagnosticRoot)

  if ($addExitCode -eq 0) {
    Write-Host "DIAGNOSIS=CONTROLLED_ADD_SUCCEEDED"
  }
  elseif ($addExitCode -eq 9001) {
    Write-Host "DIAGNOSIS=DIAGNOSTIC_PATH_PREEXISTED"
  }
  else {
    Write-Host "DIAGNOSIS=CONTROLLED_ADD_FAILED"
  }

  Write-Host "No git worktree prune was run."
  Write-Host "No worktree metadata was manually deleted."
  Write-Host "No historical locator or population cache was changed."
}
finally {
  Pop-Location
}
