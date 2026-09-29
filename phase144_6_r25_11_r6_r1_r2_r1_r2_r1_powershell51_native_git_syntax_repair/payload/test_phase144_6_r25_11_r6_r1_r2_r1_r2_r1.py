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

  assert '$stderrName = "ehp_r25_11_r6_r1_cat_file_" + $PID + ".stderr.txt"' in source
  assert "$stderrPath = Join-Path $env:TEMP $stderrName" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_uses_simple_error_message_construction():
  source = _locator_source()

  assert '$message = "git cat-file failed for " + $Sha' in source
  assert '$message = $message + " with exit code " + $exitCode' in source
  assert '$message = $message + ": " + $stderrText' in source
  assert "throw $message" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_preserves_native_git_exit_semantics():
  source = _locator_source()

  assert '$ErrorActionPreference = "Continue"' in source
  assert "git cat-file -e $objectName 2>$stderrPath" in source
  assert "$exitCode = $LASTEXITCODE" in source
  assert "if ($exitCode -eq 0)" in source
  assert "if ($exitCode -eq 1)" in source
  assert "return $true" in source
  assert "return $false" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_preserves_localization_boundary():
  source = _locator_source()

  assert "$Expected = 190" in source
  assert "UNAVAILABLE:foundation" in source
  assert "EXACT_190_SHA=" in source
