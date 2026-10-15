from toda_rules import (
  TodaProp42ExactnessStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
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
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      n,
      k,
    )
  )
  return (
    presentation,
    blocks,
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    ),
  )


def _normalized_exactness_rendering(
  proof_step,
):
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )
  suffix = r" \text{ is exact}$"

  if rendered.endswith(
    suffix
  ):
    return (
      rendered[
        :-len(
          suffix
        )
      ]
      + "$ は完全である."
    )

  return rendered


def test_phase148_rc2_4_repair_r2_pi6_3_suppresses_owned_primary_raw_windows():
  _presentation, blocks, rendered = (
    _render(
      3,
      3,
    )
  )

  exactness_steps = tuple(
    proof_step
    for block in blocks
    for proof_step in block.steps
    if isinstance(
      proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  assert len(
    exactness_steps
  ) == 3

  for proof_step in exactness_steps:
    assert (
      _normalized_exactness_rendering(
        proof_step
      )
      not in rendered
    )


def test_phase148_rc2_4_repair_r2_pi6_3_keeps_owned_short_exact_sequence():
  _presentation, _blocks, rendered = (
    _render(
      3,
      3,
    )
  )

  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )


def test_phase148_rc2_4_repair_r2_pi6_3_keeps_higher_level_method_sequence():
  _presentation, _blocks, rendered = (
    _render(
      3,
      3,
    )
  )

  assert (
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}"
    in rendered
  )


def test_phase148_rc2_4_repair_r2_pi10_4_keeps_unowned_recursive_hidden():
  _presentation, _blocks, rendered = (
    _render(
      4,
      6,
    )
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


def test_phase148_rc2_4_repair_r2_pi16_9_keeps_recursive_window_hidden():
  _presentation, _blocks, rendered = (
    _render(
      9,
      7,
    )
  )

  assert (
    r"\pi_{12}^{5} \xrightarrow{H} "
    r"\pi_{12}^{9} \xrightarrow{\Delta} "
    r"\pi_{10}^{4}"
    not in rendered
  )
