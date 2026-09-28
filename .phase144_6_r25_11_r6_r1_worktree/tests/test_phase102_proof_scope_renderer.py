import pytest

from repository_proof_scope_facade import (
  explore_standard_repository_generator_proof_scope_input,
)
from repository_proof_scope_renderer import (
  render_repository_proof_scope_exploration_markdown,
)


def test_phase102_7_renderer_renders_production_nu_prime_sections():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "nu_prime"
    )
  )

  markdown = (
    render_repository_proof_scope_exploration_markdown(
      result
    )
  )

  assert (
    "# $\\nu'$"
    in markdown
  )

  assert (
    "Proof-scope occurrences:"
    in markdown
  )

  assert (
    "Toda memberships:"
    in markdown
  )

  assert (
    "Map relations:"
    in markdown
  )

  assert (
    "## Toda memberships"
    in markdown
  )

  assert (
    "## Map relations"
    in markdown
  )

  assert (
    "Root: standard.toda."
    in markdown
  )

  assert (
    "Depth:"
    in markdown
  )


def test_phase102_7_renderer_zero_semantic_result_has_counts_only():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "eta_999"
    )
  )

  markdown = (
    render_repository_proof_scope_exploration_markdown(
      result
    )
  )

  assert (
    "Proof-scope occurrences: 0"
    in markdown
  )

  assert (
    "Toda memberships: 0"
    in markdown
  )

  assert (
    "Map relations: 0"
    in markdown
  )

  assert (
    "## Toda memberships"
    not in markdown
  )

  assert (
    "## Map relations"
    not in markdown
  )


def test_phase102_7_renderer_rejects_wrong_type():
  with pytest.raises(
    TypeError,
    match=(
      "result must be a "
      "RepositoryProofScopeExplorationResult"
    ),
  ):
    render_repository_proof_scope_exploration_markdown(
      "not-a-result"
    )
