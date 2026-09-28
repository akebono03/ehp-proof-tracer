from repository_proof_scope import (
  build_repository_proof_scope,
)
from rule_applicability import (
  build_inference_rule_premise_pattern_index,
  find_indexed_inference_rule_applicability_candidates,
  find_inference_rule_applicability_candidates,
)
from standard_production_applicability_catalog import (
  build_standard_production_applicability_catalog,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def candidate_signature(
  candidates,
):
  return tuple(
    (
      candidate.catalog_entry.key,
      candidate.premise_index,
      candidate.premise_pattern,
      candidate.source_step,
      candidate.bindings,
    )
    for candidate in candidates
  )


def test_phase103_6b_standard_production_representatives_preserve_candidates():
  repository = (
    build_standard_production_proof_repository()
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  catalog = (
    build_standard_production_applicability_catalog()
  )

  index = (
    build_inference_rule_premise_pattern_index(
      catalog
    )
  )

  representative_nodes = (
    scope.nodes[
      :8
    ]
    + tuple(
      node
      for node in scope.nodes
      if (
        node.shortest_depth > 0
      )
    )[
      :8
    ]
  )

  assert representative_nodes

  for node in representative_nodes:
    brute = (
      find_inference_rule_applicability_candidates(
        catalog,
        node.proof_step,
      )
    )

    indexed = (
      find_indexed_inference_rule_applicability_candidates(
        index,
        node.proof_step,
      )
    )

    assert (
      candidate_signature(
        indexed
      )
      == candidate_signature(
        brute
      )
    )
