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


def test_phase143_57c_pi6_3_first_local_derivation_is_grouped():
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
  connector = "これらより、"

  assert source_one in rendered
  assert source_two in rendered
  assert target in rendered
  assert (
    rendered.index(
      source_one
    )
    < rendered.index(
      source_two
    )
    < rendered.index(
      connector,
      rendered.index(
        source_two
      ),
    )
    < rendered.index(
      target
    )
  )


def test_phase143_57c_pi6_3_second_local_derivation_is_grouped():
  rendered = _render(
    3,
    3,
  )
  source_one = (
    r"$H\left(\nu'\right) = E^{2}\eta_{3}$"
  )
  source_two = (
    r"$E^{2}\eta_{3} = \eta_{5}$"
  )
  target = (
    r"$H\left(\nu'\right) = \eta_{5}$"
  )
  connector = "これらより、"

  assert source_one in rendered
  assert source_two in rendered
  assert target in rendered
  assert (
    rendered.index(
      source_one
    )
    < rendered.index(
      source_two
    )
    < rendered.index(
      connector,
      rendered.index(
        source_two
      ),
    )
    < rendered.index(
      target
    )
  )


def test_phase143_57c_pi6_3_has_two_step_derivation_connectors():
  rendered = _render(
    3,
    3,
  )

  assert rendered.count(
    "これらより、"
  ) == 2


def test_phase143_57c_argument_level_connector_remains_separate():
  rendered = _render(
    3,
    3,
  )

  assert (
    "以上より、\n\n"
    r"$\operatorname{ord}\left(\nu'\right) = 4$"
    in rendered
  )
  assert (
    "以上より、\n\n"
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in rendered
  )


def test_phase143_57c_pi8_5_does_not_gain_step_connector():
  rendered = _render(
    5,
    3,
  )

  assert "これらより、" not in rendered
  assert (
    "以上より、\n\n"
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
    in rendered
  )


def test_phase143_57c_pi15_8_does_not_gain_step_connector():
  rendered = _render(
    8,
    7,
  )

  assert "これらより、" not in rendered


def test_phase143_57c_pi16_9_does_not_gain_step_connector():
  rendered = _render(
    9,
    7,
  )

  assert "これらより、" not in rendered
