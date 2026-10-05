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
  / "test_phase157_r20_repair30_final_reflexive_suppression.py"
)

NEW_FUNCTION = 'def suppress_toda_group_proof_narrative_reflexive_equalities(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  reflexive_keys = set()\n\n  for node in presentation.nodes:\n    statement = node.proof_step.conclusion\n\n    if (\n      not isinstance(\n        statement,\n        Relation,\n      )\n      or statement.relation_type\n      is not RelationType.EQUALITY\n    ):\n      continue\n\n    try:\n      lhs_normalized = (\n        _normalize_generic_eta_family_latex(\n          _render_generic_narrative_expression_latex(\n            statement.lhs\n          )\n        )\n      )\n      rhs_normalized = (\n        _normalize_generic_eta_family_latex(\n          _render_generic_narrative_expression_latex(\n            statement.rhs\n          )\n        )\n      )\n    except (\n      TypeError,\n      ValueError,\n    ):\n      continue\n\n    if (\n      lhs_normalized\n      != rhs_normalized\n    ):\n      continue\n\n    rendered = (\n      _render_generic_narrative_step(\n        node.proof_step\n      )\n    )\n\n    if not rendered:\n      continue\n\n    reflexive_keys.add(\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n\n  if not reflexive_keys:\n    return markdown\n\n  retained = []\n\n  for paragraph in markdown.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    key = (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n    if key in reflexive_keys:\n      continue\n\n    retained.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair30() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair30_no_rendered_reflexive_equalities_remain():\n  rendered = _render_pi6_3_repair30()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert r"$\\eta_{3}^{3} = \\eta_{3}^{3}" not in body\n  assert r"$\\eta_{5} = \\eta_{5}" not in body\n\n\ndef test_phase157_r20_repair30_eta_bridge_and_hopf_support_remain():\n  rendered = _render_pi6_3_repair30()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  required = (\n    r"$\\eta_{6}=E\\eta_{5}$ である.",\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}",\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = \\eta_{5}^{2}",\n    r"$2\\nu\' = \\eta_{3}^{3}",\n  )\n\n  for text in required:\n    assert text in body\n'


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


def ensure_import(
  source: str,
) -> str:
  wanted = (
    "  _render_generic_narrative_expression_latex,\n"
  )

  if wanted in source:
    return source

  anchor = (
    "  _normalize_generic_eta_family_latex,\n"
  )

  if source.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "generic renderer import anchor mismatch"
    )

  return source.replace(
    anchor,
    anchor + wanted,
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
      "phase157_r20_repair30_backup_"
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

  source = ensure_import(
    source
  )
  source = replace_function(
    source,
    "suppress_toda_group_proof_narrative_reflexive_equalities",
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
    "Phase157-R20 repair30 applied."
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
