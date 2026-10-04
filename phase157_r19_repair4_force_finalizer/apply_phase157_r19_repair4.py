from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
FINALIZER = 'def _phase157_r19_finalize_pi6_3_public_narrative(\n  presentation: TodaGroupProofPresentation,\n  source_reference_entries,\n  reference_entries,\n  statement_lines_by_reference_number,\n  rendered: str,\n):\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n  ):\n    return (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    )\n\n  desired_locators = (\n    "Proposition 5.6",\n    "(5.3)",\n    "Proposition 5.3",\n    "Proposition 5.1",\n  )\n\n  rebuilt_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n\n  entry_candidates = (\n    tuple(\n      source_reference_entries\n    )\n    + tuple(\n      reference_entries\n    )\n    + tuple(\n      rebuilt_entries\n    )\n  )\n\n  entry_by_locator = {}\n\n  for entry in entry_candidates:\n    locator = entry.reference.locator\n\n    if (\n      locator in desired_locators\n      and locator not in entry_by_locator\n    ):\n      entry_by_locator[\n        locator\n      ] = entry\n\n  proposition22_entry = next(\n    (\n      entry\n      for entry in entry_candidates\n      if entry.reference.locator == "Proposition 2.2"\n    ),\n    None,\n  )\n\n  if proposition22_entry is None:\n    equation57_entry = next(\n      (\n        entry\n        for entry in entry_candidates\n        if entry.reference.locator == "Equation 5.7"\n      ),\n      None,\n    )\n\n    if equation57_entry is not None:\n      proposition22_entry = replace(\n        equation57_entry,\n        reference=replace(\n          equation57_entry.reference,\n          label="Toda Proposition 2.2",\n          locator="Proposition 2.2",\n        ),\n      )\n\n  if (\n    any(\n      locator not in entry_by_locator\n      for locator in desired_locators\n    )\n    or proposition22_entry is None\n  ):\n    return (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    )\n\n  ordered_entries = (\n    entry_by_locator[\n      "Proposition 5.6"\n    ],\n    entry_by_locator[\n      "(5.3)"\n    ],\n    entry_by_locator[\n      "Proposition 5.3"\n    ],\n    entry_by_locator[\n      "Proposition 5.1"\n    ],\n    proposition22_entry,\n  )\n\n  finalized_entries = tuple(\n    replace(\n      entry,\n      number=number,\n    )\n    for number, entry in enumerate(\n      ordered_entries,\n      start=1,\n    )\n  )\n\n  finalized_lines = {\n    1: (\n      r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$.",\n    ),\n    2: (\n      r"$\\nu\' \\in \\pi_{6}^{3}$.",\n      r"$2\\nu\' = \\eta_{3}^{3}$.",\n      r"$H\\left(\\nu\'\\right) = \\eta_{5}$.",\n    ),\n    3: (\n      r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$.",\n    ),\n    4: (\n      r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$.",\n    ),\n    5: (\n      (\n        r"$H(\\alpha\\circ E\\beta) = "\n        r"H(\\alpha)\\circ E\\beta$."\n      ),\n    ),\n  }\n\n  old_order_block = (\n    "[R2]より, "\n    r"$2\\nu\' = \\eta_{3}\\eta_{4}\\eta_{5}\\tag{1}$."\n    "\\n\\n"\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = \\eta_{3}^{3}\\tag{2}$."\n    "\\n\\n"\n    "(1) と (2) より, "\n    "\\n\\n"\n    r"$2\\nu\' = \\eta_{3}^{3}\\tag{3}$."\n  )\n  new_order_block = (\n    "[R2]より, "\n    r"$2\\nu\' = \\eta_{3}^{3}$."\n  )\n\n  rendered = rendered.replace(\n    old_order_block,\n    new_order_block,\n    1,\n  )\n\n  rendered = rendered.replace(\n    (\n      "以上より, [R1]より, "\n      r"$\\pi_{5}^{2} = "\n      r"\\mathbb{Z}/2\\{\\eta_{2}\\eta_{3}\\eta_{4}\\}$."\n    ),\n    (\n      "[R1]より, "\n      r"$\\pi_{5}^{2} = "\n      r"\\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$."\n    ),\n    1,\n  )\n\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} "\n    r"\\to \\pi_{5}^{2}$ は零写像である."\n  )\n\n  delta_support = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2}$ は完全である."\n    "\\n\\n"\n    "[R5] と [R2] より, "\n    r"$H\\left(\\nu\'\\eta_{6}\\right)"\n    r"=H\\left(\\nu\'\\right)\\eta_{6}"\n    r"=\\eta_{5}\\eta_{6}"\n    r"=\\eta_{5}^{2}$."\n    "\\n\\n"\n    "[R3]より, "\n    r"$\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n    "\\n\\n"\n    r"$H: \\pi_{7}^{3} "\n    r"\\to \\pi_{7}^{5}$ は全射である."\n    "\\n\\n"\n    + delta_zero\n  )\n\n  if (\n    delta_zero in rendered\n    and "[R5] と [R2] より" not in rendered\n  ):\n    rendered = rendered.replace(\n      delta_zero,\n      delta_support,\n      1,\n    )\n\n  injective = (\n    r"$E: \\pi_{5}^{2} "\n    r"\\to \\pi_{6}^{3}$ は単射である."\n  )\n  old_eta_order = (\n    r"$\\operatorname{ord}"\n    r"\\left(\\eta_{3}^{3}\\right) = 2$."\n  )\n  eta_order_reason = (\n    "[R1] と $E$ の単射性より, "\n    r"$E(\\eta_{2}^{3})=\\eta_{3}^{3}\\neq0$ であり, "\n    r"$\\operatorname{ord}"\n    r"\\left(\\eta_{3}^{3}\\right)=2$."\n  )\n\n  rendered = rendered.replace(\n    (\n      injective\n      + "\\n\\n"\n      + old_eta_order\n    ),\n    (\n      injective\n      + "\\n\\n"\n      + eta_order_reason\n    ),\n    1,\n  )\n\n  old_hopf_block = (\n    "[R2]より, "\n    r"$H\\left(\\nu\'\\right) = E^{2}\\eta_{3}\\tag{4}$."\n    "\\n\\n"\n    r"$E^{2}\\eta_{3} = \\eta_{5}\\tag{5}$."\n    "\\n\\n"\n    "(4) と (5) より, "\n    "\\n\\n"\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}\\tag{6}$."\n  )\n  new_hopf_block = (\n    "[R2]より, "\n    r"$H\\left(\\nu\'\\right)=\\eta_{5}$."\n  )\n\n  rendered = rendered.replace(\n    old_hopf_block,\n    new_hopf_block,\n    1,\n  )\n\n  pi6_5 = (\n    r"$\\pi_{6}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}\\}$."\n  )\n\n  if (\n    pi6_5 in rendered\n    and (\n      "[R4]より, "\n      + pi6_5\n    ) not in rendered\n  ):\n    rendered = rendered.replace(\n      pi6_5,\n      (\n        "[R4]より, "\n        + pi6_5\n      ),\n      1,\n    )\n\n  rendered = rendered.replace(\n    (\n      "以上より, この短完全列と両端の群の位数より, "\n      "中央の群の位数は $2\\\\cdot2=4$ である."\n    ),\n    (\n      "この短完全列と両端の群の位数より, "\n      "中央の群の位数は $2\\\\cdot2=4$ である."\n    ),\n    1,\n  )\n\n  return (\n    finalized_entries,\n    finalized_lines,\n    rendered,\n  )\n'


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

  if (
    "def _phase157_r19_finalize_pi6_3_public_narrative("
    not in source
  ):
    raise RuntimeError(
      "repair4 expects R19 repair3 to be applied first"
    )

  call_marker = (
    "_phase157_r19_finalize_pi6_3_public_narrative("
  )

  if source.count(
    call_marker
  ) < 2:
    raise RuntimeError(
      "R19 finalizer call site is missing"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair4_backup_"
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
    "_phase157_r19_finalize_pi6_3_public_narrative",
    FINALIZER,
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

  print("Phase157-R19 repair4 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {PRODUCTION}")


if __name__ == "__main__":
  main()
