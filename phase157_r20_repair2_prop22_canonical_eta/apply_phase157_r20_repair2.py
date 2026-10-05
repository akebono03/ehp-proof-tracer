from pathlib import Path
import shutil
from datetime import datetime


ROOT = Path.cwd()
TARGET = ROOT / "toda_rules.py"

OLD = '    expected_prop22_relation = Relation(\n      lhs=MapApplication(\n        map=EHP_H_MAP,\n        expression=Composition(\n          left=nu_prime,\n          right=Suspension(\n            expression=eta5_definition_element,\n          ),\n        ),\n      ),\n      rhs=Composition(\n        left=MapApplication(\n          map=EHP_H_MAP,\n          expression=nu_prime,\n        ),\n        right=Suspension(\n          expression=eta5_definition_element,\n        ),\n      ),\n      relation_type=RelationType.EQUALITY,\n    )\n'
NEW = '    expected_prop22_relation = Relation(\n      lhs=MapApplication(\n        map=EHP_H_MAP,\n        expression=Composition(\n          left=nu_prime,\n          right=Suspension(\n            expression=canonical_eta_5,\n          ),\n        ),\n      ),\n      rhs=Composition(\n        left=MapApplication(\n          map=EHP_H_MAP,\n          expression=nu_prime,\n        ),\n        right=Suspension(\n          expression=canonical_eta_5,\n        ),\n      ),\n      relation_type=RelationType.EQUALITY,\n    )\n'


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run this script from the ehp-proof-tracer repository root."
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  if OLD not in source:
    raise RuntimeError(
      "R20 Proposition 2.2 guard block was not found. "
      "repair2 expects R20 + repair1 to be applied."
    )

  if source.count(OLD) != 1:
    raise RuntimeError(
      "R20 Proposition 2.2 guard block is not unique."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase157_r20_repair2_backup_"
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

  print("Phase157-R20 repair2 applied.")
  print("Backup:", backup_dir)
  print("Changed:")
  print(" ", TARGET)

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
