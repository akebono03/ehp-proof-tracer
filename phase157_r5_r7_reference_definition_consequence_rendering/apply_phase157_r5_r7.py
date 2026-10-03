
from pathlib import Path

TARGET = Path("toda_group_proof_narrative_contribution_renderer.py")
TEST = Path("tests/test_phase157_r5_r7_reference_definition_consequence_rendering.py")
OUTPUT_DIR = Path("phase157_r5_r7_output")

IMPORT_BLOCK = '''from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)
'''

HELPER = r'''def _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines(
  selected_steps: tuple[
    ProofStep,
    ...,
  ],
  rendered_by_step_id: dict[
    int,
    str,
  ],
) -> tuple[
  str,
  ...,
]:
  boundaries = tuple(
    classify_toda_literature_statement_step(
      proof_step
    )
    for proof_step in selected_steps
  )

  fixed_component_keys = tuple(
    (
      boundary.component_key
      if (
        boundary is not None
        and boundary.classification
        is TodaLiteratureStatementClassification
        .FIXED_STATEMENT
      )
      else None
    )
    for boundary in boundaries
  )

  definition_indices = tuple(
    index
    for index, component_key in enumerate(
      fixed_component_keys
    )
    if (
      component_key is not None
      and component_key.endswith(
        "_definition"
      )
    )
  )

  if (
    len(
      definition_indices
    ) != 1
    or len(
      selected_steps
    ) < 2
  ):
    return tuple(
      rendered_by_step_id[
        id(
          proof_step
        )
      ]
      for proof_step in selected_steps
    )

  definition_index = (
    definition_indices[
      0
    ]
  )
  definition_step = selected_steps[
    definition_index
  ]
  consequence_steps = tuple(
    proof_step
    for index, proof_step in enumerate(
      selected_steps
    )
    if index != definition_index
  )
  ordered_steps = (
    definition_step,
    *consequence_steps,
  )

  lines = []

  for index, proof_step in enumerate(
    ordered_steps
  ):
    line = rendered_by_step_id[
      id(
        proof_step
      )
    ].rstrip()

    if line.endswith(
      "."
    ) or line.endswith(
      ","
    ):
      line = line[
        :-1
      ]

    if index == 0:
      lines.append(
        line
        + " とすると,"
      )
      continue

    if index == len(
      ordered_steps
    ) - 1:
      lines.append(
        line
        + "."
      )
      continue

    lines.append(
      line
      + ","
    )

  return tuple(
    lines
  )
'''

NEW_FUNCTION = r'''def _toda_group_proof_narrative_reference_statement_lines_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    str,
    ...,
  ],
]:
  statement_lines_by_reference_number = {}

  for entry in reference_entries:
    candidate_steps = []
    rendered_by_step_id = {}
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if (
        rendered_statement
        in seen_rendered_statements
      ):
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )
      rendered_by_step_id[
        id(
          proof_step
        )
      ] = rendered_statement

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    rendered_selected_by_step_id = {
      id(
        proof_step
      ): (
        _phase153_r6_render_reference_statement(
          presentation,
          entry,
          proof_step,
          rendered_by_step_id[
            id(
              proof_step
            )
          ],
        )
      )
      for proof_step in selected_steps
    }

    statement_lines = (
      _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines(
        selected_steps,
        rendered_selected_by_step_id,
      )
    )

    if statement_lines:
      statement_lines_by_reference_number[
        entry.number
      ] = statement_lines

  return statement_lines_by_reference_number
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


def _pi6_3_rendered() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[
      0
    ]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _r1_part() -> str:
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[
    0
  ]

  return reference_part.split(
    "**[R2]",
    1,
  )[
    0
  ]


def test_phase157_r5_r7_equation53_definition_precedes_consequences():
  r1_part = _r1_part()

  definition_index = r1_part.find(
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
  )
  membership_index = r1_part.find(
    r"\nu' \in \pi_{6}^{3}"
  )
  double_index = r1_part.find(
    r"2\nu' = \eta_{3}\eta_{4}\eta_{5}"
  )

  assert definition_index >= 0
  assert membership_index >= 0
  assert double_index >= 0
  assert (
    definition_index
    < membership_index
    < double_index
  )


def test_phase157_r5_r7_equation53_definition_uses_to_suru_connector():
  r1_part = _r1_part()

  assert (
    (
      r"$\nu' \in "
      r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$"
      " とすると,"
    )
    in r1_part
  )


def test_phase157_r5_r7_equation53_consequences_use_comma_then_period():
  r1_part = _r1_part()

  assert (
    r"$\nu' \in \pi_{6}^{3}$,"
    in r1_part
  )
  assert (
    (
      r"$2\nu' = "
      r"\eta_{3}\eta_{4}\eta_{5}$."
    )
    in r1_part
  )
'''


def extract_function(text: str, function_name: str) -> str:
  marker = "def " + function_name + "("
  start = text.find(marker)
  if start < 0:
    raise SystemExit("function not found: " + function_name)
  next_function = text.find("\ndef ", start + len(marker))
  if next_function < 0:
    return text[start:]
  return text[start:next_function + 1]


def replace_function(
  text: str,
  function_name: str,
  replacement: str,
) -> str:
  old = extract_function(text, function_name)
  return text.replace(
    old,
    replacement.rstrip() + "\n",
    1,
  )


def main() -> None:
  if not TARGET.exists():
    raise SystemExit(
      "target not found: "
      + str(TARGET)
    )

  text = TARGET.read_text(
    encoding="utf-8"
  )

  import_marker = (
    "from toda_literature_statement_boundary import ("
  )
  if import_marker not in text:
    anchor = '''from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
'''
    if text.count(anchor) != 1:
      raise SystemExit(
        "presentation import anchor mismatch"
      )
    text = text.replace(
      anchor,
      anchor + IMPORT_BLOCK,
      1,
    )
  else:
    start = text.index(import_marker)
    end = text.index(")\n", start) + 2
    existing = text[start:end]
    required = (
      "TodaLiteratureStatementClassification",
      "classify_toda_literature_statement_step",
    )
    if not all(
      name in existing
      for name in required
    ):
      raise SystemExit(
        "existing literature-boundary import block "
        "does not contain required names"
      )

  helper_name = (
    "_phase157_r5_r7_order_and_connect_"
    "fixed_definition_reference_lines"
  )
  if ("def " + helper_name + "(") not in text:
    marker = (
      "def _toda_group_proof_narrative_reference_"
      "statement_lines_by_number("
    )
    index = text.find(marker)
    if index < 0:
      raise SystemExit(
        "statement lines function not found"
      )
    text = (
      text[:index]
      + HELPER
      + "\n\n"
      + text[index:]
    )

  text = replace_function(
    text,
    (
      "_toda_group_proof_narrative_"
      "reference_statement_lines_by_number"
    ),
    NEW_FUNCTION,
  )

  TARGET.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  TEST.write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  (OUTPUT_DIR / "literature_boundary_import_after.txt").write_text(
    IMPORT_BLOCK,
    encoding="utf-8",
    newline="\n",
  )
  (OUTPUT_DIR / "order_and_connect_helper_after.txt").write_text(
    extract_function(
      text,
      helper_name,
    ),
    encoding="utf-8",
    newline="\n",
  )
  (OUTPUT_DIR / "reference_statement_lines_after.txt").write_text(
    extract_function(
      text,
      (
        "_toda_group_proof_narrative_"
        "reference_statement_lines_by_number"
      ),
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R7 Reference definition/consequence rendering applied."
  )


if __name__ == "__main__":
  main()
