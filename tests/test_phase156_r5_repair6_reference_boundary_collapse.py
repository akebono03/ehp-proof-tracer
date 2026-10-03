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


def _pi6_3_rendered(
  depth: int = 2,
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


def test_phase156_r5_repair6_reference_53_is_public_boundary():
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[0]
  headers = re.findall(
    r"\*\*\[R\d+\] ([^\n]+?)\.\*\*",
    reference_part,
  )

  assert headers.count(
    "(5.3)"
  ) == 1
  assert "Lemma 5.2" not in headers


def test_phase156_r5_repair6_pi6_body_does_not_expand_53_internal_proof():
  rendered = _pi6_3_rendered()

  assert "Lemma 5.2" not in rendered
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in rendered
  )
  assert "$\\nu'$ を定める." not in rendered


def test_phase156_r5_repair6_pi6_keeps_53_consequences_as_reference_results():
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  section = next(
    part
    for part in re.split(
      r"(?=\*\*\[R\d+\] )",
      reference_part,
    )
    if re.search(
      r"\*\*\[R\d+\] \(5\.3\)\.\*\*",
      part,
    )
  )

  assert "\\nu' \\in \\pi_{6}^{3}" in section
  assert "2\\nu'" in section


def test_phase156_r5_repair6_depth3_keeps_same_public_boundary():
  rendered = _pi6_3_rendered(
    depth=3,
  )

  assert "(5.3)" in rendered
  assert "Lemma 5.2.**" not in rendered
  assert "Lemma 5.2" not in rendered
  assert "$\\nu'$ を定める." not in rendered
