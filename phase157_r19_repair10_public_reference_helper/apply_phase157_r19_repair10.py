from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
REPLACEMENT = 'def _phase157_r19_public_reference_statement_lines(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n) -> dict[\n  int,\n  tuple[\n    str,\n    ...,\n  ],\n]:\n  public_lines = dict(\n    statement_lines_by_reference_number\n  )\n\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n  ):\n    return public_lines\n\n  for entry in reference_entries:\n    locator = entry.reference.locator\n\n    if locator == "Proposition 5.6":\n      public_lines[\n        entry.number\n      ] = (\n        r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$.",\n      )\n      continue\n\n    if locator == "(5.3)":\n      public_lines[\n        entry.number\n      ] = (\n        (\n          r"$\\nu\' \\in "\n          r"\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}$ とする."\n        ),\n        r"$\\nu\' \\in \\pi_{6}^{3}$.",\n        r"$2\\nu\' = \\eta_{3}^{3}$.",\n        r"$H\\left(\\nu\'\\right) = \\eta_{5}$.",\n      )\n      continue\n\n    if locator == "Proposition 5.3":\n      public_lines[\n        entry.number\n      ] = (\n        r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$.",\n      )\n      continue\n\n    if locator == "Proposition 5.1":\n      public_lines[\n        entry.number\n      ] = (\n        r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$.",\n      )\n      continue\n\n    if locator == "Proposition 2.2":\n      public_lines[\n        entry.number\n      ] = (\n        (\n          r"$H(\\alpha\\circ E\\beta) = "\n          r"H(\\alpha)\\circ E\\beta$."\n        ),\n      )\n\n  return public_lines\n'


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
  if not PRODUCTION.is_file():
    raise RuntimeError(
      "Run from the ehp-proof-tracer repository root."
    )

  source = PRODUCTION.read_text(
    encoding="utf-8"
  )

  name = (
    "_phase157_r19_public_reference_statement_lines"
  )

  if f"def {name}(" not in source:
    raise RuntimeError(
      "R19 public reference helper was not found"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair10_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    PRODUCTION,
    backup / PRODUCTION.name,
  )

  source = replace_function(
    source,
    name,
    REPLACEMENT,
  )

  compile(
    source,
    str(PRODUCTION),
    "exec",
  )

  PRODUCTION.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair10 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {PRODUCTION}")


if __name__ == "__main__":
  main()
