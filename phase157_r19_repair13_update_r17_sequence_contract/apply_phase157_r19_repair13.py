from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
TEST = ROOT / "tests" / "test_phase157_r11_r17_residual_narrative_defects.py"
NEW_TEST = 'def test_phase157_r11_r17_pi6_3_uses_one_full_initial_exact_sequence_and_trims_later_sequence():\n  _, body = _reference_and_body(\n    3,\n    3,\n  )\n\n  old_short_sequence = (\n    r"$\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$."\n  )\n  full_initial_sequence = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  redundant_four_term = (\n    r"$\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3} \\xrightarrow{H} "\n    r"\\pi_{6}^{5}$."\n  )\n  trimmed_sequence = (\n    r"$\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3} \\xrightarrow{H} "\n    r"\\pi_{6}^{5}$."\n  )\n\n  assert old_short_sequence not in body\n  assert full_initial_sequence in body\n  assert redundant_four_term not in body\n  assert trimmed_sequence in body\n'


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
    "test_phase157_r11_r17_pi6_3_keeps_first_delta_sequence_but_trims_second"
  )

  if f"def {old_name}(" not in source:
    raise RuntimeError(
      "stale R17 sequence contract was not found"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair13_backup_"
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

  print("Phase157-R19 repair13 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {TEST}")


if __name__ == "__main__":
  main()
