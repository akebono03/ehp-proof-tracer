from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent


def _locator_source():
  return (
    PHASE_DIR
    / "locate_historical_190.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_uses_simple_stderr_path_construction():
  source = _locator_source()

  assert (
    '$commitStderrName = "ehp_r25_11_r6_r1_commit_" '
    '+ $PID + ".stderr.txt"'
    in source
  )
  assert (
    "$commitStderrPath = Join-Path $env:TEMP "
    "$commitStderrName"
    in source
  )
  assert (
    '$foundationStderrName = '
    '"ehp_r25_11_r6_r1_foundation_" '
    '+ $PID + ".stderr.txt"'
    in source
  )
  assert (
    "$foundationStderrPath = Join-Path $env:TEMP "
    "$foundationStderrName"
    in source
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_uses_simple_error_message_construction():
  source = _locator_source()

  assert (
    '$message = "git commit-object check failed for " + $Sha'
    in source
  )
  assert (
    '$message = $message + " with exit code " '
    "+ $commitExitCode"
    in source
  )
  assert (
    '$message = $message + ": " + $commitStderrText'
    in source
  )
  assert "throw $message" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_preserves_native_git_exit_semantics():
  source = _locator_source()

  assert '$ErrorActionPreference = "Continue"' in source
  assert (
    "git cat-file -e $commitObjectName 2>$commitStderrPath"
    in source
  )
  assert "$commitExitCode = $LASTEXITCODE" in source
  assert "if ($commitExitCode -ne 0)" in source
  assert (
    "git cat-file -e $foundationObjectName "
    "2>$foundationStderrPath"
    in source
  )
  assert "$foundationExitCode = $LASTEXITCODE" in source
  assert "if ($foundationExitCode -eq 0)" in source
  assert "return $true" in source
  assert "return $false" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_preserves_localization_boundary():
  source = _locator_source()

  assert "$Expected = 190" in source
  assert "UNAVAILABLE:foundation" in source
  assert "EXACT_190_SHA=" in source
