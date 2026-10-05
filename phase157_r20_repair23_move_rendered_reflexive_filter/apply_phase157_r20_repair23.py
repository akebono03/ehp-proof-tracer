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
  / "test_phase157_r20_repair23_move_rendered_reflexive_filter.py"
)
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair23() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair23_rendered_reflexive_steps_are_not_displayed():\n  rendered = _render_pi6_3_repair23()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert (\n    r"$\\eta_{3}^{3} = \\eta_{3}^{3}"\n    not in body\n  )\n  assert (\n    r"$\\eta_{5} = \\eta_{5}"\n    not in body\n  )\n\n\ndef test_phase157_r20_repair23_nonreflexive_support_is_preserved():\n  rendered = _render_pi6_3_repair23()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  for text in (\n    r"$2\\nu\' = \\eta_{3}^{3}",\n    r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2",\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}",\n    r"$\\eta_{6}=E\\eta_{5}$ である.",\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = \\eta_{5}^{2}",\n  ):\n    assert text in body\n'



def function_source(
  source: str,
  name: str,
) -> str:
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
      return source[
        start:
        end
      ]

  raise RuntimeError(
    "function not found: "
    + name
  )


def repair_filter_location(
  source: str,
) -> str:
  accidental = """          and (
            context_hidden_step_ids is None
            or id(
              premise_step
            ) not in context_hidden_step_ids
          )
          and not (
            _is_toda_group_proof_narrative_rendered_reflexive_equality_step(
              proof_step
            )
          )
        )
"""

  restored = """          and (
            context_hidden_step_ids is None
            or id(
              premise_step
            ) not in context_hidden_step_ids
          )
        )
"""

  if source.count(
    accidental
  ) != 1:
    raise RuntimeError(
      "repair22 accidental relocated-premise filter "
      "was not found exactly once"
    )

  source = source.replace(
    accidental,
    restored,
    1,
  )

  display_old = """      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            excluded_non_exact_step_ids is None
            or id(
              proof_step
            ) not in excluded_non_exact_step_ids
          )
          and (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
          and (
            (
              id(
                block
              ) in preserve_provenance_block_ids
"""

  display_new = """      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            excluded_non_exact_step_ids is None
            or id(
              proof_step
            ) not in excluded_non_exact_step_ids
          )
          and (
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
            (
              id(
                block
              ) in preserve_provenance_block_ids
"""

  if source.count(
    display_old
  ) != 1:
    raise RuntimeError(
      "display_steps filter anchor was not found exactly once"
    )

  return source.replace(
    display_old,
    display_new,
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
      "phase157_r20_repair23_backup_"
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

  source = repair_filter_location(
    source
  )

  helper_name = (
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step"
  )

  if source.count(
    "def "
    + helper_name
    + "("
  ) != 1:
    raise RuntimeError(
      "rendered-reflexive helper must exist exactly once"
    )

  target_function = function_source(
    source,
    "render_toda_group_proof_narrative_argument_body_markdown",
  )

  if target_function.count(
    helper_name
  ) != 1:
    raise RuntimeError(
      "rendered-reflexive helper must be called exactly once "
      "inside argument body renderer"
    )

  compile(
    source,
    str(
      TARGET
    ),
    "exec",
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  compile(
    TEST_SOURCE,
    str(TEST),
    "exec",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair23 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed:",
    TARGET,
  )
  print("")
  print(
    "Filter placement check:"
  )
  print(
    "  helper definitions =",
    source.count(
      "def "
      + helper_name
      + "("
    ),
  )
  print(
    "  helper calls inside body renderer =",
    target_function.count(
      helper_name
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
