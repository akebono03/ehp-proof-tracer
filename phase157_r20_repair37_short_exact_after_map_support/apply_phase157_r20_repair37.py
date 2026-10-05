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
  / "test_phase157_r20_repair37_short_exact_after_map_support.py"
)

NEW_FUNCTION = 'def order_toda_group_proof_narrative_short_exact_support(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            stripped = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def unique_index_for_rendered(\n    rendered: str,\n  ) -> int | None:\n    target_key = match_key(\n      rendered\n    )\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  def map_support_step(\n    source_group,\n    target_group,\n    map_name: str,\n    property_prose: str,\n  ) -> ProofStep | None:\n    matches = []\n\n    for node in presentation.nodes:\n      proof_step = node.proof_step\n      statement = proof_step.conclusion\n      group_map = getattr(\n        statement,\n        "map",\n        None,\n      )\n\n      if group_map is None:\n        continue\n\n      if (\n        getattr(\n          group_map,\n          "source_group",\n          None,\n        )\n        != source_group\n        or getattr(\n          group_map,\n          "target_group",\n          None,\n        )\n        != target_group\n        or _toda_group_proof_narrative_map_name_latex(\n          group_map\n        )\n        != map_name\n      ):\n        continue\n\n      rendered = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if (\n        not rendered\n        or property_prose not in rendered\n      ):\n        continue\n\n      matches.append(\n        proof_step\n      )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  for node in presentation.nodes:\n    exactness_step = node.proof_step\n    short_exact_latex = (\n      _generic_short_exact_sequence_latex(\n        presentation,\n        exactness_step,\n      )\n    )\n\n    if short_exact_latex is None:\n      continue\n\n    reason = (\n      _generic_short_exact_sequence_reason_prose(\n        presentation,\n        exactness_step,\n      )\n    )\n\n    if reason is None:\n      continue\n\n    window = getattr(\n      exactness_step.conclusion,\n      "window",\n      None,\n    )\n\n    if window is None:\n      continue\n\n    first_map_name = (\n      _toda_group_proof_narrative_map_name_latex(\n        window.first_map\n      )\n    )\n    second_map_name = (\n      _toda_group_proof_narrative_map_name_latex(\n        window.second_map\n      )\n    )\n\n    if (\n      first_map_name is None\n      or second_map_name is None\n    ):\n      continue\n\n    injective_step = map_support_step(\n      window.source_term,\n      window.middle_term,\n      first_map_name,\n      "は単射である.",\n    )\n    surjective_step = map_support_step(\n      window.middle_term,\n      window.target_term,\n      second_map_name,\n      "は全射である.",\n    )\n\n    if (\n      injective_step is None\n      or surjective_step is None\n    ):\n      continue\n\n    injective_rendered = (\n      _render_generic_narrative_step(\n        injective_step\n      )\n    )\n    surjective_rendered = (\n      _render_generic_narrative_step(\n        surjective_step\n      )\n    )\n\n    if (\n      not injective_rendered\n      or not surjective_rendered\n    ):\n      continue\n\n    injective_index = unique_index_for_rendered(\n      injective_rendered\n    )\n    surjective_index = unique_index_for_rendered(\n      surjective_rendered\n    )\n\n    short_exact_paragraph = (\n      "$"\n      + short_exact_latex\n      + "$"\n    )\n    reason_index = unique_index_for_rendered(\n      reason\n    )\n    sequence_index = unique_index_for_rendered(\n      short_exact_paragraph\n    )\n\n    if (\n      injective_index is None\n      or surjective_index is None\n      or reason_index is None\n      or sequence_index is None\n    ):\n      continue\n\n    support_anchor = max(\n      injective_index,\n      surjective_index,\n    )\n\n    if (\n      reason_index > support_anchor\n      and sequence_index > support_anchor\n    ):\n      continue\n\n    moved = [\n      paragraphs[\n        reason_index\n      ],\n      paragraphs[\n        sequence_index\n      ],\n    ]\n\n    removal_indices = sorted(\n      {\n        reason_index,\n        sequence_index,\n      },\n      reverse=True,\n    )\n\n    for index in removal_indices:\n      paragraphs.pop(\n        index\n      )\n\n    support_anchor = unique_index_for_rendered(\n      surjective_rendered\n      if surjective_index >= injective_index\n      else injective_rendered\n    )\n\n    if support_anchor is None:\n      continue\n\n    insertion_index = (\n      support_anchor + 1\n    )\n    paragraphs[\n      insertion_index:\n      insertion_index\n    ] = moved\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _body_pi6_3_repair37() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  return rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n\ndef test_phase157_r20_repair37_short_exact_follows_surjectivity():\n  body = _body_pi6_3_repair37()\n\n  surjectivity = (\n    r"$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ "\n    "は全射である."\n  )\n  reason = (\n    "この完全性と, 左の写像が単射, "\n    "右の写像が全射であることより, "\n    "次の短完全列を得る."\n  )\n  short_exact = (\n    r"$0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    r"\\longrightarrow 0$."\n  )\n\n  assert surjectivity in body\n  assert reason in body\n  assert short_exact in body\n\n  assert body.index(\n    surjectivity\n  ) < body.index(\n    reason\n  )\n  assert body.index(\n    reason\n  ) < body.index(\n    short_exact\n  )\n\n\ndef test_phase157_r20_repair37_short_exact_follows_injectivity():\n  body = _body_pi6_3_repair37()\n\n  injectivity = (\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "\n    "は単射である."\n  )\n  short_exact = (\n    r"$0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    r"\\longrightarrow 0$."\n  )\n\n  assert body.index(\n    injectivity\n  ) < body.index(\n    short_exact\n  )\n'


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


def ensure_imports(
  source: str,
) -> str:
  anchor = (
    "from toda_group_proof_generic_narrative_renderer import (\n"
  )

  start = source.find(
    anchor
  )

  if start < 0:
    raise RuntimeError(
      "generic narrative renderer import block not found"
    )

  end = source.find(
    ")\n",
    start,
  )

  if end < 0:
    raise RuntimeError(
      "generic narrative renderer import block end not found"
    )

  end += len(
    ")\n"
  )
  block = source[
    start:
    end
  ]

  additions = (
    "  _generic_short_exact_sequence_latex,\n",
    "  _generic_short_exact_sequence_reason_prose,\n",
  )

  for addition in additions:
    if addition not in block:
      insert_at = block.find(
        "  _normalize_generic_eta_family_latex,\n"
      )

      if insert_at < 0:
        raise RuntimeError(
          "generic import insertion anchor not found"
        )

      block = (
        block[:insert_at]
        + addition
        + block[
          insert_at:
        ]
      )

  return (
    source[:start]
    + block
    + source[end:]
  )


def insert_function(
  source: str,
) -> str:
  anchor_name = (
    "order_toda_group_proof_narrative_surjectivity_support"
  )
  _, end = function_range(
    source,
    anchor_name,
  )

  if (
    "def order_toda_group_proof_narrative_short_exact_support("
    in source
  ):
    raise RuntimeError(
      "repair37 function already exists"
    )

  return (
    source[:end]
    + "\n\n\n"
    + NEW_FUNCTION.rstrip()
    + source[end:]
  )


def update_pipeline(
  source: str,
) -> str:
  old = """  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
"""

  new = old + """  rendered = (
    order_toda_group_proof_narrative_short_exact_support(
      presentation,
      rendered,
    )
  )
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "surjectivity ordering pipeline call "
      "was not found exactly once"
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
  backup = (
    ROOT
    / (
      "phase157_r20_repair37_backup_"
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
  source = ensure_imports(
    source
  )
  source = insert_function(
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
    "Phase157-R20 repair37 applied."
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
