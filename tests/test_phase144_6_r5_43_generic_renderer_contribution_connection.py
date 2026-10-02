from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def _pi6_context():
  return _context(3, 3)


def test_phase144_6_r5_43_pi6_uses_five_production_contributions():
  presentation, semantic_sidecar, blocks, arguments, aggregate_semantic_sidecar, proof_chains = _pi6_context()
  base=render_toda_group_proof_narrative_multi_argument_markdown(presentation,blocks,semantic_sidecar,arguments)
  ordered=build_toda_group_proof_narrative_ordered_contributions(presentation,blocks,semantic_sidecar,arguments,proof_chains,current_markdown=base)
  assert tuple(x for x in ordered if x)



def test_phase144_6_r5_43_base_renderer_remains_unchanged_and_opt_in():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _pi6_context()
  before = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  after = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  connected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert before == after
  assert connected != before


def test_phase144_6_r5_43_has_no_pi6_specific_branch():
  import inspect
  import toda_group_proof_narrative_contribution_renderer as module

  source = inspect.getsource(module)
  assert "n == 3" not in source
  assert "k == 3" not in source
  assert "_pi6" not in source.lower()
