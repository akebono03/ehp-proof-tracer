import re

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


def _render_pi6_3(
  depth: int,
) -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _parts(
  rendered: str,
) -> tuple[
  str,
  str,
]:
  body_marker = (
    "次に, $\\nu'$ の位数を決定するために"
  )
  body_index = rendered.find(
    body_marker
  )

  if body_index < 0:
    raise AssertionError(
      "pi_6^3 public body start marker is missing"
    )

  return (
    rendered[
      :body_index
    ].rstrip(),
    rendered[
      body_index:
    ],
  )


def test_phase156_r5_repair7_depth2_collapses_53_internal_proof():
  reference_part, body = _parts(
    _render_pi6_3(
      2
    )
  )

  assert "(5.3)" in reference_part
  assert "Lemma 5.2.**" not in reference_part
  assert "Lemma 5.2" not in body
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in body
  )
  assert "$2\\eta_{3} = 0$" not in body
  assert "$\\nu'$ を定める." not in body


def test_phase156_r5_repair7_depth3_collapses_53_internal_proof():
  reference_part, body = _parts(
    _render_pi6_3(
      3
    )
  )

  assert "(5.3)" in reference_part
  assert "Lemma 5.2.**" not in reference_part
  assert "Lemma 5.2" not in body
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in body
  )
  assert "$2\\eta_{3} = 0$" not in body
  assert "$\\nu'$ を定める." not in body


def test_phase156_r5_repair7_53_reference_keeps_public_consequences():
  reference_part, body = _parts(
    _render_pi6_3(
      2
    )
  )
  sections = re.split(
    r"(?=\*\*\[R\d+\] )",
    reference_part,
  )
  section = next(
    part
    for part in sections
    if re.search(
      r"\*\*\[R\d+\] \(5\.3\)\.\*\*",
      part,
    )
  )

  assert "\\nu' \\in \\pi_{6}^{3}" in section
  assert "2\\nu'" in section
