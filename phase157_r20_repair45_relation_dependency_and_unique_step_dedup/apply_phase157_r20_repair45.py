from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair45_relation_dependency_and_unique_step_dedup.py"
)

RELATION_FUNCTION = 'def order_toda_group_proof_narrative_visible_relation_dependencies(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            stripped = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def paragraph_index_for_step(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = (\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n\n    matching_indices = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph_match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matching_indices\n    ) != 1:\n      return None\n\n    return matching_indices[\n      0\n    ]\n\n  for node in presentation.nodes:\n    consumer_step = node.proof_step\n\n    if not isinstance(\n      consumer_step.conclusion,\n      Relation,\n    ):\n      continue\n\n    consumer_index = paragraph_index_for_step(\n      consumer_step\n    )\n\n    if consumer_index is None:\n      continue\n\n    relation_premises = tuple(\n      premise\n      for premise in consumer_step.premises\n      if isinstance(\n        premise.conclusion,\n        Relation,\n      )\n    )\n\n    for premise in relation_premises:\n      premise_index = paragraph_index_for_step(\n        premise\n      )\n      consumer_index = paragraph_index_for_step(\n        consumer_step\n      )\n\n      if (\n        premise_index is None\n        or consumer_index is None\n        or premise_index < consumer_index\n      ):\n        continue\n\n      paragraph = paragraphs.pop(\n        premise_index\n      )\n\n      consumer_index = paragraph_index_for_step(\n        consumer_step\n      )\n\n      if consumer_index is None:\n        paragraphs.insert(\n          premise_index,\n          paragraph,\n        )\n        continue\n\n      paragraphs.insert(\n        consumer_index,\n        paragraph,\n      )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
DEDUP_FUNCTION = 'def suppress_toda_group_proof_narrative_repeated_unique_step_statements(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  step_ids_by_key = {}\n\n  for node in presentation.nodes:\n    proof_step = node.proof_step\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      continue\n\n    key = (\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n\n    step_ids_by_key.setdefault(\n      key,\n      set(),\n    ).add(\n      id(\n        proof_step\n      )\n    )\n\n  unique_step_keys = {\n    key\n    for key, step_ids in step_ids_by_key.items()\n    if len(\n      step_ids\n    ) == 1\n  }\n\n  if not unique_step_keys:\n    return markdown\n\n  connector_prefixes = (\n    "以上より, ",\n    "したがって, ",\n    "これより, ",\n    "これらより, ",\n  )\n\n  retained = []\n  seen_unique_keys = set()\n\n  for paragraph in markdown.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n    comparable = stripped\n\n    for prefix in connector_prefixes:\n      if comparable.startswith(\n        prefix\n      ):\n        comparable = comparable[\n          len(\n            prefix\n          ):\n        ]\n        break\n\n    key = (\n      _phase157_r11_reference_statement_match_key(\n        comparable\n      )\n    )\n\n    if key not in unique_step_keys:\n      retained.append(\n        paragraph\n      )\n      continue\n\n    if key in seen_unique_keys:\n      continue\n\n    seen_unique_keys.add(\n      key\n    )\n    retained.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _body_pi6_3_repair45() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  return rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n\ndef test_phase157_r20_repair45_prop22_specialization_precedes_equation57_value():\n  body = _body_pi6_3_repair45()\n\n  prop22_specialization = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = "\n    r"H\\left(\\nu\'\\right)\\eta_{6}\\tag{7}$."\n  )\n  equation57_value = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = "\n    r"\\eta_{5}^{2}\\tag{8}$."\n  )\n\n  assert prop22_specialization in body\n  assert equation57_value in body\n  assert body.index(\n    prop22_specialization\n  ) < body.index(\n    equation57_value\n  )\n\n\ndef test_phase157_r20_repair45_prop22_specialization_stays_after_fixed_reference():\n  body = _body_pi6_3_repair45()\n\n  fixed_reference = (\n    "[R5]より, "\n    r"$H(\\alpha\\circ E\\beta) = "\n    r"H(\\alpha)\\circ E\\beta$."\n  )\n  prop22_specialization = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = "\n    r"H\\left(\\nu\'\\right)\\eta_{6}\\tag{7}$."\n  )\n\n  assert body.index(\n    fixed_reference\n  ) < body.index(\n    prop22_specialization\n  )\n\n\ndef test_phase157_r20_repair45_delta_zero_unique_step_is_rendered_once():\n  body = _body_pi6_3_repair45()\n\n  delta_zero = (\n    r"\\Delta: \\pi_{7}^{5} \\to "\n    r"\\pi_{5}^{2}$ は零写像である."\n  )\n\n  assert body.count(\n    delta_zero\n  ) == 1\n  assert (\n    "以上より, "\n    + "$"\n    + delta_zero\n    not in body\n  )\n\n\ndef test_phase157_r20_repair45_delta_zero_remains_before_injectivity():\n  body = _body_pi6_3_repair45()\n\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} \\to "\n    r"\\pi_{5}^{2}$ は零写像である."\n  )\n  injectivity = (\n    r"$E: \\pi_{5}^{2} \\to "\n    r"\\pi_{6}^{3}$ は単射である."\n  )\n\n  assert body.index(\n    delta_zero\n  ) < body.index(\n    injectivity\n  )\n\n\ndef test_phase157_r20_repair45_short_exact_order_remains_correct():\n  body = _body_pi6_3_repair45()\n\n  surjectivity = (\n    r"$H: \\pi_{6}^{3} \\to "\n    r"\\pi_{6}^{5}$ は全射である."\n  )\n  reason = (\n    "この完全性と, 左の写像が単射, "\n    "右の写像が全射であることより, "\n    "次の短完全列を得る."\n  )\n  short_exact = (\n    r"$0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    r"\\longrightarrow 0$."\n  )\n\n  assert body.index(\n    surjectivity\n  ) < body.index(\n    reason\n  )\n  assert body.index(\n    reason\n  ) < body.index(\n    short_exact\n  )\n'


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


def insert_functions(
  source: str,
) -> str:
  anchor_name = (
    "suppress_toda_group_proof_narrative_dangling_connectors"
  )
  _, end = function_range(
    source,
    anchor_name,
  )

  for name in (
    "order_toda_group_proof_narrative_visible_relation_dependencies",
    "suppress_toda_group_proof_narrative_repeated_unique_step_statements",
  ):
    if (
      "def "
      + name
      + "("
      in source
    ):
      raise RuntimeError(
        "repair45 function already exists: "
        + name
      )

  addition = (
    "\n\n\n"
    + RELATION_FUNCTION.rstrip()
    + "\n\n\n"
    + DEDUP_FUNCTION.rstrip()
  )

  return (
    source[:end]
    + addition
    + source[end:]
  )


def update_pipeline(
  source: str,
) -> str:
  old = """  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      rendered
    )
  )

  generic_used_step_ids = (
"""

  new = """  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      rendered
    )
  )
  rendered = (
    order_toda_group_proof_narrative_visible_relation_dependencies(
      presentation,
      rendered,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_repeated_unique_step_statements(
      presentation,
      rendered,
    )
  )

  generic_used_step_ids = (
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "repair45 pipeline anchor was not found exactly once"
    )

  return source.replace(
    old,
    new,
    1,
  )


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_repair45_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup / TARGET.name,
  )

  source = TARGET.read_text(
    encoding="utf-8"
  )
  source = insert_functions(
    source
  )
  source = update_pipeline(
    source
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
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
      TARGET
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

  TARGET.write_text(
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
    "Phase157-R20 repair45 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed production file:",
    TARGET,
  )
  print(
    "Added test:",
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
