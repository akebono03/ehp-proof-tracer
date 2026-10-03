from toda_calculation_facade import (
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


def _reference_and_body() -> tuple[
  str,
  str,
]:
  rendered = _pi6_3_rendered()
  reference_part, body_tail = (
    rendered.split(
      "まず",
      1,
    )
  )

  return (
    reference_part,
    "まず" + body_tail,
  )


def test_phase157_r5_r9_fixed_definition_remains_in_reference():
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[
    0
  ]

  assert (
    (
      r"$\nu' \in "
      r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$"
      " とすると,"
    )
    in reference_part
  )
  assert (
    r"$\nu' \in \pi_{6}^{3}$,"
    in reference_part
  )
  assert (
    (
      r"$2\nu' = "
      r"\eta_{3}\eta_{4}\eta_{5}$."
    )
    in reference_part
  )


def test_phase157_r5_r9_fixed_definition_introduction_is_removed_from_body():
  rendered = _pi6_3_rendered()

  assert (
    r"$\nu'$ を定める."
    not in rendered
  )


def test_phase157_r5_r9_definition_only_precondition_is_removed_from_body():
  rendered = _pi6_3_rendered()

  assert (
    r"$2\eta_{3} = 0$"
    not in rendered
  )


def test_phase157_r5_r9_fixed_definition_statement_is_not_repeated_in_body():
  rendered = _pi6_3_rendered()
  definition = (
    r"\nu' \in "
    r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
  )

  assert (
    rendered.count(
      definition
    )
    == 1
  )


def test_phase157_r5_r9_body_starts_with_next_argument_after_reference_boundary():
  rendered = _pi6_3_rendered()
  body = rendered.split(
    "**[R3] Proposition 5.6.**",
    1,
  )[
    1
  ]

  assert (
    "まず, "
    r"$\nu'$ の位数を決定するために"
    in body
  )
