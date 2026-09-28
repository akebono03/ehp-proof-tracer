from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent


def _locator_source():
  return (
    PHASE_DIR
    / "locate_historical_190.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_measure_commit_is_single_complete_function():
  source = _locator_source()

  assert source.count("function Measure-Commit {") == 1
  assert source.count("function Parse-Total {") == 1

  measure_start = source.index("function Measure-Commit {")
  parse_start = source.index("function Parse-Total {")
  measure_source = source[measure_start:parse_start]

  assert "return $measuredRow" in measure_source
  assert measure_source.rstrip().endswith("}")


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_measure_commit_uses_scalar_add_exit_code():
  source = _locator_source()
  measure_start = source.index("function Measure-Commit {")
  parse_start = source.index("function Parse-Total {")
  measure_source = source[measure_start:parse_start]

  assert (
    "& git worktree add --detach $Worktree $Sha "
    "1>$null 2>$null"
    in measure_source
  )
  assert "$addExitCode = $LASTEXITCODE" in measure_source
  assert "if ($addExitCode -ne 0)" in measure_source
  assert (
    '$ErrorActionPreference = "Continue"'
    in measure_source
  )
  assert (
    "$ErrorActionPreference = $oldErrorActionPreference"
    in measure_source
  )


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_preserves_measure_commit_collector_flow():
  source = _locator_source()
  measure_start = source.index("function Measure-Commit {")
  parse_start = source.index("function Parse-Total {")
  measure_source = source[measure_start:parse_start]

  assert "Test-FoundationAtCommit -Sha $Sha" in measure_source
  assert 'UNAVAILABLE:foundation' in measure_source
  assert 'Join-Path $Worktree "_r25_11_r6_r1_collector.py"' in measure_source
  assert '$collectorOutput = & python ".\\_r25_11_r6_r1_collector.py" 2>&1' in measure_source
  assert '$totalLines = $collectorOutput | Where-Object { $_ -like "TOTAL=*" }' in measure_source
  assert "Remove-TemporaryWorktree" in measure_source
  assert "Write-PopulationCache" in measure_source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_preserves_historical_target():
  source = _locator_source()

  assert "$Expected = 190" in source
  assert "EXACT_190_SHA=" in source
