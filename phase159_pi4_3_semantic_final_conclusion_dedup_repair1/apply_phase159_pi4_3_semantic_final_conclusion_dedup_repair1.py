from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent

CONTRIBUTION_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
IDENTITY_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_statement_identity.py"
)
TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_semantic_final_conclusion_dedup.py"
)


def add_import(
  source: str,
) -> str:
  import_text = """from toda_group_proof_narrative_statement_identity import (
  toda_group_proof_narrative_statement_semantic_key,
)
"""

  if import_text in source:
    return source

  anchor = """from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
)
"""

  if anchor not in source:
    raise RuntimeError(
      "semantic import anchor not found"
    )

  return source.replace(
    anchor,
    anchor + import_text,
    1,
  )


def replace_contribution_function(
  source: str,
) -> str:
  start_marker = (
    "def _insert_toda_group_proof_narrative_argument_contributions("
  )
  end_marker = (
    "\ndef _is_toda_group_proof_narrative_reference_statement_candidate("
  )

  start = source.find(
    start_marker
  )

  if start < 0:
    raise RuntimeError(
      "contribution insertion function start not found"
    )

  end = source.find(
    end_marker,
    start,
  )

  if end < 0:
    raise RuntimeError(
      "contribution insertion function end not found"
    )

  replacement = 'def _insert_toda_group_proof_narrative_argument_contributions(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n  ordered_contributions,\n) -> str:\n  insertion_indices = (\n    _contribution_insertion_indices(\n      markdown,\n      blocks,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  connector_by_target_step_id = (\n    _contribution_connector_lines(\n      presentation,\n      ordered_contributions,\n    )\n  )\n\n  root_semantic_key = (\n    toda_group_proof_narrative_statement_semantic_key(\n      presentation.root_step.conclusion\n    )\n  )\n  argument_conclusion_semantic_keys = {\n    toda_group_proof_narrative_statement_semantic_key(\n      conclusion_step.conclusion\n    )\n    for argument in arguments\n    for conclusion_step in (\n      extract_toda_group_proof_narrative_argument_conclusion_step(\n        argument\n      ),\n    )\n    if conclusion_step is not None\n  }\n  root_conclusion_owned_by_argument = (\n    root_semantic_key\n    in argument_conclusion_semantic_keys\n  )\n\n  insertions_by_index = {}\n\n  for argument_index, contributions in enumerate(\n    ordered_contributions\n  ):\n    for contribution_index, contribution in enumerate(\n      contributions\n    ):\n      if (\n        root_conclusion_owned_by_argument\n        and (\n          toda_group_proof_narrative_statement_semantic_key(\n            contribution.proof_step.conclusion\n          )\n          == root_semantic_key\n        )\n      ):\n        continue\n\n      contribution_line = (\n        _render_generic_narrative_step(\n          contribution.proof_step\n        )\n      )\n\n      if not contribution_line:\n        continue\n\n      if not (\n        _is_toda_group_proof_narrative_reference_statement_candidate(\n          contribution.proof_step,\n          contribution_line,\n        )\n      ):\n        continue\n\n      if contribution_line in markdown:\n        continue\n\n      insertion_index = insertion_indices[\n        argument_index\n      ][\n        contribution_index\n      ]\n\n      if insertion_index is None:\n        continue\n\n      connector = (\n        connector_by_target_step_id.get(\n          id(\n            contribution.proof_step\n          )\n        )\n      )\n      lines = []\n\n      if connector is not None:\n        lines.append(\n          connector\n        )\n\n      lines.append(\n        contribution_line\n      )\n\n      insertions_by_index.setdefault(\n        insertion_index,\n        [],\n      ).append(\n        "\\n\\n".join(\n          lines\n        )\n      )\n\n  rendered = markdown\n\n  for insertion_index in sorted(\n    insertions_by_index,\n    reverse=True,\n  ):\n    contribution_fragments = insertions_by_index[\n      insertion_index\n    ]\n    insertion = (\n      "\\n\\n"\n      + "\\n\\n".join(\n        contribution_fragments\n      )\n    )\n\n    if (\n      insertion_index < len(\n        markdown\n      )\n      and not markdown[\n        insertion_index:\n      ].startswith(\n        "\\n\\n"\n      )\n    ):\n      insertion += "\\n\\n"\n\n    rendered = (\n      rendered[\n        :insertion_index\n      ]\n      + insertion\n      + rendered[\n        insertion_index:\n      ]\n    )\n\n  return rendered\n'

  return (
    source[:start]
    + replacement.rstrip()
    + "\n"
    + source[end:]
  )


def main() -> int:
  source = CONTRIBUTION_PATH.read_text(
    encoding="utf-8",
  )
  updated = add_import(
    source
  )
  updated = replace_contribution_function(
    updated
  )

  CONTRIBUTION_PATH.write_text(
    updated,
    encoding="utf-8",
  )
  IDENTITY_PATH.write_text(
    (
      PACKAGE_ROOT
      / "toda_group_proof_narrative_statement_identity.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )
  TEST_PATH.write_text(
    (
      PACKAGE_ROOT
      / "test_phase159_pi4_3_semantic_final_conclusion_dedup.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 repair1 applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
