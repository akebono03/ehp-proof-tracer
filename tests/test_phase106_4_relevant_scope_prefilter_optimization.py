from proof import (
  InferenceRule,
  PremisePattern,
)
import repository_generator_applicability_facade as applicability_facade
from repository_generator_applicability_facade import (
  _build_generator_applicability_result,
)
from repository_proof_scope_applicability import (
  find_repository_proof_scope_applicability_candidates,
)
from repository_proof_scope_facade import (
  explore_standard_repository_generator_proof_scope_input,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


def _build_phase106_4_wildcard_catalog():
  catalog = InferenceRuleCatalog()

  rule = InferenceRule(
    name=(
      "phase106.4 relevant-scope "
      "prefilter wildcard rule"
    ),
    premise_patterns=(
      PremisePattern(),
    ),
  )

  entry = InferenceRuleCatalogEntry(
    key=(
      "phase106.4.relevant-scope."
      "prefilter-wildcard"
    ),
    rule=rule,
    conclusion_type=object,
  )

  catalog.register(
    entry
  )

  return catalog


def _current_phase103_generator_filter_semantics(
  proof_scope_exploration,
  catalog,
):
  all_candidates = (
    find_repository_proof_scope_applicability_candidates(
      proof_scope_exploration.scope,
      catalog,
    )
  )

  occurrence_node_ids = {
    id(
      occurrence.scope_node
    )
    for occurrence
    in proof_scope_exploration.occurrences
  }

  return tuple(
    candidate
    for candidate in all_candidates
    if id(
      candidate.scope_node
    ) in occurrence_node_ids
  )


def test_phase106_4_prefilter_preserves_current_candidate_order_and_identity():
  proof_scope_exploration = (
    explore_standard_repository_generator_proof_scope_input(
      "nu_prime"
    )
  )
  catalog = (
    _build_phase106_4_wildcard_catalog()
  )

  expected = (
    _current_phase103_generator_filter_semantics(
      proof_scope_exploration,
      catalog,
    )
  )

  actual = (
    _build_generator_applicability_result(
      proof_scope_exploration,
      catalog,
    )
    .candidates
  )

  assert len(
    actual
  ) == len(
    expected
  )

  for (
    actual_candidate,
    expected_candidate,
  ) in zip(
    actual,
    expected,
  ):
    assert (
      actual_candidate.scope_node
      is expected_candidate.scope_node
    )
    assert (
      actual_candidate.root_entry
      is expected_candidate.root_entry
    )
    assert (
      actual_candidate.candidate.source_step
      is expected_candidate.candidate.source_step
    )
    assert (
      actual_candidate.candidate.catalog_entry
      is expected_candidate.candidate.catalog_entry
    )
    assert (
      actual_candidate.candidate.inference_rule
      is expected_candidate.candidate.inference_rule
    )
    assert (
      actual_candidate.candidate.premise_index
      == expected_candidate.candidate.premise_index
    )
    assert (
      actual_candidate.candidate.premise_pattern
      == expected_candidate.candidate.premise_pattern
    )
    assert (
      actual_candidate.candidate.bindings
      == expected_candidate.candidate.bindings
    )


def test_phase106_4_finder_receives_only_generator_relevant_scope_nodes(
  monkeypatch,
):
  proof_scope_exploration = (
    explore_standard_repository_generator_proof_scope_input(
      "nu_prime"
    )
  )
  catalog = (
    _build_phase106_4_wildcard_catalog()
  )

  occurrence_node_ids = {
    id(
      occurrence.scope_node
    )
    for occurrence
    in proof_scope_exploration.occurrences
  }

  expected_nodes = tuple(
    scope_node
    for scope_node
    in proof_scope_exploration.scope.nodes
    if id(
      scope_node
    ) in occurrence_node_ids
  )

  captured = {}
  original = (
    applicability_facade
    .find_repository_proof_scope_applicability_candidates
  )

  def capture_scope(
    scope,
    catalog,
  ):
    captured[
      "scope"
    ] = scope

    return original(
      scope,
      catalog,
    )

  monkeypatch.setattr(
    applicability_facade,
    "find_repository_proof_scope_applicability_candidates",
    capture_scope,
  )

  result = (
    _build_generator_applicability_result(
      proof_scope_exploration,
      catalog,
    )
  )

  assert tuple(
    captured[
      "scope"
    ].nodes
  ) == expected_nodes

  assert len(
    captured[
      "scope"
    ].nodes
  ) < len(
    proof_scope_exploration.scope.nodes
  )

  assert len(
    result.candidates
  ) == len(
    expected_nodes
  )


def test_phase106_4_zero_occurrence_path_passes_empty_scope_to_finder(
  monkeypatch,
):
  proof_scope_exploration = (
    explore_standard_repository_generator_proof_scope_input(
      "eta_999"
    )
  )
  catalog = (
    _build_phase106_4_wildcard_catalog()
  )

  captured = {}
  original = (
    applicability_facade
    .find_repository_proof_scope_applicability_candidates
  )

  def capture_scope(
    scope,
    catalog,
  ):
    captured[
      "scope"
    ] = scope

    return original(
      scope,
      catalog,
    )

  monkeypatch.setattr(
    applicability_facade,
    "find_repository_proof_scope_applicability_candidates",
    capture_scope,
  )

  result = (
    _build_generator_applicability_result(
      proof_scope_exploration,
      catalog,
    )
  )

  assert (
    captured[
      "scope"
    ].nodes
    == ()
  )

  assert (
    result.candidates
    == ()
  )
