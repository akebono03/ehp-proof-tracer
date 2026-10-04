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
  / "test_phase157_r20_repair42_repeated_reference_restatements.py"
)

NEW_FUNCTION = 'def suppress_toda_group_proof_narrative_repeated_reference_restatements(\n  body_markdown: str,\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n) -> str:\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  reference_keys = set()\n\n  for reference_number, statement_lines in (\n    statement_lines_by_reference_number.items()\n  ):\n    if (\n      isinstance(\n        reference_number,\n        bool,\n      )\n      or not isinstance(\n        reference_number,\n        int,\n      )\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number keys "\n        "must be integers"\n      )\n\n    if not isinstance(\n      statement_lines,\n      tuple,\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number values "\n        "must be tuples"\n      )\n\n    for statement_line in statement_lines:\n      if not isinstance(\n        statement_line,\n        str,\n      ):\n        raise TypeError(\n          "statement_lines_by_reference_number values "\n          "must contain only strings"\n        )\n\n      if not statement_line:\n        continue\n\n      reference_keys.add(\n        _phase157_r11_reference_statement_match_key(\n          statement_line\n        )\n      )\n\n  if not reference_keys:\n    return body_markdown\n\n  retained = []\n  seen_reference_keys = set()\n\n  for paragraph in body_markdown.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n    comparable = stripped\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            comparable = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    key = (\n      _phase157_r11_reference_statement_match_key(\n        comparable\n      )\n    )\n\n    if key not in reference_keys:\n      retained.append(\n        paragraph\n      )\n      continue\n\n    if key in seen_reference_keys:\n      continue\n\n    seen_reference_keys.add(\n      key\n    )\n    retained.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _body_pi6_3_repair42() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  return rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n\ndef test_phase157_r20_repair42_hopf_fixed_statement_is_not_repeated():\n  body = _body_pi6_3_repair42()\n\n  assert (\n    body.count(\n      r"H\\left(\\nu\'\\right) = \\eta_{5}"\n    )\n    == 1\n  )\n  assert (\n    "[R2]より, "\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in body\n  )\n\n\ndef test_phase157_r20_repair42_double_nu_fixed_statement_is_not_repeated():\n  body = _body_pi6_3_repair42()\n\n  assert (\n    body.count(\n      "[R2]より, "\n      r"$2\\nu\' = \\eta_{3}^{3}"\n    )\n    == 1\n  )\n  assert (\n    r"$\\operatorname{ord}(\\eta_{3}^{3})=2$ "\n    r"かつ $2\\nu\'=\\eta_{3}^{3}$ より, "\n    r"$4\\nu\'=0$ かつ $2\\nu\'\\neq0$ である."\n    in body\n  )\n\n\ndef test_phase157_r20_repair42_short_exact_order_remains_correct():\n  body = _body_pi6_3_repair42()\n\n  surjectivity = (\n    r"$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ "\n    "は全射である."\n  )\n  reason = (\n    "この完全性と, 左の写像が単射, "\n    "右の写像が全射であることより, "\n    "次の短完全列を得る."\n  )\n\n  assert body.index(\n    surjectivity\n  ) < body.index(\n    reason\n  )\n'


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
    "suppress_toda_group_proof_narrative_reference_body_restatements"
  )
  _, end = function_range(
    source,
    anchor_name,
  )

  if (
    "def suppress_toda_group_proof_narrative_repeated_reference_restatements("
    in source
  ):
    raise RuntimeError(
      "repair42 function already exists"
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
    order_toda_group_proof_narrative_short_exact_support(
      presentation,
      rendered,
    )
  )

  generic_used_step_ids = (
"""

  new = """  rendered = (
    order_toda_group_proof_narrative_short_exact_support(
      presentation,
      rendered,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_repeated_reference_restatements(
      rendered,
      statement_lines_by_reference_number,
    )
  )

  generic_used_step_ids = (
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "repair42 pipeline anchor was not found exactly once"
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
    "phase157_r20_repair42_backup_"
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
    str(TARGET),
    "exec",
  )
  compile(
    TEST_SOURCE,
    str(TEST),
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
    "Phase157-R20 repair42 applied."
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
