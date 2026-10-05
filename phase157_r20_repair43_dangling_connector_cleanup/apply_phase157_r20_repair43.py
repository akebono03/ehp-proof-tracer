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
  / "test_phase157_r20_repair43_dangling_connector_cleanup.py"
)

NEW_FUNCTION = 'def suppress_toda_group_proof_narrative_dangling_connectors(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  standalone_connectors = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  def is_dangling_connector_line(\n    line: str,\n  ) -> bool:\n    stripped = line.strip()\n\n    if stripped in standalone_connectors:\n      return True\n\n    if (\n      stripped.startswith(\n        "("\n      )\n      and stripped.endswith(\n        "より,"\n      )\n      and ") と (" in stripped\n      and "$" not in stripped\n      and "[R" not in stripped\n    ):\n      return True\n\n    return False\n\n  retained_paragraphs = []\n\n  for paragraph in markdown.split(\n    "\\n\\n"\n  ):\n    lines = paragraph.splitlines()\n\n    while (\n      lines\n      and is_dangling_connector_line(\n        lines[\n          -1\n        ]\n      )\n    ):\n      lines.pop()\n\n    if not lines:\n      continue\n\n    normalized = "\\n".join(\n      lines\n    )\n    stripped = normalized.lstrip()\n\n    for connector in standalone_connectors:\n      prefix = (\n        connector\n        + " "\n      )\n\n      if (\n        stripped.startswith(\n          prefix\n          + "[R"\n        )\n      ):\n        leading = len(\n          normalized\n        ) - len(\n          stripped\n        )\n        normalized = (\n          normalized[\n            :leading\n          ]\n          + stripped[\n            len(\n              prefix\n            ):\n          ]\n        )\n        break\n\n    if normalized.strip():\n      retained_paragraphs.append(\n        normalized\n      )\n\n  return "\\n\\n".join(\n    retained_paragraphs\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _body_pi6_3_repair43() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  return rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n\ndef test_phase157_r20_repair43_has_no_dangling_connector_paragraphs_or_lines():\n  body = _body_pi6_3_repair43()\n  standalone_connectors = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  for paragraph in body.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n\n    assert stripped not in standalone_connectors\n\n    lines = tuple(\n      line.strip()\n      for line in paragraph.splitlines()\n      if line.strip()\n    )\n\n    if not lines:\n      continue\n\n    assert lines[\n      -1\n    ] not in standalone_connectors\n\n    assert not (\n      lines[\n        -1\n      ].startswith(\n        "("\n      )\n      and lines[\n        -1\n      ].endswith(\n        "より,"\n      )\n      and ") と (" in lines[\n        -1\n      ]\n    )\n\n\ndef test_phase157_r20_repair43_reference_marker_does_not_keep_redundant_connector_prefix():\n  body = _body_pi6_3_repair43()\n\n  assert (\n    "以上より, [R"\n    not in body\n  )\n  assert (\n    "したがって, [R"\n    not in body\n  )\n  assert (\n    "これらより, [R"\n    not in body\n  )\n\n\ndef test_phase157_r20_repair43_required_reason_sentences_remain():\n  body = _body_pi6_3_repair43()\n\n  assert (\n    "完全性より, "\n    r"$\\ker \\Delta=\\operatorname{Im}H="\n    r"\\pi_{7}^{5}$ である."\n    in body\n  )\n  assert (\n    "この完全性と $Δ=0$ より, "\n    r"$\\ker E=\\operatorname{Im}Δ=0$ である."\n    in body\n  )\n  assert (\n    r"$\\operatorname{ord}(\\eta_{3}^{3})=2$ "\n    r"かつ $2\\nu\'=\\eta_{3}^{3}$ より, "\n    r"$4\\nu\'=0$ かつ $2\\nu\'\\neq0$ である."\n    in body\n  )\n'


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


def insert_function(
  source: str,
) -> str:
  anchor_name = (
    "normalize_toda_group_proof_narrative_connectors"
  )
  _, end = function_range(
    source,
    anchor_name,
  )

  if (
    "def suppress_toda_group_proof_narrative_dangling_connectors("
    in source
  ):
    raise RuntimeError(
      "repair43 function already exists"
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
    suppress_toda_group_proof_narrative_repeated_reference_restatements(
      rendered,
      statement_lines_by_reference_number,
    )
  )

  generic_used_step_ids = (
"""

  new = """  rendered = (
    suppress_toda_group_proof_narrative_repeated_reference_restatements(
      rendered,
      statement_lines_by_reference_number,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      rendered
    )
  )

  generic_used_step_ids = (
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "repair43 pipeline anchor was not found exactly once"
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
    "phase157_r20_repair43_backup_"
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
    "Phase157-R20 repair43 applied."
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
