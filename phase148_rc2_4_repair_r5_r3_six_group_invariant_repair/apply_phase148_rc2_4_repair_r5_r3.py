from pathlib import Path
import shutil


def main():
  source = Path(
    "phase148_rc2_4_repair_r5_r3_six_group_invariant_repair"
  ) / "test_phase148_rc2_4_post_repair_six_group.py"
  target = Path(
    "tests"
  ) / "test_phase148_rc2_4_post_repair_six_group.py"

  if not source.exists():
    raise SystemExit(
      "replacement audit test source not found"
    )

  shutil.copyfile(
    source,
    target,
  )

  print(
    "R5-R3 six-group audit invariant repaired."
  )
  print(
    "Production changes: none."
  )
  print(
    "The invariant now identifies actual "
    "TodaProp42ExactnessStatement renderings."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
