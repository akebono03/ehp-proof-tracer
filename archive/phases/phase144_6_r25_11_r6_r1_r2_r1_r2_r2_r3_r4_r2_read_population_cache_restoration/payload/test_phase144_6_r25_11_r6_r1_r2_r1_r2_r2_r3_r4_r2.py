from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent
LOCATOR = PHASE_DIR / "locate_historical_190.ps1"


def _source():
  return LOCATOR.read_text(encoding="utf-8-sig")


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_r2_read_population_cache_restored_once():
  source = _source()

  assert source.count("function Read-PopulationCache {") == 1
  assert source.count("function Write-PopulationCache {") == 1
  assert source.count("function Measure-Commit {") == 1


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_r2_read_population_cache_preserves_original_behavior():
  source = _source()
  read_start = source.index("function Read-PopulationCache {")
  write_start = source.index("function Write-PopulationCache {")
  read_source = source[read_start:write_start]

  assert "$result = @()" in read_source
  assert "if (-not (Test-Path $CachePath))" in read_source
  assert '-Description "population cache read"' in read_source
  assert (
    "$script:cacheReadLines = "
    "Get-Content -Path $CachePath -Encoding UTF8"
    in read_source
  )
  assert "foreach ($line in $script:cacheReadLines)" in read_source
  assert "$result += $line" in read_source
  assert "return $result" in read_source


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_r2_helper_order_is_preserved():
  source = _source()

  read_start = source.index("function Read-PopulationCache {")
  write_start = source.index("function Write-PopulationCache {")
  measure_start = source.index("function Measure-Commit {")

  assert read_start < write_start < measure_start


def test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_r2_r4_repairs_remain_present():
  source = _source()

  assert "$addExitCode = $LASTEXITCODE" in source
  assert "$Expected = 190" in source
