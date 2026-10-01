from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_exactness_method_renderer import (
  render_toda_group_proof_narrative_exactness_method_transition,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from tests.test_phase143_30_exactness_method_transition import (
  _transition_data,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)


def _render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
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


def test_phase154_r6_2_repair1_exactness_transition_uses_ascii_comma():
  primary_component, transition = _transition_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert primary_component is not None
  assert transition == (
    "そのために, 次の完全列を考える."
  )


def test_phase154_r6_2_repair1_pi6_3_argument_header_rejoins_purpose_and_method():
  rendered = _render_group(
    3,
    3,
  )

  assert (
    r"次に, $\nu'$ の位数を決定するために, "
    r"次の完全列を考える."
    in rendered
  )
  assert (
    r"$\nu'$ の位数を決定する.そのために"
    not in rendered
  )


def test_phase154_r6_2_repair1_pi11_4_has_no_japanese_punctuation():
  rendered = _render_group(
    4,
    7,
  )

  assert "、" not in rendered
  assert "。" not in rendered

  assert (
    r"まず, $H: \pi_{10}^{3} \to \pi_{10}^{5}$ は単射である."
    in rendered
  )
  assert (
    r"[R2]より, $\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert (
    r"したがって, $\pi_{11}^{4} = 0$を得る."
    in rendered
  )
