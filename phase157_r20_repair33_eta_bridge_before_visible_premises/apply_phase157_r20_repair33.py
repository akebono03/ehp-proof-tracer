from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair33_eta_bridge_before_visible_premises.py"
)

NEW_FUNCTION = 'def insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def visible_indices(\n    proof_step: ProofStep,\n  ) -> tuple[\n    int,\n    ...,\n  ]:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return ()\n\n    target_key = match_key(\n      rendered\n    )\n\n    return tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n  for node in presentation.nodes:\n    consumer_step = node.proof_step\n\n    definition_steps = tuple(\n      premise\n      for premise in consumer_step.premises\n      if type(\n        premise.conclusion\n      ).__name__\n      == "TodaEtaFamilyDefinitionStatement"\n    )\n\n    if len(\n      definition_steps\n    ) < 2:\n      continue\n\n    ordered = tuple(\n      sorted(\n        definition_steps,\n        key=lambda step: (\n          step.conclusion.index\n        ),\n      )\n    )\n\n    consumer_indices = visible_indices(\n      consumer_step\n    )\n\n    if len(\n      consumer_indices\n    ) != 1:\n      continue\n\n    consumer_index = consumer_indices[\n      0\n    ]\n\n    visible_direct_premise_indices = tuple(\n      index\n      for premise in consumer_step.premises\n      if premise not in definition_steps\n      for premise_indices in (\n        visible_indices(\n          premise\n        ),\n      )\n      if len(\n        premise_indices\n      ) == 1\n      for index in premise_indices\n      if index < consumer_index\n    )\n\n    insertion_index = min(\n      (\n        consumer_index,\n        *visible_direct_premise_indices,\n      )\n    )\n\n    for lower_step, upper_step in zip(\n      ordered,\n      ordered[\n        1:\n      ],\n    ):\n      lower = lower_step.conclusion\n      upper = upper_step.conclusion\n\n      if (\n        not isinstance(\n          lower.index,\n          int,\n        )\n        or isinstance(\n          lower.index,\n          bool,\n        )\n        or not isinstance(\n          upper.index,\n          int,\n        )\n        or isinstance(\n          upper.index,\n          bool,\n        )\n        or upper.index\n        != lower.index + 1\n      ):\n        continue\n\n      bridge = (\n        "$"\n        + render_toda_expression_latex(\n          upper.element\n        )\n        + "=E"\n        + render_toda_expression_latex(\n          lower.element\n        )\n        + "$ である."\n      )\n\n      bridge_key = match_key(\n        bridge\n      )\n\n      if any(\n        match_key(\n          paragraph\n        )\n        == bridge_key\n        for paragraph in paragraphs\n      ):\n        continue\n\n      paragraphs.insert(\n        insertion_index,\n        bridge,\n      )\n      insertion_index += 1\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _body_pi6_3_repair33() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  return rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n\ndef test_phase157_r20_repair33_eta_bridge_precedes_visible_prop22_support():\n  body = _body_pi6_3_repair33()\n\n  eta6_definition = (\n    r"$\\eta_{6}=E\\eta_{5}$ である."\n  )\n  prop22 = (\n    "[R5]より, "\n    r"$H(\\alpha\\circ E\\beta) = "\n    r"H(\\alpha)\\circ E\\beta$."\n  )\n  hopf_value = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = "\n    r"\\eta_{5}^{2}\\tag{8}$."\n  )\n\n  assert eta6_definition in body\n  assert prop22 in body\n  assert hopf_value in body\n\n  assert body.index(\n    eta6_definition\n  ) < body.index(\n    prop22\n  )\n  assert body.index(\n    prop22\n  ) < body.index(\n    hopf_value\n  )\n\n\ndef test_phase157_r20_repair33_full_exactness_still_precedes_eta_bridge():\n  body = _body_pi6_3_repair33()\n\n  full_exactness = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  eta6_definition = (\n    r"$\\eta_{6}=E\\eta_{5}$ である."\n  )\n\n  assert full_exactness in body\n  assert eta6_definition in body\n  assert body.index(\n    full_exactness\n  ) < body.index(\n    eta6_definition\n  )\n'


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


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair33_backup_"
      + timestamp
    )
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
  source = replace_function(
    source,
    "insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges",
    NEW_FUNCTION,
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
    "Phase157-R20 repair33 applied."
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
