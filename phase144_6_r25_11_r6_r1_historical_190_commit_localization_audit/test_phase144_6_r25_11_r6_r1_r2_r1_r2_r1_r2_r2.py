from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent


def _locator_source():
  return (
    PHASE_DIR
    / "locate_historical_190.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_checks_commit_before_foundation_path():
  source = _locator_source()

  commit_check = '& git cat-file -e $commitObjectName 2>$commitStderrPath'
  foundation_check = '& git cat-file -e $foundationObjectName 2>$foundationStderrPath'

  assert '$commitObjectName = $Sha + "^{commit}"' in source
  assert commit_check in source
  assert foundation_check in source
  assert source.index(commit_check) < source.index(foundation_check)


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_commit_failure_is_real_error():
  source = _locator_source()

  assert "if ($commitExitCode -ne 0)" in source
  assert '$message = "git commit-object check failed for " + $Sha' in source
  assert "throw $message" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_foundation_failure_means_unavailable():
  source = _locator_source()

  assert "if ($foundationExitCode -eq 0)" in source
  assert "return $true" in source

  function_start = source.index("function Test-FoundationAtCommit {")
  function_end = source.index("function Remove-TemporaryWorktree {")
  function_source = source[function_start:function_end]

  assert function_source.rstrip().endswith("return $false\n}")


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_preserves_error_action_restoration():
  source = _locator_source()

  assert "$oldErrorActionPreference = $ErrorActionPreference" in source
  assert source.count('$ErrorActionPreference = "Continue"') >= 2
  assert source.count(
    "$ErrorActionPreference = $oldErrorActionPreference"
  ) >= 2


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_preserves_localization_boundary():
  source = _locator_source()

  assert "$Expected = 190" in source
  assert "UNAVAILABLE:foundation" in source
  assert "EXACT_190_SHA=" in source
