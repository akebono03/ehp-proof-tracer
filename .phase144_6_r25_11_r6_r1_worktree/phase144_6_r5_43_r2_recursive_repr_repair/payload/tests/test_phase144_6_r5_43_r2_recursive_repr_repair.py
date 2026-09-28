from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  _group_key,
  build_toda_group_proof_narrative_ordered_contributions,
)


def test_phase144_6_r5_43_r2_group_key_does_not_use_recursive_repr():
  import inspect

  source = inspect.getsource(_group_key)

  assert "repr(" not in source
  assert "_render_generic_narrative_step" in source
  assert "_normalized" in source


def test_phase144_6_r5_43_r2_six_group_population_remains_190():
  total = 0

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)
    base_markdown = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
    ordered = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
        current_markdown=base_markdown,
      )
    )
    total += sum(
      len(argument_rows)
      for argument_rows in ordered
    )

  assert total == 190
