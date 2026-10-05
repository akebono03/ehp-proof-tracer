from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
BOUNDARY = ROOT / "toda_literature_statement_boundary.py"
REFERENCES = ROOT / "toda_group_proof_narrative_references.py"
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair53_r3_fixed_reference_attribution.py"
)

REPLACEMENT_EXTRACT = 'def extract_toda_group_proof_step_literature_reference(\n  proof_step: ProofStep,\n) -> LiteratureReference | None:\n  if not isinstance(proof_step, ProofStep):\n    raise TypeError("proof_step must be a ProofStep")\n\n  inference_rule = proof_step.inference_rule\n  if inference_rule is None:\n    return None\n\n  boundary = classify_toda_literature_statement_step(\n    proof_step\n  )\n\n  if (\n    boundary is not None\n    and boundary.classification\n    == TodaLiteratureStatementClassification.FIXED_STATEMENT\n  ):\n    fixed_locator = boundary.reference_locator\n    existing_reference = (\n      inference_rule.literature_reference\n    )\n\n    if (\n      existing_reference is not None\n      and existing_reference.locator\n      == fixed_locator\n    ):\n      return existing_reference\n\n    if existing_reference is not None:\n      return replace(\n        existing_reference,\n        label="Toda " + fixed_locator,\n        locator=fixed_locator,\n      )\n\n    return LiteratureReference(\n      label="Toda " + fixed_locator,\n      locator=fixed_locator,\n    )\n\n  if inference_rule.literature_reference is not None:\n    return inference_rule.literature_reference\n\n  return _infer_toda_group_proof_literature_reference_from_rule_name(\n    inference_rule.name\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  extract_toda_group_proof_step_literature_reference,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_literature_statement_boundary import (\n  TodaLiteratureStatementClassification,\n  classify_toda_literature_statement_step,\n)\nfrom toda_rules import (\n  TodaProp44IsomorphismStatement,\n)\n\n\nRULE_NAME = (\n  "Toda Proposition 5.15 sigma_8 n=8 "\n  "Proposition 4.4 decomposition specialization"\n)\n\n\ndef _repair53_r3_data():\n  report = build_standard_toda_report(\n    n=8,\n    k=7,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n\n  prop44_step = next(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      isinstance(\n        node.proof_step.conclusion,\n        TodaProp44IsomorphismStatement,\n      )\n      and node.proof_step.inference_rule is not None\n      and node.proof_step.inference_rule.name\n      == RULE_NAME\n    )\n  )\n\n  return (\n    raw,\n    presentation,\n    prop44_step,\n  )\n\n\ndef test_phase157_r20_repair53_r3_n8_prop44_is_fixed_statement():\n  (\n    raw,\n    presentation,\n    prop44_step,\n  ) = _repair53_r3_data()\n\n  boundary = classify_toda_literature_statement_step(\n    prop44_step\n  )\n\n  assert boundary is not None\n  assert (\n    boundary.classification\n    == TodaLiteratureStatementClassification.FIXED_STATEMENT\n  )\n  assert (\n    boundary.reference_locator\n    == "Proposition 4.4"\n  )\n  assert (\n    boundary.component_key\n    == "nu4_decomposition_isomorphism"\n  )\n\n\ndef test_phase157_r20_repair53_r3_reference_identity_uses_prop44():\n  (\n    raw,\n    presentation,\n    prop44_step,\n  ) = _repair53_r3_data()\n\n  reference = (\n    extract_toda_group_proof_step_literature_reference(\n      prop44_step\n    )\n  )\n\n  assert reference is not None\n  assert reference.locator == "Proposition 4.4"\n  assert reference.label == "Toda Proposition 4.4"\n\n\ndef test_phase157_r20_repair53_r3_graph_entries_split_prop44_from_prop515():\n  (\n    raw,\n    presentation,\n    prop44_step,\n  ) = _repair53_r3_data()\n\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n\n  locators = tuple(\n    entry.reference.locator\n    for entry in entries\n  )\n\n  assert "Proposition 4.4" in locators\n  assert "Proposition 5.15" in locators\n\n  prop44_entry = next(\n    entry\n    for entry in entries\n    if entry.reference.locator\n    == "Proposition 4.4"\n  )\n\n  assert prop44_step in prop44_entry.proof_steps\n\n\ndef test_phase157_r20_repair53_r3_public_pi15_8_restores_prop44_reference():\n  (\n    raw,\n    presentation,\n    prop44_step,\n  ) = _repair53_r3_data()\n\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n\n  assert "Toda Proposition 4.4 の分解同型" in rendered\n  assert "Proposition 5.15" in rendered\n  assert (\n    r"\\pi_{14}^{7} = "\n    r"\\mathbb{Z}/8\\{\\sigma\'\\}"\n    in rendered\n  )\n  assert (\n    r"\\left(α, \\beta\\right) \\mapsto "\n    r"Eα + \\sigma_{8}\\beta"\n    in rendered\n  )\n\n\ndef test_phase157_r20_repair53_r3_fragment_normalization_remains_active():\n  (\n    raw,\n    presentation,\n    prop44_step,\n  ) = _repair53_r3_data()\n\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  paragraphs = tuple(\n    paragraph.strip()\n    for paragraph in rendered.split(\n      "\\n\\n"\n    )\n    if paragraph.strip()\n  )\n\n  assert "である." not in paragraphs\n  assert "を得る." not in paragraphs\n'

RULE_NAME = (
  "Toda Proposition 5.15 sigma_8 n=8 "
  "Proposition 4.4 decomposition specialization"
)


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
        ast.FunctionDef,
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
      return start, end

  raise RuntimeError(
    "function not found: "
    + name
  )


def update_boundary_component_mapping(
  source: str,
) -> str:
  old = """    'Toda Proposition 4.4 nu_4 n=4 decomposition specialization': 'nu4_decomposition_isomorphism',
"""

  new = """    'Toda Proposition 4.4 nu_4 n=4 decomposition specialization': 'nu4_decomposition_isomorphism',
    'Toda Proposition 5.15 sigma_8 n=8 Proposition 4.4 decomposition specialization': 'nu4_decomposition_isomorphism',
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "component mapping anchor was not found exactly once"
    )

  return source.replace(
    old,
    new,
    1,
  )


def update_boundary_locator_mapping(
  source: str,
) -> str:
  old = """    'Toda Proposition 4.4 nu_4 n=4 decomposition specialization': 'Proposition 4.4',
"""

  new = """    'Toda Proposition 4.4 nu_4 n=4 decomposition specialization': 'Proposition 4.4',
    'Toda Proposition 5.15 sigma_8 n=8 Proposition 4.4 decomposition specialization': 'Proposition 4.4',
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "locator mapping anchor was not found exactly once"
    )

  return source.replace(
    old,
    new,
    1,
  )


def replace_extract_function(
  source: str,
) -> str:
  name = (
    "extract_toda_group_proof_step_literature_reference"
  )
  start, end = function_range(
    source,
    name,
  )

  return (
    source[
      :start
    ]
    + REPLACEMENT_EXTRACT.rstrip()
    + source[
      end:
    ]
  )


def main() -> int:
  for path in (
    BOUNDARY,
    REFERENCES,
  ):
    if not path.is_file():
      raise RuntimeError(
        "Run from repository root."
      )

  boundary_source = BOUNDARY.read_text(
    encoding="utf-8"
  )
  references_source = REFERENCES.read_text(
    encoding="utf-8"
  )

  if RULE_NAME in boundary_source:
    raise RuntimeError(
      "repair53-r3 boundary mapping already exists"
    )

  boundary_source = (
    update_boundary_component_mapping(
      boundary_source
    )
  )
  boundary_source = (
    update_boundary_locator_mapping(
      boundary_source
    )
  )
  references_source = (
    replace_extract_function(
      references_source
    )
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  combined = (
    boundary_source
    + "\n"
    + references_source
  )

  for token in forbidden:
    if token in combined:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    boundary_source,
    str(
      BOUNDARY
    ),
    "exec",
  )
  compile(
    references_source,
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

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_repair53_r3_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    BOUNDARY,
    backup / BOUNDARY.name,
  )
  shutil.copy2(
    REFERENCES,
    backup / REFERENCES.name,
  )

  BOUNDARY.write_text(
    boundary_source,
    encoding="utf-8",
    newline="\n",
  )
  REFERENCES.write_text(
    references_source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair53-r3 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed production file:",
    BOUNDARY,
  )
  print(
    "Changed production file:",
    REFERENCES,
  )
  print(
    "Added test:",
    TEST,
  )
  print("")
  print(
    "Import changes: none"
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
      combined.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
