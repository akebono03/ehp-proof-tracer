from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
TEST = ROOT / "tests" / "test_phase157_r3_pi6_3_reference_boundary.py"
NEW_TEST = 'def test_phase157_r3_pi6_3_depth3_suppresses_prop53_internal_suspension():\n  reference, body = _reference_and_body(\n    _render_pi6_3(3)\n  )\n\n  assert "Proposition 5.3" in reference\n  assert (\n    r"\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}"\n    in reference\n  )\n  assert (\n    r"E: \\pi_{4}^{2} \\to \\pi_{5}^{3}"\n    not in reference\n  )\n  assert (\n    r"E: \\pi_{4}^{2} \\to \\pi_{5}^{3}"\n    not in body\n  )\n'


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  marker = f"def {name}("
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      f"function not found: {name}"
    )

  next_match = re.search(
    r"^def [A-Za-z_][A-Za-z0-9_]*\(",
    source[start + len(marker):],
    flags=re.MULTILINE,
  )

  if next_match is None:
    end = len(source)
  else:
    end = (
      start
      + len(marker)
      + next_match.start()
    )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def main() -> None:
  if not TEST.is_file():
    raise RuntimeError(
      "Run from the ehp-proof-tracer repository root."
    )

  source = TEST.read_text(
    encoding="utf-8"
  )

  old_name = (
    "test_phase157_r3_pi6_3_depth3_keeps_prop53_derived_suspension_in_body"
  )

  if f"def {old_name}(" not in source:
    raise RuntimeError(
      "stale Phase157-R3 depth3 test was not found"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair7_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TEST,
    backup / TEST.name,
  )

  source = replace_function(
    source,
    old_name,
    NEW_TEST,
  )

  compile(
    source,
    str(TEST),
    "exec",
  )

  TEST.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair7 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {TEST}")


if __name__ == "__main__":
  main()
