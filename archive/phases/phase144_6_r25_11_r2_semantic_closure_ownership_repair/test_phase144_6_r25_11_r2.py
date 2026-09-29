import inspect

from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)


def _selected_population():
  total = 0
  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)
    base_markdown = render_toda_group_proof_narrative_multi_argument_markdown(
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
      current_markdown=base_markdown,
    )
    total += sum(len(argument_rows) for argument_rows in ordered)
  return total


def test_phase144_6_r25_11_r2_restores_general_direct_premise_boundary():
  source = inspect.getsource(
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids
  )
  protection = """for proof_step in direct_premise_steps:
    protected_step_ids.update("""
  assert protection in source
  protection_index = source.index(protection)
  prefix = source[max(0, protection_index - 120):protection_index]
  assert "ESTABLISH_DEFINITION" not in prefix


def test_phase144_6_r25_11_r2_selected_population_returns_to_190():
  assert _selected_population() == 190
