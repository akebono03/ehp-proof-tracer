from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent


def _locator_source():
  return (
    PHASE_DIR
    / "locate_historical_190.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_add_uses_scalar_last_exit_code():
  source = _locator_source()

  assert (
    "& git worktree add --detach $Worktree $Sha "
    "1>$null 2>$null"
    in source
  )
  assert "$addExitCode = $LASTEXITCODE" in source
  assert "if ($addExitCode -ne 0)" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_remove_uses_scalar_last_exit_code():
  source = _locator_source()

  assert (
    "& git worktree remove --force $Worktree "
    "1>$null 2>$null"
    in source
  )
  assert "$removeExitCode = $LASTEXITCODE" in source
  assert "if ($removeExitCode -ne 0)" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_prune_uses_scalar_last_exit_code():
  source = _locator_source()

  assert (
    "& git worktree prune --expire now "
    "1>$null 2>$null"
    in source
  )
  assert "$pruneExitCode = $LASTEXITCODE" in source
  assert "if ($pruneExitCode -ne 0)" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_native_calls_temporarily_relax_error_action():
  source = _locator_source()

  assert source.count(
    '$ErrorActionPreference = "Continue"'
  ) >= 5
  assert source.count(
    "$ErrorActionPreference = $oldErrorActionPreference"
  ) >= 5


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_preserves_historical_boundary():
  source = _locator_source()

  assert "$Expected = 190" in source
  assert "UNAVAILABLE:foundation" in source
  assert "EXACT_190_SHA=" in source
