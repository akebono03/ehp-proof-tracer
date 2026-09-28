from pathlib import Path


def test_phase144_6_r25_11_r6_r1_collector_keeps_six_group_boundary():
  source = (
    Path(__file__).resolve().parent
    / "collect_selected_total.py"
  ).read_text(
    encoding="utf-8"
  )

  assert "(3, 3)" in source
  assert "(5, 3)" in source
  assert "(4, 6)" in source
  assert "(5, 7)" in source
  assert "(8, 7)" in source
  assert "(9, 7)" in source


def test_phase144_6_r25_11_r6_r1_locator_requires_real_190():
  source = (
    Path(__file__).resolve().parent
    / "locate_historical_190.ps1"
  ).read_text(
    encoding="utf-8-sig"
  )

  assert "$Expected = 190" in source
  assert "EXACT_190_SHA=" in source
  assert "EXACT_190_COUNT=0" in source
