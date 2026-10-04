from pathlib import Path
import shutil
from datetime import datetime


ROOT = Path.cwd()
TARGET = ROOT / "toda_prop58_zero_bootstrap.py"

OLD = '  equation57_step = _find_unique_step(\n    result.steps,\n    lambda step: (\n      isinstance(\n        step.conclusion,\n        Relation,\n      )\n      and isinstance(\n        step.conclusion.lhs,\n        MapApplication,\n      )\n      and step.conclusion.lhs.map\n      == EHP_H_MAP\n      and isinstance(\n        step.conclusion.lhs.expression,\n        Composition,\n      )\n    ),\n    "Equation (5.7)",\n  )\n'
NEW = '  equation57_step = _find_unique_step(\n    result.steps,\n    lambda step: (\n      step.inference_rule is not None\n      and step.inference_rule.name\n      == (\n        "Toda Equation 5.7 "\n        "nu-prime eta_6 Hopf value"\n      )\n    ),\n    "Equation (5.7)",\n  )\n'


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run this script from the ehp-proof-tracer repository root."
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  if source.count(OLD) != 1:
    raise RuntimeError(
      "Equation (5.7) selector block was not found exactly once. "
      "repair3 expects R20 + repair1 + repair2."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase157_r20_repair3_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup_dir / TARGET.name,
  )

  updated = source.replace(
    OLD,
    NEW,
    1,
  )

  compile(
    updated,
    str(TARGET),
    "exec",
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R20 repair3 applied.")
  print("Backup:", backup_dir)
  print("Changed:")
  print(" ", TARGET)

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
