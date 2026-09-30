from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _group_result():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _context(
  replay,
):
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def test_phase148_rc2_4_repair_r3_web_narrative_uses_depth2_metadata_but_complete_replay_route():
  group_result = (
    _group_result()
  )
  depth2 = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  complete = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )

  assert view.max_depth == 2
  assert len(
    view.steps
  ) == len(
    depth2.steps
  )
  assert complete.max_depth >= 2
  assert len(
    complete.steps
  ) >= len(
    depth2.steps
  )


def test_phase148_rc2_4_repair_r3_measures_contribution_layer_separately():
  group_result = (
    _group_result()
  )
  complete = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _context(
    complete
  )

  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  with_contributions = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  assert isinstance(
    base,
    str,
  )
  assert isinstance(
    with_contributions,
    str,
  )
  assert base
  assert with_contributions
