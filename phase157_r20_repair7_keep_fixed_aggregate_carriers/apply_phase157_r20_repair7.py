from __future__ import annotations

import ast
import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()

REFERENCES = (
  ROOT
  / "toda_group_proof_narrative_references.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair7_fixed_aggregate_carriers.py"
)

NEW_IMPORT = 'from toda_literature_statement_boundary import (\n  TodaLiteratureStatementClassification,\n  classify_toda_literature_statement_step,\n  get_toda_fixed_statement_component,\n  get_toda_fixed_statement_components,\n  is_toda_fixed_statement_component_reference_eligible,\n)\n'
NEW_FUNCTION = 'def filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(\n  entries: tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  root_step: ProofStep,\n) -> tuple[\n  TodaGroupProofNarrativeReferenceEntry,\n  ...,\n]:\n  if not isinstance(\n    entries,\n    tuple,\n  ):\n    raise TypeError(\n      "entries must be a tuple"\n    )\n\n  if not all(\n    isinstance(\n      entry,\n      TodaGroupProofNarrativeReferenceEntry,\n    )\n    for entry in entries\n  ):\n    raise TypeError(\n      "entries must contain only "\n      "TodaGroupProofNarrativeReferenceEntry objects"\n    )\n\n  if not isinstance(\n    root_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "root_step must be a ProofStep"\n    )\n\n  root_boundary = (\n    classify_toda_literature_statement_step(\n      root_step\n    )\n  )\n\n  target_reference_locator = (\n    None\n    if root_boundary is None\n    else root_boundary.reference_locator\n  )\n  target_component_key = (\n    None\n    if root_boundary is None\n    else root_boundary.component_key\n  )\n\n  retained_entries = []\n\n  for entry in entries:\n    retained_steps = []\n\n    for proof_step in entry.proof_steps:\n      boundary = (\n        classify_toda_literature_statement_step(\n          proof_step\n        )\n      )\n\n      if (\n        boundary is None\n        or boundary.classification\n        != TodaLiteratureStatementClassification.FIXED_STATEMENT\n      ):\n        continue\n\n      if boundary.component_key is None:\n        fixed_components = (\n          get_toda_fixed_statement_components(\n            boundary.reference_locator\n          )\n        )\n\n        if fixed_components:\n          retained_steps.append(\n            proof_step\n          )\n\n        continue\n\n      component = (\n        get_toda_fixed_statement_component(\n          boundary.reference_locator,\n          boundary.component_key,\n        )\n      )\n\n      if component is None:\n        continue\n\n      if (\n        target_reference_locator is not None\n        and target_component_key is not None\n        and not is_toda_fixed_statement_component_reference_eligible(\n          component,\n          target_reference_locator,\n          target_component_key,\n        )\n      ):\n        continue\n\n      retained_steps.append(\n        proof_step\n      )\n\n    if not retained_steps:\n      continue\n\n    retained_entries.append(\n      replace(\n        entry,\n        number=len(\n          retained_entries\n        ) + 1,\n        proof_steps=tuple(\n          retained_steps\n        ),\n      )\n    )\n\n  return tuple(\n    retained_entries\n  )\n'
TEST_SOURCE = 'from pathlib import Path\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_r20_repair7() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair7_fixed_aggregate_carriers_reach_reference_selection():\n  rendered = _render_pi6_3_r20_repair7()\n\n  for locator in (\n    "Proposition 5.6",\n    "(5.3)",\n    "Proposition 5.3",\n    "Proposition 5.1",\n    "Proposition 2.2",\n  ):\n    assert locator in rendered\n\n\ndef test_phase157_r20_repair7_aggregate_component_selection_stays_minimal():\n  rendered = _render_pi6_3_r20_repair7()\n\n  assert (\n    r"$\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n    in rendered\n  )\n  assert (\n    r"$\\pi_{6}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}\\}$."\n    in rendered\n  )\n\n  assert (\n    r"$\\pi_{4}^{2}"\n    not in rendered.split(\n      "**[R3] Proposition 5.3.**",\n      1,\n    )[1].split(\n      "**[R4]",\n      1,\n    )[0]\n  )\n\n\ndef test_phase157_r20_repair7_has_no_target_specific_reference_logic():\n  source = Path(\n    "toda_group_proof_narrative_references.py"\n  ).read_text(\n    encoding="utf-8"\n  )\n\n  forbidden = (\n    "is_pi6_3",\n    "filter_phase157_r3_pi6_3_reference_entries",\n    "_phase157_r3_is_pi6_3_root",\n    "restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage",\n  )\n\n  for token in forbidden:\n    assert token not in source\n'


def function_range(
  source: str,
  name: str,
) -> tuple[
  int,
  int,
]:
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        (
          ast.FunctionDef,
          ast.AsyncFunctionDef,
        ),
      )
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(line)
        for line in lines[
          :node.end_lineno
        ]
      )

      while (
        end < len(source)
        and source[
          end:
          end + 1
        ] == "\n"
      ):
        end += 1

      return (
        start,
        end,
      )

  raise RuntimeError(
    "function not found: "
    + name
  )


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    name,
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def replace_boundary_import(
  source: str,
) -> str:
  pattern = re.compile(
    r"from toda_literature_statement_boundary import \(\n"
    r".*?\n\)",
    flags=re.DOTALL,
  )
  match = pattern.search(
    source
  )

  if match is None:
    raise RuntimeError(
      "toda_literature_statement_boundary import block not found"
    )

  return (
    source[:match.start()]
    + NEW_IMPORT.rstrip()
    + source[match.end():]
  )


def main() -> int:
  if not REFERENCES.is_file():
    raise RuntimeError(
      "missing file: "
      + str(
        REFERENCES
      )
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair7_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    REFERENCES,
    backup / REFERENCES.name,
  )

  source = REFERENCES.read_text(
    encoding="utf-8"
  )

  source = replace_boundary_import(
    source
  )
  source = replace_function(
    source,
    "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary",
    NEW_FUNCTION,
  )

  forbidden = (
    "is_pi6_3",
    "filter_phase157_r3_pi6_3_reference_entries",
    "_phase157_r3_is_pi6_3_root",
    "restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage",
  )

  for token in forbidden:
    if token in source:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    source,
    str(
      REFERENCES
    ),
    "exec",
  )
  compile(
    TEST_SOURCE,
    str(
      TEST
    ),
    "exec",
  )

  REFERENCES.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair7 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed:"
  )
  print(
    " ",
    REFERENCES,
  )
  print(
    " ",
    TEST,
  )
  print("")
  print(
    "Architecture preflight:"
  )
  for token in forbidden:
    print(
      " ",
      token,
      "=",
      source.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
