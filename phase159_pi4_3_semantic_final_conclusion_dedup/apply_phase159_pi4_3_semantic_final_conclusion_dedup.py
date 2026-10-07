from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

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

PACKAGE_ROOT = Path(__file__).resolve().parent


def insert_import(
  source: str,
) -> str:
  anchor = '''from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
)
'''
  replacement = anchor + '''from toda_group_proof_narrative_statement_identity import (
  toda_group_proof_narrative_statement_semantic_key,
)
'''

  if replacement in source:
    return source

  if anchor not in source:
    raise RuntimeError(
      "contribution renderer import anchor not found"
    )

  return source.replace(
    anchor,
    replacement,
    1,
  )


def insert_function(
  source: str,
) -> str:
  marker = (
    "def suppress_toda_group_proof_narrative_repeated_unique_step_statements(\\n"
  )

  if (
    "def suppress_toda_group_proof_narrative_repeated_root_semantic_conclusion(\\n"
    in source
  ):
    return source

  index = source.find(
    marker
  )

  if index < 0:
    raise RuntimeError(
      "repeated unique-step suppression function anchor not found"
    )

  function_text = 'def suppress_toda_group_proof_narrative_repeated_root_semantic_conclusion(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  root_key = (\n    toda_group_proof_narrative_statement_semantic_key(\n      presentation.root_step.conclusion\n    )\n  )\n\n  semantically_matching_steps = tuple(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      toda_group_proof_narrative_statement_semantic_key(\n        node.proof_step.conclusion\n      )\n      == root_key\n    )\n  )\n\n  if not semantically_matching_steps:\n    return markdown\n\n  rendered_root_keys = {\n    _phase157_r11_reference_statement_match_key(\n      rendered\n    )\n    for proof_step in semantically_matching_steps\n    for rendered in (\n      _render_generic_narrative_step(\n        proof_step\n      ),\n    )\n    if rendered\n  }\n\n  if not rendered_root_keys:\n    return markdown\n\n  connector_prefixes = (\n    "以上より, ",\n    "したがって, ",\n    "これより, ",\n    "これらより, ",\n  )\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  matching_indices = []\n  connected_indices = []\n\n  for index, paragraph in enumerate(\n    paragraphs\n  ):\n    stripped = paragraph.strip()\n    comparable = stripped\n    connected = False\n\n    for prefix in connector_prefixes:\n      if comparable.startswith(\n        prefix\n      ):\n        comparable = comparable[\n          len(\n            prefix\n          ):\n        ]\n        connected = True\n        break\n\n    key = (\n      _phase157_r11_reference_statement_match_key(\n        comparable\n      )\n    )\n\n    if key not in rendered_root_keys:\n      continue\n\n    matching_indices.append(\n      index\n    )\n\n    if connected:\n      connected_indices.append(\n        index\n      )\n\n  if (\n    len(\n      matching_indices\n    )\n    <= 1\n    or not connected_indices\n  ):\n    return markdown\n\n  retained_index = connected_indices[\n    -1\n  ]\n\n  retained = tuple(\n    paragraph\n    for index, paragraph in enumerate(\n      paragraphs\n    )\n    if (\n      index == retained_index\n      or index not in matching_indices\n    )\n  )\n\n  return "\\n\\n".join(\n    retained\n  )\n\n\n'

  return (
    source[
      :index
    ]
    + function_text
    + source[
      index:
    ]
  )


def insert_pipeline_call(
  source: str,
) -> str:
  old = '''  rendered = (
    suppress_toda_group_proof_narrative_repeated_unique_step_statements(
      presentation,
      rendered,
    )
  )
  rendered = (
    insert_toda_group_proof_narrative_map_property_dependencies(
'''
  new = '''  rendered = (
    suppress_toda_group_proof_narrative_repeated_unique_step_statements(
      presentation,
      rendered,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_repeated_root_semantic_conclusion(
      presentation,
      rendered,
    )
  )
  rendered = (
    insert_toda_group_proof_narrative_map_property_dependencies(
'''

  if new in source:
    return source

  if old not in source:
    raise RuntimeError(
      "pipeline insertion anchor not found"
    )

  return source.replace(
    old,
    new,
    1,
  )


def main() -> int:
  source = CONTRIBUTION_PATH.read_text(
    encoding="utf-8",
  )

  updated = insert_import(
    source
  )
  updated = insert_function(
    updated
  )
  updated = insert_pipeline_call(
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
    "Phase 159 semantic final-conclusion dedup applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
