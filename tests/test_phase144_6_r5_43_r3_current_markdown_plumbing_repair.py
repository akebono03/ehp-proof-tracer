import inspect

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  _build_visibility_occurrences,
  build_toda_group_proof_narrative_ordered_contributions,
)


def test_phase144_6_r5_43_r3_current_markdown_is_optional_on_both_layers():
  internal = inspect.signature(
    _build_visibility_occurrences
  )
  public = inspect.signature(
    build_toda_group_proof_narrative_ordered_contributions
  )

  assert internal.parameters["current_markdown"].default is None
  assert public.parameters["current_markdown"].default is None


def test_phase144_6_r5_43_r3_explicit_base_markdown_matches_default_pi6():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)

  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  default_rows = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )
  explicit_rows = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )

  assert tuple(
    tuple(id(row.proof_step) for row in argument_rows)
    for argument_rows in explicit_rows
  ) == tuple(
    tuple(id(row.proof_step) for row in argument_rows)
    for argument_rows in default_rows
  )
