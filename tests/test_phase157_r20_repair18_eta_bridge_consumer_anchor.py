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


def _render_pi6_3_repair18() -> str:
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


def test_phase157_r20_repair18_eta_bridge_uses_consumer_anchor():
  rendered = _render_pi6_3_repair18()
  body = rendered.split(
    "---",
    1,
  )[1]

  bridge = (
    r"$\eta_{6}=E\eta_{5}$."
  )
  hopf_value = (
    r"$H\left(\nu'\eta_{6}\right) = "
    r"\eta_{5}^{2}"
  )

  assert bridge in body
  assert hopf_value in body
  assert body.index(
    bridge
  ) < body.index(
    hopf_value
  )


def test_phase157_r20_repair18_does_not_require_visible_eta_definition_paragraph():
  rendered = _render_pi6_3_repair18()
  body = rendered.split(
    "---",
    1,
  )[1]

  assert (
    r"$\eta_{6}=E\eta_{5}$."
    in body
  )
  assert (
    "TodaEtaFamilyDefinitionStatement"
    not in body
  )
