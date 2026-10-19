from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render(n, k):
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      n,
      k,
    )
  )
  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase148_rc2_3_repair_r1_pi10_4_closes_relocation_bypass():
  rendered = _render(
    4,
    6,
  )
  assert (
    r"\pi_{9}^{3} \xrightarrow{H} "
    r"\pi_{9}^{5} \xrightarrow{\Delta} "
    r"\pi_{7}^{2}"
    not in rendered
  )
  assert (
    r"\pi_{8}^{2} \xrightarrow{E} "
    r"\pi_{9}^{3} \xrightarrow{H} "
    r"\pi_{9}^{5}"
    not in rendered
  )


def test_phase148_rc2_3_repair_r1_pi6_3_keeps_owned_short_exact_sequence():
  rendered = _render(
    3,
    3,
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )


def test_phase148_rc2_3_repair_r1_pi16_9_keeps_recursive_window_hidden():
  rendered = _render(
    9,
    7,
  )
  assert (
    r"\pi_{12}^{5} \xrightarrow{H} "
    r"\pi_{12}^{9} \xrightarrow{\Delta} "
    r"\pi_{10}^{4}"
    not in rendered
  )
