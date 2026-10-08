from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = REPO_ROOT / "tests" / "test_phase161_pi4_2_restored_reference_relink.py"
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

OLD = '''    )
  else:
    frontier_step_ids = (
      _toda_group_proof_narrative_reference_frontier_step_ids(
        presentation,
        reference_entries,
      )
    )
    boundary_visible_used_step_ids = frozenset(
      step_id
      for step_id in generic_used_step_ids
      if step_id in frontier_step_ids
    )

    (
      reference_entries,
      statement_lines_by_reference_number,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        reference_entries,
        statement_lines_by_reference_number,
        boundary_visible_used_step_ids,
        presentation.root_step,
      )
    )

  if "[R" in rendered:
'''

NEW = '''    )
    rendered = (
      link_toda_group_proof_narrative_unmarked_reference_consumers(
        presentation,
        rendered,
        reference_entries,
      )
    )
  else:
    frontier_step_ids = (
      _toda_group_proof_narrative_reference_frontier_step_ids(
        presentation,
        reference_entries,
      )
    )
    boundary_visible_used_step_ids = frozenset(
      step_id
      for step_id in generic_used_step_ids
      if step_id in frontier_step_ids
    )

    (
      reference_entries,
      statement_lines_by_reference_number,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        reference_entries,
        statement_lines_by_reference_number,
        boundary_visible_used_step_ids,
        presentation.root_step,
      )
    )

  if "[R" in rendered:
'''

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


def _extract_function(
  source: str,
  function_name: str,
) -> str:
  tree = ast.parse(
    source
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name
      == function_name
    ):
      lines = source.splitlines()
      return "\\n".join(
        lines[
          node.lineno - 1:
          node.end_lineno
        ]
      ) + "\\n"

  raise RuntimeError(
    f"function not found: {function_name}"
  )


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )

  if NEW in source:
    print(
      "Production repair is already applied."
    )
  else:
    count = source.count(
      OLD
    )

    if count != 1:
      raise RuntimeError(
        "Expected exactly one Phase 161-R3 insertion anchor, "
        f"found {count}."
      )

    BACKUP_DIR.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      TARGET,
      BACKUP_DIR / TARGET.name,
    )

    updated = source.replace(
      OLD,
      NEW,
      1,
    )
    TARGET.write_text(
      updated,
      encoding="utf-8",
      newline="\\n",
    )
    print(
      "Updated:",
      TARGET,
    )

  TEST.write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\\n",
  )
  print(
    "Wrote:",
    TEST,
  )

  updated_source = TARGET.read_text(
    encoding="utf-8"
  )
  changed_function = _extract_function(
    updated_source,
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    OUTPUT_DIR
    / "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown.py.txt"
  ).write_text(
    changed_function,
    encoding="utf-8",
    newline="\\n",
  )

  (
    OUTPUT_DIR
    / "test_phase161_pi4_2_restored_reference_relink.py.txt"
  ).write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\\n",
  )

  print(
    "Full changed function written to output/."
  )


if __name__ == "__main__":
  main()
