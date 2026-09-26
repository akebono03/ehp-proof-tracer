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


def test_phase143_47_pi6_3_suppresses_shared_blocks_and_keeps_short_exact():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert rendered.count(
    r"\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}"
  ) == 1
  assert rendered.count(
    r"2\eta_{3} = 0"
  ) == 1
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )
  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    in rendered
  )


def test_phase143_47_pi8_5_suppresses_shared_exactness_contributions():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert rendered.count(
    r"$\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
  ) == 1
  assert rendered.count(
    r"$\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$ は完全である."
  ) == 1
  assert rendered.count(
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
  ) == 1
  assert (
    r"\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}"
    in rendered
  )


def test_phase143_47_pi15_8_single_argument_is_unchanged_by_dedup():
  rendered = _render_multi_argument(
    8,
    7,
  )

  assert rendered.startswith(
    "$\\pi_{15}^{8}$ の群構造を決定する."
  )
  assert (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}"
    in rendered
  )


def test_phase143_47_pi16_9_suppresses_shared_definition_evidence():
  rendered = _render_multi_argument(
    9,
    7,
  )

  exactness = (
    r"$\pi_{12}^{5} \xrightarrow{H} "
    r"\pi_{12}^{9} \xrightarrow{\Delta} "
    r"\pi_{10}^{4}$ は完全である."
  )

  assert rendered.count(
    exactness
  ) == 1
  assert (
    r"\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}"
    in rendered
  )
  assert (
    "まず、$\\sigma_{9}$ を定める."
    in rendered
  )
  assert (
    "最後に、$\\pi_{16}^{9}$ の群構造を決定する."
    in rendered
  )


def test_phase143_47_pi8_5_still_excludes_detached_argument():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert (
    "$\\nu'$ の位数を決定する. "
    "そのために、次の完全列を考える."
    not in rendered
  )
