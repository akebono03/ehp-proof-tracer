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


def _render_pi6_3_repair10() -> str:
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
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase157_r20_repair10_public_references_are_dependency_specialized():
  rendered = _render_pi6_3_repair10()

  headers = (
    "**[R1] Proposition 5.6.**",
    "**[R2] (5.3).**",
    "**[R3] Proposition 5.3.**",
    "**[R4] Proposition 5.1.**",
    "**[R5] Proposition 2.2.**",
  )

  for header in headers:
    assert header in rendered

  reference = rendered.split(
    "---",
    1,
  )[0]

  r3 = reference.split(
    "**[R3] Proposition 5.3.**",
    1,
  )[1].split(
    "**[R4]",
    1,
  )[0]

  assert (
    r"\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}"
    in r3
  )
  assert r"\pi_{5}^{3}" not in r3
  assert r"\pi_{4}^{2}" not in r3

  r4 = reference.split(
    "**[R4] Proposition 5.1.**",
    1,
  )[1].split(
    "**[R5]",
    1,
  )[0]

  assert (
    r"\pi_{6}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\}"
    in r4
  )
  assert r"\pi_{3}^{2}" not in r4

  r5 = reference.split(
    "**[R5] Proposition 2.2.**",
    1,
  )[1]

  assert (
    r"H(\alpha\circ E\beta)"
    in r5
  )
  assert r"\alpha" in r5
  assert r"\beta" in r5
  assert "H(lpha" not in r5
  assert "H(lpha\\circ eta)" not in r5


def test_phase157_r20_repair10_body_uses_same_reference_specializations():
  rendered = _render_pi6_3_repair10()
  body = rendered.split(
    "---",
    1,
  )[1]

  assert "[R3]より" in body
  assert "[R4]より" in body
  assert "[R5]より" in body

  assert (
    r"\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}"
    in body
  )
  assert (
    r"\pi_{6}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\}"
    in body
  )
