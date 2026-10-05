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
  / "test_phase157_r20_repair32_exactness_intro_anchor.py"
)

NEW_FUNCTION = 'def merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  exactness_steps = tuple(\n    node.proof_step\n    for node in presentation.nodes\n    if classify_toda_proof_step_role(\n      node.proof_step\n    )\n    is TodaProofDependencyRole.EHP_EXACTNESS\n  )\n\n  for left_step in exactness_steps:\n    left_window = getattr(\n      left_step.conclusion,\n      "window",\n      None,\n    )\n\n    if left_window is None:\n      continue\n\n    for right_step in exactness_steps:\n      if right_step is left_step:\n        continue\n\n      right_window = getattr(\n        right_step.conclusion,\n        "window",\n        None,\n      )\n\n      if right_window is None:\n        continue\n\n      if not (\n        left_window.middle_term\n        == right_window.source_term\n        and left_window.target_term\n        == right_window.middle_term\n        and _toda_group_proof_narrative_map_name_latex(\n          left_window.second_map\n        )\n        == _toda_group_proof_narrative_map_name_latex(\n          right_window.first_map\n        )\n      ):\n        continue\n\n      left_line = (\n        _render_generic_narrative_step(\n          left_step\n        )\n      )\n      right_line = (\n        _render_generic_narrative_step(\n          right_step\n        )\n      )\n\n      left_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == left_line.strip()\n        ),\n        None,\n      )\n      right_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == right_line.strip()\n        ),\n        None,\n      )\n\n      if (\n        left_index is None\n        or right_index is None\n      ):\n        continue\n\n      first_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          left_window.first_map\n        )\n      )\n      second_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          left_window.second_map\n        )\n      )\n      third_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          right_window.second_map\n        )\n      )\n\n      if None in (\n        first_map,\n        second_map,\n        third_map,\n      ):\n        continue\n\n      bare_sequence = (\n        "$"\n        + render_toda_primary_group_latex(\n          left_window.source_term\n        )\n        + r" \\xrightarrow{"\n        + first_map\n        + "} "\n        + render_toda_primary_group_latex(\n          left_window.middle_term\n        )\n        + r" \\xrightarrow{"\n        + second_map\n        + "} "\n        + render_toda_primary_group_latex(\n          left_window.target_term\n        )\n        + r" \\xrightarrow{"\n        + third_map\n        + "} "\n        + render_toda_primary_group_latex(\n          right_window.target_term\n        )\n        + "$"\n      )\n      merged = (\n        bare_sequence\n        + " は完全である."\n      )\n\n      bare_indices = tuple(\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if paragraph.strip().rstrip(\n          "."\n        )\n        == bare_sequence\n      )\n\n      introduction_index = (\n        bare_indices[\n          0\n        ]\n        if len(\n          bare_indices\n        ) == 1\n        else None\n      )\n\n      removal_indices = {\n        left_index,\n        right_index,\n      }\n\n      if introduction_index is not None:\n        removal_indices.add(\n          introduction_index\n        )\n        insertion_index = (\n          introduction_index\n        )\n      else:\n        insertion_index = min(\n          left_index,\n          right_index,\n        )\n\n      for index in sorted(\n        removal_indices,\n        reverse=True,\n      ):\n        paragraphs.pop(\n          index\n        )\n\n      removed_before_insertion = sum(\n        1\n        for index in removal_indices\n        if index < insertion_index\n      )\n      insertion_index -= (\n        removed_before_insertion\n      )\n\n      paragraphs.insert(\n        insertion_index,\n        merged,\n      )\n\n      return "\\n\\n".join(\n        paragraphs\n      )\n\n  return markdown\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _body_pi6_3_repair32() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  return rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n\ndef test_phase157_r20_repair32_full_exactness_uses_intro_sequence_anchor():\n  body = _body_pi6_3_repair32()\n\n  full_exactness = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  eta6_definition = (\n    r"$\\eta_{6}=E\\eta_{5}$ である."\n  )\n\n  assert full_exactness in body\n  assert eta6_definition in body\n  assert body.index(\n    full_exactness\n  ) < body.index(\n    eta6_definition\n  )\n\n\ndef test_phase157_r20_repair32_bare_duplicate_full_sequence_is_removed():\n  body = _body_pi6_3_repair32()\n\n  bare_sequence = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$."\n  )\n  full_exactness = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n\n  assert bare_sequence not in body\n  assert body.count(\n    full_exactness\n  ) == 1\n'


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
      "phase157_r20_repair32_backup_"
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
    "merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows",
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
    "Phase157-R20 repair32 applied."
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
