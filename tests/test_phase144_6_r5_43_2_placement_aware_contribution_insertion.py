from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def _pi6_data():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  ordered = build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=base,
  )
  connected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  return base, connected, blocks, arguments, ordered








def test_phase144_6_r5_43_2_base_renderer_remains_unchanged():
  base, connected, blocks, arguments, ordered = _pi6_data()
  (
    presentation,
    semantic_sidecar,
    fresh_blocks,
    fresh_arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  fresh_base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    fresh_blocks,
    semantic_sidecar,
    fresh_arguments,
  )

  assert base == fresh_base
  assert connected != base


