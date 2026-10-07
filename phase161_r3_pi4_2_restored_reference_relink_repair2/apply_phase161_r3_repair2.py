from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = REPO_ROOT / "tests" / "test_phase161_pi4_2_restored_reference_relink.py"

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

FUNCTION_NAME = (
  "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown"
)

RESTORE_NAME = (
  "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage"
)

RELINK_NAME = (
  "link_toda_group_proof_narrative_unmarked_reference_consumers"
)

RELINK_LINES = [
  "    rendered = (",
  "      link_toda_group_proof_narrative_unmarked_reference_consumers(",
  "        presentation,",
  "        rendered,",
  "        reference_entries,",
  "      )",
  "    )",
]

TEST_TEXT = r'''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _render_pi4_2_phase161_r3() -> str:
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase161_r3_pi4_2_reference_keeps_toda52_and_prop44():
  rendered = _render_pi4_2_phase161_r3()
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "**[R1] (5.2).**" in reference
  assert (
    r"$\eta_{2}\circ -: "
    r"\pi_{i}^{3} \to \pi_{i}^{2}$"
    in reference
  )
  assert "**[R2] Proposition 4.4.**" in reference

  assert "[R1]" in body
  assert "[R2]" in body


def test_phase161_r3_pi4_2_keeps_group_result_and_qed():
  rendered = _render_pi4_2_phase161_r3()

  assert (
    r"\pi_{4}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
    in rendered
  )
  assert "□" in rendered
'''


def _call_name(
  node,
):
  if not isinstance(
    node,
    ast.Call,
  ):
    return None

  function = node.func

  if isinstance(
    function,
    ast.Name,
  ):
    return function.id

  if isinstance(
    function,
    ast.Attribute,
  ):
    return function.attr

  return None


def _statement_contains_call(
  statement,
  target_name: str,
) -> bool:
  return any(
    _call_name(
      node
    ) == target_name
    for node in ast.walk(
      statement
    )
    if isinstance(
      node,
      ast.Call,
    )
  )


def _find_target_function(
  tree,
):
  matches = [
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == FUNCTION_NAME
    )
  ]

  if len(
    matches
  ) != 1:
    raise RuntimeError(
      "Expected exactly one target render function, "
      f"found {len(matches)}."
    )

  return matches[
    0
  ]


def _already_relinked_after_restore(
  function_node,
) -> bool:
  for statement in function_node.body:
    if not isinstance(
      statement,
      ast.If,
    ):
      continue

    restore_indices = [
      index
      for index, child in enumerate(
        statement.body
      )
      if _statement_contains_call(
        child,
        RESTORE_NAME,
      )
    ]

    if not restore_indices:
      continue

    for restore_index in restore_indices:
      for child in statement.body[
        restore_index + 1:
      ]:
        if _statement_contains_call(
          child,
          RELINK_NAME,
        ):
          return True

  return False


def _find_restore_statement_end_line(
  function_node,
) -> int:
  candidates = []

  for statement in function_node.body:
    if not isinstance(
      statement,
      ast.If,
    ):
      continue

    for child in statement.body:
      if _statement_contains_call(
        child,
        RESTORE_NAME,
      ):
        candidates.append(
          child.end_lineno
        )

  if len(
    candidates
  ) != 1:
    raise RuntimeError(
      "Expected exactly one restore statement in the "
      "target function, "
      f"found {len(candidates)}."
    )

  return candidates[
    0
  ]


def _extract_function(
  source: str,
) -> str:
  tree = ast.parse(
    source
  )
  function_node = _find_target_function(
    tree
  )
  lines = source.splitlines()

  return "\n".join(
    lines[
      function_node.lineno - 1:
      function_node.end_lineno
    ]
  ) + "\n"


def _validate_repair(
  source: str,
) -> None:
  tree = ast.parse(
    source
  )
  function_node = _find_target_function(
    tree
  )

  if not _already_relinked_after_restore(
    function_node
  ):
    raise RuntimeError(
      "Repaired source does not contain the relink "
      "after the fixed-reference restore."
    )


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )

  tree = ast.parse(
    source
  )
  function_node = _find_target_function(
    tree
  )

  if _already_relinked_after_restore(
    function_node
  ):
    print(
      "Production repair is already applied."
    )
  else:
    restore_end_line = (
      _find_restore_statement_end_line(
        function_node
      )
    )

    source_lines = source.splitlines()

    insertion_index = restore_end_line

    repaired_lines = (
      source_lines[
        :insertion_index
      ]
      + RELINK_LINES
      + source_lines[
        insertion_index:
      ]
    )

    updated_source = (
      "\n".join(
        repaired_lines
      )
      + (
        "\n"
        if source.endswith(
          "\n"
        )
        else ""
      )
    )

    _validate_repair(
      updated_source
    )

    BACKUP_DIR.mkdir(
      parents=True,
      exist_ok=True,
    )

    shutil.copy2(
      TARGET,
      BACKUP_DIR / TARGET.name,
    )

    TARGET.write_text(
      updated_source,
      encoding="utf-8",
      newline="\n",
    )

    print(
      "Updated:",
      TARGET,
    )
    print(
      "Inserted relink immediately after restore statement."
    )

  TEST.write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Wrote:",
    TEST,
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  full_function = _extract_function(
    TARGET.read_text(
      encoding="utf-8"
    )
  )

  (
    OUTPUT_DIR
    / "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown.py.txt"
  ).write_text(
    full_function,
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "test_phase161_pi4_2_restored_reference_relink.py.txt"
  ).write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Full changed function and full test file written to output/."
  )


if __name__ == "__main__":
  main()
