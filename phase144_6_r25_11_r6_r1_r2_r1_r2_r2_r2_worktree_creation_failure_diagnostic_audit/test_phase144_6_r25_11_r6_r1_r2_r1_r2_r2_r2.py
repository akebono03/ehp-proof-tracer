from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT = HERE / "audit_worktree_creation_failure.ps1"


def _source():
  return AUDIT.read_text(
    encoding="utf-8-sig"
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_targets_exact_failed_commit():
  source = _source()

  assert (
    '$TargetSha = "a2d9a4922bb728494d01ece912595aca93b835a6"'
    in source
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_inspects_registered_worktrees_and_metadata():
  source = _source()

  assert "git worktree list --porcelain" in source
  assert '$worktreesMetadataDir = Join-Path $resolvedGitDir "worktrees"' in source
  assert '$gitdirFile = Join-Path $entry.FullName "gitdir"' in source
  assert '$lockedFile = Join-Path $entry.FullName "locked"' in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_makes_only_one_controlled_add_attempt():
  source = _source()

  assert source.count(
    "git worktree add --detach $DiagnosticWorktree $TargetSha"
  ) == 1
  assert "WORKTREE_ADD_EXIT=" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_avoids_destructive_metadata_cleanup():
  source = _source()
  executable_lines = tuple(
    line.strip()
    for line in source.splitlines()
    if line.strip()
    and not line.lstrip().startswith("#")
    and not line.lstrip().startswith("Write-Host")
  )

  assert not any(
    line.startswith("& git worktree prune")
    or line.startswith("git worktree prune")
    for line in executable_lines
  )
  assert not any(
    line.startswith("Remove-Item")
    and "$worktreesMetadataDir" in line
    for line in executable_lines
  )
  assert "No git worktree prune was run." in source
  assert "No worktree metadata was manually deleted." in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_cleans_up_only_after_successful_add():
  source = _source()

  assert "if ($addExitCode -eq 0)" in source
  assert "git worktree remove --force $DiagnosticWorktree" in source
  assert (
    "No cleanup mutation performed because diagnostic add did not succeed."
    in source
  )
