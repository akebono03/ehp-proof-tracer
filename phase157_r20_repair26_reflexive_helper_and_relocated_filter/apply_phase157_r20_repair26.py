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
  / "test_phase157_r20_repair26_reflexive_helper_and_relocated_filter.py"
)

HELPER_FUNCTION = 'def _is_toda_group_proof_narrative_rendered_reflexive_equality_step(\n  proof_step: ProofStep,\n) -> bool:\n  if not isinstance(\n    proof_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "proof_step must be a ProofStep"\n    )\n\n  statement = proof_step.conclusion\n\n  if (\n    not isinstance(\n      statement,\n      Relation,\n    )\n    or statement.relation_type\n    is not RelationType.EQUALITY\n  ):\n    return False\n\n  try:\n    lhs_normalized = (\n      _render_generic_narrative_expression_latex(\n        statement.lhs\n      )\n    )\n    rhs_normalized = (\n      _render_generic_narrative_expression_latex(\n        statement.rhs\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    return False\n\n  return (\n    lhs_normalized\n    == rhs_normalized\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair26() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair26_hides_both_rendered_reflexive_equalities():\n  rendered = _render_pi6_3_repair26()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert (\n    r"$\\eta_{3}^{3} = \\eta_{3}^{3}"\n    not in body\n  )\n  assert (\n    r"$\\eta_{5} = \\eta_{5}"\n    not in body\n  )\n\n\ndef test_phase157_r20_repair26_keeps_required_nonreflexive_support():\n  rendered = _render_pi6_3_repair26()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  required = (\n    r"$2\\nu\' = \\eta_{3}^{3}",\n    r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2",\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}",\n    r"$\\eta_{6}=E\\eta_{5}$ である.",\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = \\eta_{5}^{2}",\n  )\n\n  for text in required:\n    assert text in body\n'


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


def remove_unused_try_import(
  source: str,
) -> str:
  line = (
    "  _try_render_generic_narrative_expression_latex,\n"
  )

  if line in source:
    source = source.replace(
      line,
      "",
      1,
    )

  return source


def add_relocated_filter(
  source: str,
) -> str:
  start, end = function_range(
    source,
    "render_toda_group_proof_narrative_argument_body_markdown",
  )
  function_text = source[
    start:
    end
  ]

  anchor = """          and (
            context_hidden_step_ids is None
            or id(
              premise_step
            ) not in context_hidden_step_ids
          )
"""

  if function_text.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "relocated direct premise context-hidden anchor "
      "was not found exactly once"
    )

  insertion = (
    anchor
    + """          and not (
            _is_toda_group_proof_narrative_rendered_reflexive_equality_step(
              premise_step
            )
          )
"""
  )

  function_text = function_text.replace(
    anchor,
    insertion,
    1,
  )

  source = (
    source[:start]
    + function_text
    + source[end:]
  )

  return source


def validate_filter_calls(
  source: str,
) -> None:
  start, end = function_range(
    source,
    "render_toda_group_proof_narrative_argument_body_markdown",
  )
  function_text = source[
    start:
    end
  ]
  helper_name = (
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step"
  )

  if function_text.count(
    helper_name
  ) != 2:
    raise RuntimeError(
      "body renderer must call rendered-reflexive helper "
      "exactly twice: display_steps and relocated premises"
    )

  if (
    helper_name
    + "(\n              proof_step"
    not in function_text
  ):
    raise RuntimeError(
      "display_steps helper call is missing"
    )

  if (
    helper_name
    + "(\n              premise_step"
    not in function_text
  ):
    raise RuntimeError(
      "relocated-premise helper call is missing"
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
      "phase157_r20_repair26_backup_"
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
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step",
    HELPER_FUNCTION,
  )
  source = remove_unused_try_import(
    source
  )
  source = add_relocated_filter(
    source
  )

  validate_filter_calls(
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
    "Phase157-R20 repair26 applied."
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

  start, end = function_range(
    source,
    "render_toda_group_proof_narrative_argument_body_markdown",
  )
  function_text = source[
    start:
    end
  ]

  print("")
  print(
    "Filter placement:"
  )
  print(
    "  body-renderer helper calls =",
    function_text.count(
      "_is_toda_group_proof_narrative_rendered_reflexive_equality_step"
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
