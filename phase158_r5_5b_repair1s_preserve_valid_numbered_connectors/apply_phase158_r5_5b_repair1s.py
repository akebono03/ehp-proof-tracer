from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair43_dangling_connector_cleanup.py"
)

NEW_FUNCTION = 'def suppress_toda_group_proof_narrative_dangling_connectors(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  standalone_connectors = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  def numbered_connector_numbers(\n    line: str,\n  ) -> tuple[\n    int,\n    ...,\n  ] | None:\n    stripped = line.strip()\n\n    if (\n      not stripped.startswith(\n        "("\n      )\n      or not stripped.endswith(\n        "より,"\n      )\n      or "$" in stripped\n      or "[R" in stripped\n    ):\n      return None\n\n    relation_text = stripped[\n      : -len(\n        "より,"\n      )\n    ].strip()\n    parts = tuple(\n      part.strip()\n      for part in relation_text.split(\n        " と "\n      )\n    )\n\n    if not parts:\n      return None\n\n    numbers = []\n\n    for part in parts:\n      if (\n        len(\n          part\n        ) < 3\n        or not part.startswith(\n          "("\n        )\n        or not part.endswith(\n          ")"\n        )\n      ):\n        return None\n\n      number_text = part[\n        1:-1\n      ]\n\n      if not number_text.isdigit():\n        return None\n\n      numbers.append(\n        int(\n          number_text\n        )\n      )\n\n    return tuple(\n      numbers\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  retained_paragraphs = []\n\n  for paragraph_index, paragraph in enumerate(\n    paragraphs\n  ):\n    lines = paragraph.splitlines()\n\n    while lines:\n      stripped = lines[\n        -1\n      ].strip()\n\n      if stripped in standalone_connectors:\n        lines.pop()\n        continue\n\n      connector_numbers = (\n        numbered_connector_numbers(\n          stripped\n        )\n      )\n\n      if connector_numbers is None:\n        break\n\n      previous_text = "\\n\\n".join(\n        paragraphs[\n          :paragraph_index\n        ]\n      )\n      referenced_tags_exist = all(\n        (\n          r"\\tag{"\n          + str(\n            number\n          )\n          + "}"\n        )\n        in previous_text\n        for number in connector_numbers\n      )\n\n      next_paragraph = next(\n        (\n          candidate.strip()\n          for candidate in paragraphs[\n            paragraph_index + 1:\n          ]\n          if candidate.strip()\n        ),\n        "",\n      )\n      has_following_derivation = (\n        "$" in next_paragraph\n      )\n\n      if (\n        referenced_tags_exist\n        and has_following_derivation\n      ):\n        break\n\n      lines.pop()\n\n    if not lines:\n      continue\n\n    normalized = "\\n".join(\n      lines\n    )\n    stripped = normalized.lstrip()\n\n    for connector in standalone_connectors:\n      prefix = (\n        connector\n        + " "\n      )\n\n      if (\n        stripped.startswith(\n          prefix\n          + "[R"\n        )\n      ):\n        leading = len(\n          normalized\n        ) - len(\n          stripped\n        )\n        normalized = (\n          normalized[\n            :leading\n          ]\n          + stripped[\n            len(\n              prefix\n            ):\n          ]\n        )\n        break\n\n    if normalized.strip():\n      retained_paragraphs.append(\n        normalized\n      )\n\n  return "\\n\\n".join(\n    retained_paragraphs\n  )\n'
NEW_TEST_IMPORT = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  suppress_toda_group_proof_narrative_dangling_connectors,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n'
NEW_TEST_FUNCTIONS = 'def test_phase157_r20_repair43_has_no_dangling_connector_paragraphs_or_lines():\n  body = _body_pi6_3_repair43()\n  standalone_connectors = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  for paragraph in body.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n\n    assert stripped not in standalone_connectors\n\n    lines = tuple(\n      line.strip()\n      for line in paragraph.splitlines()\n      if line.strip()\n    )\n\n    if not lines:\n      continue\n\n    assert lines[\n      -1\n    ] not in standalone_connectors\n\n\ndef test_phase157_r20_repair43_keeps_valid_numbered_derivation_connector():\n  markdown = "\\n\\n".join(\n    (\n      r"$a=b\\tag{4}$",\n      r"$b=c\\tag{7}$",\n      "(4) と (7) より,",\n      r"$a=c$",\n    )\n  )\n\n  rendered = (\n    suppress_toda_group_proof_narrative_dangling_connectors(\n      markdown\n    )\n  )\n\n  assert "(4) と (7) より," in rendered\n\n\ndef test_phase157_r20_repair43_removes_unreferenced_numbered_connector():\n  markdown = "\\n\\n".join(\n    (\n      r"$a=b$",\n      "(4) と (7) より,",\n      r"$a=c$",\n    )\n  )\n\n  rendered = (\n    suppress_toda_group_proof_narrative_dangling_connectors(\n      markdown\n    )\n  )\n\n  assert "(4) と (7) より," not in rendered\n'


def function_range(
  source: str,
  function_name: str,
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
      and node.name == function_name
    ):
      start = sum(
        len(
          line
        )
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(
          line
        )
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
    + function_name
  )


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    function_name,
  )
  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n\n"
    + source[
      end:
    ].lstrip(
      "\n"
    )
  )


def replace_import_section(
  source: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )
  import_nodes = tuple(
    node
    for node in tree.body
    if isinstance(
      node,
      (
        ast.Import,
        ast.ImportFrom,
      ),
    )
  )

  if not import_nodes:
    raise RuntimeError(
      "test import section not found"
    )

  lines = source.splitlines(
    keepends=True
  )
  start_line = import_nodes[
    0
  ].lineno
  end_line = import_nodes[
    -1
  ].end_lineno
  start = sum(
    len(
      line
    )
    for line in lines[
      :start_line - 1
    ]
  )
  end = sum(
    len(
      line
    )
    for line in lines[
      :end_line
    ]
  )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n\n"
    + source[
      end:
    ].lstrip(
      "\n"
    )
  )


def main() -> int:
  for path in (
    PRODUCTION,
    TEST,
  ):
    if not path.exists():
      raise RuntimeError(
        "missing expected file: "
        + str(
          path
        )
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase158_r5_5b_repair1s_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    PRODUCTION,
    backup_dir
    / PRODUCTION.name,
  )
  shutil.copy2(
    TEST,
    backup_dir
    / TEST.name,
  )

  production_source = PRODUCTION.read_text(
    encoding="utf-8"
  )
  production_updated = replace_function(
    production_source,
    "suppress_toda_group_proof_narrative_dangling_connectors",
    NEW_FUNCTION,
  )
  ast.parse(
    production_updated
  )
  PRODUCTION.write_text(
    production_updated,
    encoding="utf-8",
    newline="\n",
  )

  test_source = TEST.read_text(
    encoding="utf-8"
  )
  test_updated = replace_import_section(
    test_source,
    NEW_TEST_IMPORT,
  )
  test_updated = replace_function(
    test_updated,
    "test_phase157_r20_repair43_has_no_dangling_connector_paragraphs_or_lines",
    NEW_TEST_FUNCTIONS,
  )
  ast.parse(
    test_updated
  )
  TEST.write_text(
    test_updated,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 158-R5-5b repair1s applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Production changed: "
    + PRODUCTION.name
  )
  print(
    "Test changed: "
    + TEST.name
  )
  print(
    "Production import changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
