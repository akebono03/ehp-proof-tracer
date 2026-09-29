from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent


def test_phase144_6_r25_11_r6_r1_r1_locator_uses_safe_collector_output_flow():
  source = (
    PHASE_DIR
    / "locate_historical_190.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )

  assert '$collectorOutput = & python ".\\_r25_11_r6_r1_collector.py" 2>&1' in source
  assert "$collectorExitCode = $LASTEXITCODE" in source
  assert "if ($collectorExitCode -ne 0)" in source
  assert "$lastOutputLine = $collectorOutput | Select-Object -Last 1" in source
  assert '$totalLines = $collectorOutput | Where-Object { $_ -like "TOTAL=*" }' in source
  assert "$result = $totalLines | Select-Object -Last 1" in source


def test_phase144_6_r25_11_r6_r1_r1_parent_runner_propagates_child_exit_code():
  source = (
    PHASE_DIR
    / "run_phase144_6_r25_11_r6_r1.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )

  assert "$localizationExitCode = $LASTEXITCODE" in source
  assert "if ($localizationExitCode -ne 0)" in source
  assert "R25-11-R6-R1-R1 completed." in source


def test_phase144_6_r25_11_r6_r1_r1_parent_runner_has_parser_preflight():
  source = (
    PHASE_DIR
    / "run_phase144_6_r25_11_r6_r1.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )

  assert "System.Management.Automation.Language.Parser" in source
  assert "PowerShell parser preflight: PASS" in source
