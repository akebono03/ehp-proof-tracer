from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase143_61b_pi8_5_places_direct_derivation_premises_together():
  rendered = _render(
    5,
    3,
  )

  double_relation = (
    r"$2\nu_{5} = E^{2}\nu'$"
  )
  e2_order = (
    r"$\operatorname{ord}\left(E^{2}\nu'\right) = 4$"
  )
  conclusion = (
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
  )

  assert rendered.count(
    double_relation
  ) == 1
  assert rendered.count(
    e2_order
  ) == 1
  assert (
    rendered.index(
      double_relation
    )
    < rendered.index(
      e2_order
    )
    < rendered.index(
      "以上より、",
      rendered.index(
        e2_order
      ),
    )
    < rendered.index(
      conclusion
    )
  )


def test_phase143_61b_pi8_5_direct_premise_is_not_left_at_argument_start():
  rendered = _render(
    5,
    3,
  )

  double_relation = (
    r"$2\nu_{5} = E^{2}\nu'$"
  )
  pi6_3 = (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
  )

  assert (
    rendered.index(
      pi6_3
    )
    < rendered.index(
      double_relation
    )
  )


def test_phase143_61b_pi6_3_keeps_local_calculation_derivation():
  rendered = _render(
    3,
    3,
  )

  source_one = (
    r"$2\nu' = \eta_{3}E\eta_{3}\eta_{5}$"
  )
  source_two = (
    r"$\eta_{3}E\eta_{3}\eta_{5} = \eta_{3}^{3}$"
  )
  target = (
    r"$2\nu' = \eta_{3}^{3}$"
  )

  assert (
    rendered.index(
      source_one
    )
    < rendered.index(
      source_two
    )
    < rendered.index(
      "これらより、",
      rendered.index(
        source_two
      ),
    )
    < rendered.index(
      target
    )
  )


def test_phase143_61b_pi6_3_does_not_duplicate_order_premises():
  rendered = _render(
    3,
    3,
  )

  assert rendered.count(
    r"$2\nu' = \eta_{3}^{3}$"
  ) == 1
  assert rendered.count(
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
  ) == 1


def test_phase143_61b_pi15_8_final_group_remains_single():
  rendered = _render(
    8,
    7,
  )

  assert (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
    not in rendered
  )
  assert rendered.count(
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
  ) == 1


def test_phase143_61b_pi16_9_final_conclusion_remains():
  rendered = _render(
    9,
    7,
  )

  assert (
    "以上より、\n\n"
    r"$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$"
    in rendered
  )
