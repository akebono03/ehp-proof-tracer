from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent
LOCATOR = PHASE_DIR / "locate_historical_190.ps1"


def _remove_source():
  source = LOCATOR.read_text(encoding="utf-8-sig")
  start = source.index("function Remove-TemporaryWorktree {")
  end = source.index("function Read-PopulationCache {")
  return source[start:end]


def test_phase144_6_r25_11_r6_r1_r4_r3_remove_temporary_worktree_checks_registration():
  source = _remove_source()

  assert "& git worktree list --porcelain 2>$null" in source
  assert "$listExitCode = $LASTEXITCODE" in source
  assert '$isRegistered = $false' in source
  assert '$registeredLine -like "worktree *"' in source


def test_phase144_6_r25_11_r6_r1_r4_r3_registered_worktree_uses_git_remove():
  source = _remove_source()

  assert "if ($isRegistered)" in source
  assert "& git worktree remove --force $Worktree 1>$null 2>$null" in source
  assert "$removeExitCode = $LASTEXITCODE" in source


def test_phase144_6_r25_11_r6_r1_r4_r3_unregistered_cleanup_is_audit_path_guarded():
  source = _remove_source()

  assert '$expectedLeaf = ".phase144_6_r25_11_r6_r1_worktree"' in source
  assert "if ($actualLeaf -ne $expectedLeaf)" in source
  assert "refusing unregistered path cleanup outside audit worktree" in source
  assert '-Description "stale unregistered audit worktree path cleanup"' in source
  assert "-LiteralPath $normalizedTarget" in source


def test_phase144_6_r25_11_r6_r1_r4_r3_preserves_restored_helper_and_measure_repair():
  source = LOCATOR.read_text(encoding="utf-8-sig")

  assert source.count("function Read-PopulationCache {") == 1
  assert source.count("function Measure-Commit {") == 1
  assert "$addExitCode = $LASTEXITCODE" in source
  assert "$Expected = 190" in source
