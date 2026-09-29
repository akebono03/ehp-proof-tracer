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
  assert '$ErrorActionPreference = "Continue"' in source
  assert '$ErrorActionPreference = $oldErrorActionPreference' in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_cat_file_captures_native_stderr():
  source = _locator_source()

  assert "git cat-file -e $objectName 2>$stderrPath" in source
  assert "$exitCode = $LASTEXITCODE" in source
  assert "Get-Content -Path $stderrPath -Encoding UTF8" in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_cat_file_distinguishes_absence_from_error():
  source = _locator_source()

  assert "if ($exitCode -eq 0)" in source
  assert "if ($exitCode -eq 1)" in source
  assert "return $true" in source
  assert "return $false" in source
  assert "git cat-file failed for " in source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_keeps_historical_target_and_prefilter():
  source = _locator_source()

  assert "$Expected = 190" in source
  assert "UNAVAILABLE:foundation" in source
  assert "EXACT_190_SHA=" in source
