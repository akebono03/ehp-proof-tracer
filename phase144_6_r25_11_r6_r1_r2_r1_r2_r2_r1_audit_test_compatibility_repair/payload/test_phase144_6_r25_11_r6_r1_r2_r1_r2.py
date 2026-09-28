from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent


def _locator_source():
  return (
    PHASE_DIR
    / "locate_historical_190.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_cat_file_temporarily_relaxes_error_action():
  source = _locator_source()

  assert "function Test-FoundationAtCommit" in source
  assert '$oldErrorActionPreference = $ErrorActionPreference' in source
  assert source.count('$ErrorActionPreference = "Continue"') >= 2
  assert source.count(
    "$ErrorActionPreference = $oldErrorActionPreference"
  ) >= 2


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_cat_file_captures_native_stderr():
  source = _locator_source()

  assert (
    "git cat-file -e $commitObjectName 2>$commitStderrPath"
    in source
  )
  assert "$commitExitCode = $LASTEXITCODE" in source
  assert (
    "git cat-file -e $foundationObjectName 2>$foundationStderrPath"
    in source
  )
  assert "$foundationExitCode = $LASTEXITCODE" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_cat_file_distinguishes_absence_from_error():
  source = _locator_source()

  assert "if ($commitExitCode -ne 0)" in source
  assert "git commit-object check failed for " in source
  assert "throw $message" in source
  assert "if ($foundationExitCode -eq 0)" in source
  assert "return $true" in source

  function_start = source.index(
    "function Test-FoundationAtCommit {"
  )
  function_end = source.index(
    "function Remove-TemporaryWorktree {"
  )
  function_source = source[
    function_start:function_end
  ]

  assert function_source.rstrip().endswith(
    "return $false\n}"
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_keeps_historical_target_and_prefilter():
  source = _locator_source()

  assert "$Expected = 190" in source
  assert "UNAVAILABLE:foundation" in source
  assert "EXACT_190_SHA=" in source
