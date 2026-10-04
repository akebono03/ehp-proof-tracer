from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
TEST = ROOT / "tests" / "test_phase157_r3_pi6_3_reference_boundary.py"
NEW_TEST = 'def test_phase157_r3_pi6_3_same_proposition_earlier_component_survives_root_exclusion():\n  reference, _ = _reference_and_body(\n    _render_pi6_3(2)\n  )\n\n  assert "Proposition 5.6" in reference\n  assert (\n    r"\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}"\n    in reference\n  )\n'


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

  name = (
    "test_phase157_r3_pi6_3_same_proposition_earlier_component_survives_root_exclusion"
  )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair8_backup_"
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
    name,
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

  print("Phase157-R19 repair8 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {TEST}")


if __name__ == "__main__":
  main()
