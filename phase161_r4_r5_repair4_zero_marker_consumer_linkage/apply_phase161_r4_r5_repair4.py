from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_repair4_zero_marker_consumer_linkage.py"
)

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

NEW_FUNCTION = 'def link_toda_group_proof_narrative_reference_body_consumers(\n  presentation: TodaGroupProofPresentation,\n  body_markdown: str,\n  reference_entries,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  source_steps_by_number = (\n    _phase154_r5_reference_source_steps_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  lines = body_markdown.splitlines()\n\n  for reference_number, source_steps in (\n    source_steps_by_number.items()\n  ):\n    marker = (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]"\n    )\n\n    current_body = "\\n".join(\n      lines\n    )\n    consumer_line = (\n      _phase154_r5_unique_visible_non_root_consumer_line(\n        presentation,\n        source_steps,\n        current_body,\n      )\n    )\n\n    if consumer_line is None:\n      continue\n\n    marker_indices = tuple(\n      index\n      for index, line in enumerate(\n        lines\n      )\n      if marker in line\n    )\n\n    if len(\n      marker_indices\n    ) > 1:\n      continue\n\n    consumer_indices = tuple(\n      index\n      for index, line in enumerate(\n        lines\n      )\n      if (\n        consumer_line in line\n        and (\n          not marker_indices\n          or index != marker_indices[0]\n        )\n      )\n    )\n\n    if len(\n      consumer_indices\n    ) != 1:\n      continue\n\n    consumer_index = consumer_indices[\n      0\n    ]\n\n    if not marker_indices:\n      consumer_text = lines[\n        consumer_index\n      ]\n\n      if marker in consumer_text:\n        continue\n\n      lines[\n        consumer_index\n      ] = (\n        marker\n        + "より, "\n        + consumer_text\n      )\n      continue\n\n    marker_index = marker_indices[\n      0\n    ]\n    marker_line = lines[\n      marker_index\n    ]\n\n    if consumer_index <= marker_index:\n      continue\n\n    legacy_marker_only = (\n      marker_line\n      .rstrip()\n      .endswith(\n        marker\n        + "を用いる。"\n      )\n    )\n\n    rendered_source_lines = tuple(\n      rendered\n      for source_step in source_steps\n      for rendered in (\n        _render_generic_narrative_step(\n          source_step\n        ),\n      )\n      if rendered\n    )\n\n    self_reference_marker = (\n      not legacy_marker_only\n      and any(\n        rendered_source in marker_line\n        for rendered_source in rendered_source_lines\n      )\n      and consumer_line not in marker_line\n    )\n\n    if not (\n      legacy_marker_only\n      or self_reference_marker\n    ):\n      continue\n\n    lines[\n      marker_index\n    ] = (\n      marker\n      + "より, "\n      + consumer_line\n    )\n    del lines[\n      consumer_index\n    ]\n\n  compacted_lines = []\n  previous_blank = False\n\n  for line in lines:\n    is_blank = not line.strip()\n\n    if is_blank and previous_blank:\n      continue\n\n    compacted_lines.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted_lines\n  ).strip()\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_phase161_r4_r5_repair4_pi4_2() -> str:\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=3,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase161_r4_r5_repair4_links_zero_marker_reference_to_pi4_3():\n  rendered = (\n    _render_phase161_r4_r5_repair4_pi4_2()\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  prop51_number = next(\n    number\n    for number in range(\n      1,\n      5,\n    )\n    if (\n      f"**[R{number}] Proposition 5.1.**"\n      in reference\n    )\n  )\n  marker = (\n    "[R"\n    + str(\n      prop51_number\n    )\n    + "]"\n  )\n\n  assert (\n    r"\\pi_{n + 1}^{n} = "\n    r"\\mathbb{Z}/2\\{\\eta_{n}\\}"\n    in reference\n  )\n  assert (\n    r"\\pi_{n + 1}^{n} = "\n    r"\\mathbb{Z}/2\\{\\eta_{n}\\}"\n    not in body\n  )\n\n  pi4_3_paragraph = next(\n    paragraph\n    for paragraph in body.split(\n      "\\n\\n"\n    )\n    if (\n      r"\\pi_{4}^{3} = "\n      r"\\mathbb{Z}/2\\{\\eta_{3}\\}"\n      in paragraph\n    )\n  )\n\n  assert marker in pi4_3_paragraph\n  assert (\n    pi4_3_paragraph.count(\n      marker\n    )\n    == 1\n  )\n\n\ndef test_phase161_r4_r5_repair4_keeps_pi4_2_specialization_contract():\n  rendered = (\n    _render_phase161_r4_r5_repair4_pi4_2()\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "(5.2)" in reference\n  assert (\n    r"\\eta_{2}\\circ -: "\n    r"\\pi_{i}^{3} \\to \\pi_{i}^{2}"\n    in reference\n  )\n\n  assert "$i=4$" in body\n  assert (\n    r"\\eta_{2}\\circ -: "\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}"\n    in body\n  )\n  assert (\n    r"\\eta_{3} \\mapsto "\n    r"\\eta_{2}\\eta_{3}"\n    in body\n  )\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in body\n  )\n  assert "□" in body\n'


def _functions(
  source: str,
):
  tree = ast.parse(
    source
  )

  return {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }


def _replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing function: {function_name}"
    )

  node = functions[
    function_name
  ]
  lines = source.splitlines(
    keepends=True
  )
  replacement_lines = [
    line + "\n"
    for line in replacement.rstrip(
      "\n"
    ).split(
      "\n"
    )
  ]

  return "".join(
    lines[
      :node.lineno - 1
    ]
    + replacement_lines
    + lines[
      node.end_lineno:
    ]
  )


def _extract_function(
  source: str,
  function_name: str,
) -> str:
  node = _functions(
    source
  )[
    function_name
  ]
  lines = source.splitlines()

  return "\n".join(
    lines[
      node.lineno - 1:
      node.end_lineno
    ]
  ) + "\n"


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )

  required = (
    "_phase154_r5_reference_source_steps_by_number",
    "_phase154_r5_unique_visible_non_root_consumer_line",
    "link_toda_group_proof_narrative_reference_body_consumers",
  )

  functions = _functions(
    source
  )

  for function_name in required:
    if function_name not in functions:
      raise RuntimeError(
        f"Required function missing: {function_name}"
      )

  updated = _replace_function(
    source,
    "link_toda_group_proof_narrative_reference_body_consumers",
    NEW_FUNCTION,
  )

  ast.parse(
    updated
  )
  ast.parse(
    TEST_SOURCE
  )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP_DIR / TARGET.name,
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    OUTPUT_DIR
    / "link_toda_group_proof_narrative_reference_body_consumers.py.txt"
  ).write_text(
    _extract_function(
      updated,
      "link_toda_group_proof_narrative_reference_body_consumers",
    ),
    encoding="utf-8",
    newline="\n",
  )
  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_repair4_zero_marker_consumer_linkage.py.txt"
  ).write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    TARGET,
  )
  print(
    "Wrote:",
    TEST,
  )
  print(
    "Production imports changed: NONE"
  )
  print(
    "Full changed function and test written to output/."
  )


if __name__ == "__main__":
  main()
