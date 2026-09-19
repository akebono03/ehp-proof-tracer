import pytest

from expression import (
  GeneratorSymbol,
)
from map_facts import EHP_H_MAP
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_proof_scope_exploration import (
  RepositoryProofScopeGeneratorOccurrence,
  RepositoryProofScopeMapRelationOccurrence,
  RepositoryProofScopeTodaMembershipOccurrence,
  find_repository_proof_scope_generator_occurrences,
  find_repository_proof_scope_map_relation_occurrences,
  find_repository_proof_scope_toda_membership_occurrences,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def nu_prime_generator():
  return GeneratorSymbol(
    family="ν",
    decoration="′",
  )


def build_standard_scope():
  repository = (
    build_standard_production_proof_repository()
  )

  return (
    repository,
    build_repository_proof_scope(
      repository
    ),
  )


def test_phase102_5b_standard_scope_has_nu_prime_occurrences_below_root():
  repository, scope = build_standard_scope()

  result = (
    find_repository_proof_scope_generator_occurrences(
      scope,
      nu_prime_generator(),
    )
  )

  assert result

  assert all(
    isinstance(
      occurrence,
      RepositoryProofScopeGeneratorOccurrence,
    )
    for occurrence in result
  )

  assert any(
    occurrence
    .scope_node
    .shortest_depth
    > 0
    for occurrence in result
  )

  assert all(
    any(
      occurrence.scope_node.root_entry
      is entry
      for entry in repository.entries()
    )
    for occurrence in result
  )


def test_phase102_5b_standard_scope_finds_nu_prime_as_membership_element():
  _, scope = build_standard_scope()

  result = (
    find_repository_proof_scope_toda_membership_occurrences(
      scope,
      nu_prime_generator(),
    )
  )

  element_matches = tuple(
    occurrence
    for occurrence in result
    if occurrence.is_membership_element
  )

  assert element_matches

  assert all(
    isinstance(
      occurrence,
      RepositoryProofScopeTodaMembershipOccurrence,
    )
    for occurrence in element_matches
  )

  assert any(
    occurrence.statement.element.generator
    == nu_prime_generator()
    and occurrence.statement.bracket.index == 1
    for occurrence in element_matches
  )


def test_phase102_5b_standard_scope_membership_preserves_root_provenance():
  _, scope = build_standard_scope()

  result = (
    find_repository_proof_scope_toda_membership_occurrences(
      scope,
      nu_prime_generator(),
    )
  )

  match = next(
    occurrence
    for occurrence in result
    if occurrence.is_membership_element
  )

  assert (
    match
    .source_occurrence
    .scope_node
    .root_entry
    .key
    .startswith(
      "standard.toda."
    )
  )

  assert (
    match
    .source_occurrence
    .scope_node
    .shortest_depth
    > 0
  )


def test_phase102_5b_standard_scope_finds_h_nu_prime_relation():
  _, scope = build_standard_scope()

  result = (
    find_repository_proof_scope_map_relation_occurrences(
      scope,
      nu_prime_generator(),
      map_symbol=EHP_H_MAP,
    )
  )

  assert result

  assert all(
    isinstance(
      occurrence,
      RepositoryProofScopeMapRelationOccurrence,
    )
    for occurrence in result
  )

  assert any(
    occurrence.map == EHP_H_MAP
    and (
      occurrence
      .input_expression
      .generator
      == nu_prime_generator()
    )
    for occurrence in result
  )


def test_phase102_5b_map_relation_preserves_actual_proof_step_identity():
  _, scope = build_standard_scope()

  result = (
    find_repository_proof_scope_map_relation_occurrences(
      scope,
      nu_prime_generator(),
      map_symbol=EHP_H_MAP,
    )
  )

  occurrence = result[
    0
  ]

  assert (
    occurrence.relation
    is occurrence
    .source_occurrence
    .scope_node
    .proof_step
    .conclusion
  )

  assert (
    occurrence.map_application
    is occurrence.relation.lhs
  )

  assert (
    occurrence.input_expression
    is occurrence.relation.lhs.expression
  )

  assert (
    occurrence.output_expression
    is occurrence.relation.rhs
  )


def test_phase102_5b_unknown_generator_returns_empty_semantic_results():
  _, scope = build_standard_scope()

  unknown = GeneratorSymbol(
    family="ζ",
    index=999,
  )

  assert (
    find_repository_proof_scope_toda_membership_occurrences(
      scope,
      unknown,
    )
    == ()
  )

  assert (
    find_repository_proof_scope_map_relation_occurrences(
      scope,
      unknown,
    )
    == ()
  )


def test_phase102_5b_scope_search_is_deterministic():
  _, scope = build_standard_scope()

  first = (
    find_repository_proof_scope_generator_occurrences(
      scope,
      nu_prime_generator(),
    )
  )

  second = (
    find_repository_proof_scope_generator_occurrences(
      scope,
      nu_prime_generator(),
    )
  )

  assert tuple(
    (
      occurrence.scope_node.root_entry.key,
      id(
        occurrence.scope_node.proof_step
      ),
      occurrence.scope_node.shortest_depth,
      occurrence.path,
      occurrence.roles,
    )
    for occurrence in first
  ) == tuple(
    (
      occurrence.scope_node.root_entry.key,
      id(
        occurrence.scope_node.proof_step
      ),
      occurrence.scope_node.shortest_depth,
      occurrence.path,
      occurrence.roles,
    )
    for occurrence in second
  )


def test_phase102_5b_repository_is_not_mutated_by_scope_semantic_search():
  repository, scope = build_standard_scope()

  before = (
    repository.entries()
  )

  find_repository_proof_scope_toda_membership_occurrences(
    scope,
    nu_prime_generator(),
  )

  find_repository_proof_scope_map_relation_occurrences(
    scope,
    nu_prime_generator(),
  )

  after = (
    repository.entries()
  )

  assert after == before

  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase102_5b_generator_search_rejects_non_scope():
  with pytest.raises(
    TypeError,
    match=(
      "scope must be a RepositoryProofScopeResult"
    ),
  ):
    find_repository_proof_scope_generator_occurrences(
      "not-a-scope",
      nu_prime_generator(),
    )


def test_phase102_5b_generator_search_rejects_non_generator():
  _, scope = build_standard_scope()

  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    find_repository_proof_scope_generator_occurrences(
      scope,
      "ν′",
    )


def test_phase102_5b_map_search_rejects_invalid_map_filter():
  _, scope = build_standard_scope()

  with pytest.raises(
    TypeError,
    match=(
      "map_symbol must be a MapSymbol or None"
    ),
  ):
    find_repository_proof_scope_map_relation_occurrences(
      scope,
      nu_prime_generator(),
      map_symbol="H",
    )
