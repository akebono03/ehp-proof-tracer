from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render_multi_argument(
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


def test_phase143_46_pi6_3_assembles_three_main_arguments():
  rendered = _render_multi_argument(
    3,
    3,
  )

  definition = (
    "まず、$\\nu'$ を定める."
  )
  order = (
    "次に、$\\nu'$ の位数を決定する."
  )
  group = (
    "最後に、$\\pi_{6}^{3}$ の群構造を決定する."
  )

  assert definition in rendered
  assert order in rendered
  assert group in rendered
  assert (
    rendered.index(
      definition
    )
    < rendered.index(
      order
    )
    < rendered.index(
      group
    )
  )
  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    in rendered
  )


def test_phase143_46_pi8_5_excludes_detached_nu_prime_order_argument():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert (
    "まず、$\\nu_{5}$ を定める."
    in rendered
  )
  assert (
    "次に、$\\nu_{5}$ の位数を決定する."
    in rendered
  )
  assert (
    "最後に、$\\pi_{8}^{5}$ の群構造を決定する."
    in rendered
  )
  assert (
    "$\\nu'$ の位数を決定する. "
    "そのために、次の完全列を考える."
    not in rendered
  )


def test_phase143_46_pi15_8_single_argument_has_no_discourse_marker():
  rendered = _render_multi_argument(
    8,
    7,
  )

  assert rendered.startswith(
    "$\\pi_{15}^{8}$ の群構造を決定する."
  )
  assert not rendered.startswith(
    "まず、"
  )
  assert not rendered.startswith(
    "最後に、"
  )
  assert (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}"
    in rendered
  )


def test_phase143_46_pi16_9_assembles_definition_then_group_structure():
  rendered = _render_multi_argument(
    9,
    7,
  )

  definition = (
    "まず、$\\sigma_{9}$ を定める."
  )
  group = (
    "最後に、$\\pi_{16}^{9}$ の群構造を決定する."
  )

  assert definition in rendered
  assert group in rendered
  assert (
    rendered.index(
      definition
    )
    < rendered.index(
      group
    )
  )
  assert (
    r"\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}"
    in rendered
  )


def test_phase143_46_empty_arguments_render_empty_string():
  (
    presentation,
    blocks,
    sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  assert (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      (),
    )
    == ""
  )
