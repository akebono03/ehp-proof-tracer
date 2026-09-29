from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent
LOCATOR = PHASE_DIR / "locate_historical_190.ps1"


def _measure_source():
  source = LOCATOR.read_text(encoding="utf-8-sig")
  start = source.index("function Measure-Commit {")
  end = source.index("function Parse-Total {")
  return source[start:end]


def test_phase144_6_r4_r4_collector_temporarily_allows_native_stderr():
  source = _measure_source()

  assert "$collectorOldErrorActionPreference = $ErrorActionPreference" in source
  assert '$ErrorActionPreference = "Continue"' in source
  assert '$collectorOutput = & python ".\\_r25_11_r6_r1_collector.py" 2>&1' in source
  assert "$collectorExitCode = $LASTEXITCODE" in source
  assert "$ErrorActionPreference = $collectorOldErrorActionPreference" in source


def test_phase144_6_r4_r4_collector_preserves_failure_output_conversion():
  source = _measure_source()

  assert "if ($collectorExitCode -ne 0)" in source
  assert "$lastOutputLine = $collectorOutput | Select-Object -Last 1" in source
  assert '$result = "UNAVAILABLE:" + $lastOutputLine' in source


def test_phase144_6_r4_r4_preserves_prior_harness_repairs():
  source = LOCATOR.read_text(encoding="utf-8-sig")

  assert "& git worktree prune --expire now 1>$null 2>$null" in source
  assert "$pruneExitCode = $LASTEXITCODE" in source
  assert source.count("function Read-PopulationCache {") == 1
  assert "$addExitCode = $LASTEXITCODE" in source
  assert "$Expected = 190" in source
