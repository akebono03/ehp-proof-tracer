from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "toda_group_proof_narrative_argument_body_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair28_match_step_level_eta_normalization.py"
)

HELPER_FUNCTION = 'def _is_toda_group_proof_narrative_rendered_reflexive_equality_step(\n  proof_step: ProofStep,\n) -> bool:\n  if not isinstance(\n    proof_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "proof_step must be a ProofStep"\n    )\n\n  statement = proof_step.conclusion\n\n  if (\n    not isinstance(\n      statement,\n      Relation,\n    )\n    or statement.relation_type\n    is not RelationType.EQUALITY\n  ):\n    return False\n\n  try:\n    lhs_normalized = (\n      _normalize_generic_eta_family_latex(\n        _render_generic_narrative_expression_latex(\n          statement.lhs\n        )\n      )\n    )\n    rhs_normalized = (\n      _normalize_generic_eta_family_latex(\n        _render_generic_narrative_expression_latex(\n          statement.rhs\n        )\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    return False\n\n  return (\n    lhs_normalized\n    == rhs_normalized\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair28() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair28_hides_eta3_step_level_reflexive_equality():\n  rendered = _render_pi6_3_repair28()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert (\n    r"$\\eta_{3}^{3} = \\eta_{3}^{3}"\n    not in body\n  )\n\n\ndef test_phase157_r20_repair28_hides_eta5_step_level_reflexive_equality():\n  rendered = _render_pi6_3_repair28()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert (\n    r"$\\eta_{5} = \\eta_{5}"\n    not in body\n  )\n\n\ndef test_phase157_r20_repair28_keeps_needed_support():\n  rendered = _render_pi6_3_repair28()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  required = (\n    r"$2\\nu\' = \\eta_{3}^{3}",\n    r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2",\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}",\n    r"$\\eta_{6}=E\\eta_{5}$ である.",\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = \\eta_{5}^{2}",\n  )\n\n  for text in required:\n    assert text in body\n'


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


def add_eta_family_normalizer_import(
  source: str,
) -> str:
  anchor = (
    "  _generic_short_exact_sequence_reason_prose,\n"
  )
  addition = (
    "  _normalize_generic_eta_family_latex,\n"
  )

  if addition in source:
    return source

  if source.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "generic renderer import anchor mismatch"
    )

  return source.replace(
    anchor,
    anchor + addition,
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
      "phase157_r20_repair28_backup_"
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

  source = add_eta_family_normalizer_import(
    source
  )
  source = replace_function(
    source,
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step",
    HELPER_FUNCTION,
  )

  body_start, body_end = function_range(
    source,
    "render_toda_group_proof_narrative_argument_body_markdown",
  )
  body_source = source[
    body_start:
    body_end
  ]

  helper_name = (
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step"
  )

  if body_source.count(
    helper_name
  ) != 2:
    raise RuntimeError(
      "repair26 filters must remain exactly twice"
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
    "Phase157-R20 repair28 applied."
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

  print("")
  print(
    "Body-renderer helper calls:",
    body_source.count(
      helper_name
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
