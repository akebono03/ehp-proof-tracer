from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent


def _locator_source():
  return (
    PHASE_DIR
    / "locate_historical_190.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )


def test_phase144_6_r25_11_r6_r1_r2_keeps_expected_190():
  source = _locator_source()

  assert "$Expected = 190" in source
  assert "EXACT_190_SHA=" in source


def test_phase144_6_r25_11_r6_r1_r2_prefilters_missing_foundation_without_worktree():
  source = _locator_source()

  assert "function Test-FoundationAtCommit" in source
  assert "git cat-file" in source
  assert "UNAVAILABLE:foundation" in source


def test_phase144_6_r25_11_r6_r1_r2_has_worktree_retry_and_noninteractive_git():
  source = _locator_source()

  assert "function Invoke-WithRetry" in source
  assert "function Remove-TemporaryWorktree" in source
  assert '$env:GIT_TERMINAL_PROMPT = "0"' in source
  assert "git worktree remove" in source
  assert "git worktree prune" in source


def test_phase144_6_r25_11_r6_r1_r2_has_cache_retry_and_atomic_replace():
  source = _locator_source()

  assert "function Write-PopulationCache" in source
  assert "population cache update" in source
  assert "Set-Content" in source
  assert "Move-Item" in source


def test_phase144_6_r25_11_r6_r1_r2_does_not_change_target_collector():
  collector = (
    PHASE_DIR
    / "collect_selected_total.py"
  ).read_text(
    encoding="utf-8"
  )

  assert "(3, 3)" in collector
  assert "(5, 3)" in collector
  assert "(4, 6)" in collector
  assert "(5, 7)" in collector
  assert "(8, 7)" in collector
  assert "(9, 7)" in collector
