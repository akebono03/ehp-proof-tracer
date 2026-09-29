from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent
LOCATOR = PHASE_DIR / "locate_historical_190.ps1"


def _remove_source():
  source = LOCATOR.read_text(encoding="utf-8-sig")
  start = source.index("function Remove-TemporaryWorktree {")
  end = source.index("function Read-PopulationCache {")
  return source[start:end]


def test_phase144_6_r4_r3_r1_preserves_stale_path_branch():
  source = _remove_source()

  assert "& git worktree list --porcelain 2>$null" in source
  assert "if ($isRegistered)" in source
  assert '$expectedLeaf = ".phase144_6_r25_11_r6_r1_worktree"' in source
  assert '-Description "stale unregistered audit worktree path cleanup"' in source


def test_phase144_6_r4_r3_r1_restores_scalar_prune_contract():
  source = _remove_source()

  assert '-Description "git worktree prune"' in source
  assert "& git worktree prune --expire now 1>$null 2>$null" in source
  assert "$pruneExitCode = $LASTEXITCODE" in source
  assert "if ($pruneExitCode -ne 0)" in source


def test_phase144_6_r4_r3_r1_preserves_prior_repairs():
  source = LOCATOR.read_text(encoding="utf-8-sig")

  assert source.count("function Read-PopulationCache {") == 1
  assert source.count("function Measure-Commit {") == 1
  assert "$addExitCode = $LASTEXITCODE" in source
  assert "$Expected = 190" in source
