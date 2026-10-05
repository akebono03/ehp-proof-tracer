from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "tests"
  / "test_phase157_r11_reference_reason_punctuation.py"
)


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair36_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup / TARGET.name,
  )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  old = (
    "  fixed_hopf = (\n"
    "    \"[R2]より, \"\n"
    "    r\"$H\\left(\\nu'\\right)=\\eta_{5}$.\"\n"
    "  )\n"
  )

  new = (
    "  fixed_hopf = (\n"
    "    \"[R2]より, \"\n"
    "    r\"$H\\left(\\nu'\\right) = \\eta_{5}$.\"\n"
    "  )\n"
  )

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "stale fixed_hopf spacing expectation "
      "was not found exactly once"
    )

  source = source.replace(
    old,
    new,
    1,
  )

  compile(
    source,
    str(
      TARGET
    ),
    "exec",
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair36 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Updated test:",
    TARGET,
  )
  print(
    "Production code changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
