from __future__ import annotations

from pathlib import Path


TARGET = Path(
  "phase157_r5_r5_112_group_cross_audit"
) / "audit_phase157_r5_r5.py"

OLD = """from pathlib import Path

from toda_calculation_facade import (
"""

NEW = """from pathlib import Path
import sys


REPOSITORY_ROOT = Path.cwd()
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )


from toda_calculation_facade import (
"""


def main() -> None:
  if not TARGET.exists():
    raise SystemExit(
      "target audit script not found: "
      + str(
        TARGET
      )
    )

  text = TARGET.read_text(
    encoding="utf-8"
  )

  if OLD not in text:
    if "REPOSITORY_ROOT = Path.cwd()" in text:
      print(
        "Phase157-R5-R5 repair1 is already applied."
      )
      return

    raise SystemExit(
      "expected import anchor not found"
    )

  text = text.replace(
    OLD,
    NEW,
    1,
  )

  TARGET.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R5 repair1 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Existing tests changes: none"
  )
  print(
    "Audit logic changes: none"
  )
  print(
    "Added repository root to sys.path before project imports."
  )


if __name__ == "__main__":
  main()
