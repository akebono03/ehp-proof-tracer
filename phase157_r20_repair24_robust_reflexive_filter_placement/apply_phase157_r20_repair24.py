from __future__ import annotations

import ast
import re
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
  / "test_phase157_r20_repair24_robust_reflexive_filter_placement.py"
)

TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair24() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair24_reflexive_equalities_are_hidden():\n  rendered = _render_pi6_3_repair24()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert r"$\\eta_{3}^{3} = \\eta_{3}^{3}" not in body\n  assert r"$\\eta_{5} = \\eta_{5}" not in body\n\n\ndef test_phase157_r20_repair24_needed_nonreflexive_steps_remain():\n  rendered = _render_pi6_3_repair24()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  for text in (\n    r"$2\\nu\' = \\eta_{3}^{3}",\n    r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2",\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}",\n    r"$\\eta_{6}=E\\eta_{5}$ である.",\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = \\eta_{5}^{2}",\n  ):\n    assert text in body\n'


def function_range(
  source: str,
  name: str,
) -> tuple[int, int]:
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


def remove_helper_calls(
  function_text: str,
) -> str:
  pattern = re.compile(
    r"""
(?P<indent>[ \t]*)and[ \t]+not[ \t]*\(\s*
_is_toda_group_proof_narrative_rendered_reflexive_equality_step
\(\s*proof_step\s*\)\s*
\)
""",
    re.VERBOSE,
  )

  return pattern.sub(
    "",
    function_text,
  )


def insert_filter_in_display_steps(
  function_text: str,
) -> str:
  display_start = function_text.find(
    "      display_steps = tuple("
  )

  if display_start < 0:
    raise RuntimeError(
      "display_steps block not found"
    )

  display_end_anchor = (
    "\n\n      if not display_steps:"
  )
  display_end = function_text.find(
    display_end_anchor,
    display_start,
  )

  if display_end < 0:
    raise RuntimeError(
      "display_steps end not found"
    )

  display_block = function_text[
    display_start:
    display_end
  ]

  if (
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step"
    in display_block
  ):
    raise RuntimeError(
      "display_steps unexpectedly already contains helper call "
      "after cleanup"
    )

  anchor = """          and (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
"""

  if display_block.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "display_steps context-hidden anchor mismatch"
    )

  insertion = anchor + """          and not (
            _is_toda_group_proof_narrative_rendered_reflexive_equality_step(
              proof_step
            )
          )
"""

  display_block = display_block.replace(
    anchor,
    insertion,
    1,
  )

  return (
    function_text[:display_start]
    + display_block
    + function_text[display_end:]
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
      "phase157_r20_repair24_backup_"
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

  helper_name = (
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step"
  )

  if source.count(
    "def "
    + helper_name
    + "("
  ) != 1:
    raise RuntimeError(
      "repair22 helper definition is not present exactly once"
    )

  start, end = function_range(
    source,
    "render_toda_group_proof_narrative_argument_body_markdown",
  )
  function_text = source[
    start:
    end
  ]

  function_text = remove_helper_calls(
    function_text
  )
  function_text = insert_filter_in_display_steps(
    function_text
  )

  if function_text.count(
    helper_name
  ) != 1:
    raise RuntimeError(
      "helper must be called exactly once in body renderer"
    )

  source = (
    source[:start]
    + function_text
    + source[end:]
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
    "Phase157-R20 repair24 applied."
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
    "Placement check:"
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
    "  helper calls in body renderer =",
    function_text.count(
      helper_name
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
