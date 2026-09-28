from homotopy_groups import (
  DirectSumGroup,
)
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
from toda_proof_narrative_renderer import (
  render_toda_raw_group_structure_latex,
)
from toda_rules import (
  Toda515Sigma8TransportedDecompositionStatement,
)


def _pi15_8_presentation():
  report = build_standard_toda_report(
    n=8,
    k=7,
  )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase134_24_v2_raw_group_renderer_accepts_transported_direct_sum(
):
  presentation = (
    _pi15_8_presentation()
  )

  transported = next(
    node.proof_step.conclusion
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      Toda515Sigma8TransportedDecompositionStatement,
    )
  )

  assert isinstance(
    transported.transported_group,
    DirectSumGroup,
  )

  assert (
    render_toda_raw_group_structure_latex(
      transported.transported_group
    )
    == (
      r"\mathbb{Z}/8\{E\sigma'\}"
      r" \oplus "
      r"\mathbb{Z}\{\sigma_{8}\}"
    )
  )


def test_phase134_24_v2_pi15_8_narrative_renders_transport_order(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation()
    )
  )

  assert (
    r"\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus "
    r"\mathbb{Z}\{\sigma_{8}\}"
    in rendered
  )


def test_phase134_24_v2_pi15_8_narrative_renders_final_standard_order(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation()
    )
  )

  assert (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus "
    r"\mathbb{Z}/8\{E\sigma'\}"
    in rendered
  )
