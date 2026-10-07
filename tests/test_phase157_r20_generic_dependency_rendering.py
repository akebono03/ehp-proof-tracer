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


def _render_pi6_3_r20() -> str:
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


def test_phase157_r20_reference_dependencies_are_recovered_from_graph():
  rendered = _render_pi6_3_r20()

  for reference in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "(5.7)",
  ):
    assert reference in rendered

def test_phase157_r20_eta_family_is_canonicalized_generically():
  rendered = _render_pi6_3_r20()

  assert r"\eta_{2}^{3}" in rendered
  assert r"\eta_{3}^{3}" in rendered
  assert r"\eta_{5}" in rendered
  assert r"\eta_{5}^{2}" in rendered

  assert (
    r"\eta_{2}\eta_{3}\eta_{4}"
    not in rendered
  )
  assert (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\eta_{6}\}$."
    not in rendered
  )
  assert (
    r"E^{2}\eta_{3}"
    not in rendered
  )

