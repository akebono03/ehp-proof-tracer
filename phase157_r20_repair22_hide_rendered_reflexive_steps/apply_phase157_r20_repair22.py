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
  / "test_phase157_r20_repair22_hide_rendered_reflexive_steps.py"
)

HELPER = 'def _is_toda_group_proof_narrative_rendered_reflexive_equality_step(\n  proof_step: ProofStep,\n) -> bool:\n  if not isinstance(\n    proof_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "proof_step must be a ProofStep"\n    )\n\n  statement = proof_step.conclusion\n\n  if (\n    not isinstance(\n      statement,\n      Relation,\n    )\n    or statement.relation_type\n    is not RelationType.EQUALITY\n  ):\n    return False\n\n  lhs_raw = (\n    _try_render_generic_narrative_expression_latex(\n      statement.lhs\n    )\n  )\n  rhs_raw = (\n    _try_render_generic_narrative_expression_latex(\n      statement.rhs\n    )\n  )\n\n  if (\n    lhs_raw is None\n    or rhs_raw is None\n  ):\n    return False\n\n  try:\n    lhs_normalized = (\n      _render_generic_narrative_expression_latex(\n        statement.lhs\n      )\n    )\n    rhs_normalized = (\n      _render_generic_narrative_expression_latex(\n        statement.rhs\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    return False\n\n  return (\n    lhs_normalized\n    == rhs_normalized\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair22() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair22_hides_eta3_rendered_reflexive_equality():\n  rendered = _render_pi6_3_repair22()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert (\n    r"$\\eta_{3}^{3} = \\eta_{3}^{3}"\n    not in body\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}"\n    in body\n  )\n  assert (\n    r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2"\n    in body\n  )\n\n\ndef test_phase157_r20_repair22_hides_eta5_rendered_reflexive_equality():\n  rendered = _render_pi6_3_repair22()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert (\n    r"$\\eta_{5} = \\eta_{5}"\n    not in body\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}"\n    in body\n  )\n\n\ndef test_phase157_r20_repair22_keeps_eta_suspension_bridge():\n  rendered = _render_pi6_3_repair22()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert (\n    r"$\\eta_{6}=E\\eta_{5}$ である."\n    in body\n  )\n  assert (\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = \\eta_{5}^{2}"\n    in body\n  )\n'


def function_range(
  source: str,
  name: str,
):
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

      while (
        end < len(source)
        and source[
          end:
          end + 1
        ] == "\n"
      ):
        end += 1

      return start, end

  raise RuntimeError(
    "function not found: "
    + name
  )


def insert_before_function(
  source: str,
  before_name: str,
  addition: str,
) -> str:
  start, _end = function_range(
    source,
    before_name,
  )

  return (
    source[:start]
    + addition.rstrip()
    + "\n\n\n"
    + source[start:]
  )


def replace_imports(
  source: str,
) -> str:
  old_generic = """from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _generic_short_exact_sequence_reason_prose,
  _render_generic_narrative_proof_block,
  _render_generic_narrative_step,
)
"""
  new_generic = """from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _generic_short_exact_sequence_reason_prose,
  _render_generic_narrative_expression_latex,
  _render_generic_narrative_proof_block,
  _render_generic_narrative_step,
  _try_render_generic_narrative_expression_latex,
)
"""

  old_proof = """from proof import (
  ProofStep,
)
"""
  new_proof = """from proof import (
  ProofStep,
  Relation,
  RelationType,
)
"""

  if source.count(
    old_generic
  ) != 1:
    raise RuntimeError(
      "generic narrative renderer import block mismatch"
    )

  if source.count(
    old_proof
  ) != 1:
    raise RuntimeError(
      "proof import block mismatch"
    )

  source = source.replace(
    old_generic,
    new_generic,
    1,
  )
  source = source.replace(
    old_proof,
    new_proof,
    1,
  )

  return source


def add_display_filter(
  source: str,
) -> str:
  old = """          and (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
          and (
"""

  new = """          and (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
          and not (
            _is_toda_group_proof_narrative_rendered_reflexive_equality_step(
              proof_step
            )
          )
          and (
"""

  if source.count(
    old
  ) < 1:
    raise RuntimeError(
      "display_steps filter anchor not found"
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
      "phase157_r20_repair22_backup_"
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

  source = replace_imports(
    source
  )

  if (
    "def _is_toda_group_proof_narrative_rendered_reflexive_equality_step("
    not in source
  ):
    source = insert_before_function(
      source,
      "render_toda_group_proof_narrative_argument_body_markdown",
      HELPER,
    )

  source = add_display_filter(
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
    "Phase157-R20 repair22 applied."
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
