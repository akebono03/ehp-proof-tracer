from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = ROOT / "tests" / "test_phase157_r19_pi6_3_reference_dependency_restoration.py"

HELPERS = 'def _phase157_r19_restore_prop22_reference_for_pi6_3(\n  presentation: TodaGroupProofPresentation,\n  source_entries,\n  filtered_entries,\n):\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n  ):\n    return filtered_entries\n\n  if any(\n    entry.reference.locator == "Proposition 2.2"\n    for entry in filtered_entries\n  ):\n    return filtered_entries\n\n  equation57_entries = tuple(\n    entry\n    for entry in source_entries\n    if entry.reference.locator == "Equation 5.7"\n  )\n\n  if len(\n    equation57_entries\n  ) != 1:\n    return filtered_entries\n\n  equation57_entry = equation57_entries[0]\n\n  proposition22_entry = replace(\n    equation57_entry,\n    number=len(filtered_entries) + 1,\n    reference=replace(\n      equation57_entry.reference,\n      label="Toda Proposition 2.2",\n      locator="Proposition 2.2",\n    ),\n  )\n\n  return tuple(\n    replace(\n      entry,\n      number=number,\n    )\n    for number, entry in enumerate(\n      filtered_entries + (proposition22_entry,),\n      start=1,\n    )\n  )\n\n\ndef _phase157_r19_public_reference_statement_lines(\n  reference_entries,\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[str, ...],\n  ],\n) -> dict[\n  int,\n  tuple[str, ...],\n]:\n  public_lines = dict(\n    statement_lines_by_reference_number\n  )\n\n  for entry in reference_entries:\n    locator = entry.reference.locator\n\n    if locator == "Proposition 2.2":\n      public_lines[entry.number] = (\n        (\n          r"$H(\\alpha\\circ E\\beta) = "\n          r"H(\\alpha)\\circ E\\beta$."\n        ),\n      )\n      continue\n\n    if locator != "(5.3)":\n      continue\n\n    lines = public_lines.get(\n      entry.number,\n      (),\n    )\n\n    public_lines[entry.number] = tuple(\n      (\n        r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n        if (\n          r"$H\\left(\\nu\'\\right) = "\n          r"E^{2}\\eta_{3}$."\n          == line\n        )\n        else line\n      )\n      for line in lines\n    )\n\n  return public_lines\n'
TEST_HELPER = 'def _render_pi6_3() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n'


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

  if not TEST.is_file():
    raise RuntimeError(
      f"missing test file: {TEST}"
    )

  production = PRODUCTION.read_text(
    encoding="utf-8"
  )
  test_source = TEST.read_text(
    encoding="utf-8"
  )

  required_call = (
    "_phase157_r19_restore_prop22_reference_for_pi6_3("
  )

  if required_call not in production:
    raise RuntimeError(
      "R19 call site is missing; apply this repair "
      "after the first R19 package."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair1_backup_"
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
  shutil.copy2(
    TEST,
    backup / TEST.name,
  )

  helper_marker = (
    "def _phase157_r19_restore_prop22_reference_for_pi6_3("
  )
  public_helper_marker = (
    "def _phase157_r19_public_reference_statement_lines("
  )

  if (
    helper_marker not in production
    or public_helper_marker not in production
  ):
    insertion_marker = (
      "def _toda_group_proof_narrative_reference_statement_lines_by_number("
    )
    insertion_index = production.find(
      insertion_marker
    )

    if insertion_index < 0:
      raise RuntimeError(
        "reference helper insertion point not found"
      )

    production = (
      production[:insertion_index]
      + HELPERS.rstrip()
      + "\n\n\n"
      + production[insertion_index:]
    )

  test_source = replace_function(
    test_source,
    "_render_pi6_3",
    TEST_HELPER,
  )

  compile(
    production,
    str(PRODUCTION),
    "exec",
  )
  compile(
    test_source,
    str(TEST),
    "exec",
  )

  PRODUCTION.write_text(
    production,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    test_source,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair1 applied.")
  print(f"Backup: {backup}")
  print("Repaired:")
  print(f"  {PRODUCTION}")
  print(f"  {TEST}")


if __name__ == "__main__":
  main()
