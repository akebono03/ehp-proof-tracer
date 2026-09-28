from dataclasses import dataclass

from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_catalog import (
  RuleRelevanceCategory,
)


@dataclass(frozen=True)
class RepositoryGeneratorApplicabilitySelection:
  applicability_result: RepositoryGeneratorApplicabilityExplorationResult
  candidates: tuple[
    RepositoryProofScopeApplicabilityCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.applicability_result,
      RepositoryGeneratorApplicabilityExplorationResult,
    ):
      raise TypeError(
        "applicability_result must be a "
        "RepositoryGeneratorApplicabilityExplorationResult"
      )

    if not isinstance(
      self.candidates,
      tuple,
    ):
      raise TypeError(
        "candidates must be a tuple"
      )

    source_positions = {
      id(
        candidate
      ): index
      for index, candidate
      in enumerate(
        self.applicability_result.candidates
      )
    }

    selected_positions = []
    selected_candidate_ids = set()

    for candidate in self.candidates:
      if not isinstance(
        candidate,
        RepositoryProofScopeApplicabilityCandidate,
      ):
        raise TypeError(
          "candidates must contain only "
          "RepositoryProofScopeApplicabilityCandidate "
          "objects"
        )

      candidate_id = id(
        candidate
      )

      if candidate_id not in source_positions:
        raise ValueError(
          "each candidate must be an original "
          "candidate from applicability_result"
        )

      if candidate_id in selected_candidate_ids:
        raise ValueError(
          "candidates must not contain duplicate "
          "candidate identities"
        )

      selected_candidate_ids.add(
        candidate_id
      )
      selected_positions.append(
        source_positions[
          candidate_id
        ]
      )

    if selected_positions != sorted(
      selected_positions
    ):
      raise ValueError(
        "candidates must preserve applicability_result "
        "candidate order"
      )


def select_repository_generator_applicability_by_relevance(
  applicability_result,
  relevance_categories,
):
  if not isinstance(
    applicability_result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  if not isinstance(
    relevance_categories,
    tuple,
  ):
    raise TypeError(
      "relevance_categories must be a tuple"
    )

  if any(
    not isinstance(
      category,
      RuleRelevanceCategory,
    )
    for category in relevance_categories
  ):
    raise TypeError(
      "relevance_categories must contain only "
      "RuleRelevanceCategory objects"
    )

  requested_categories = frozenset(
    relevance_categories
  )

  candidates = tuple(
    candidate
    for candidate
    in applicability_result.candidates
    if (
      candidate
      .candidate
      .catalog_entry
      .relevance_category
      in requested_categories
    )
  )

  return RepositoryGeneratorApplicabilitySelection(
    applicability_result=(
      applicability_result
    ),
    candidates=candidates,
  )


def select_repository_generator_applicability_by_source_nodes(
  applicability_result,
  scope_nodes,
):
  if not isinstance(
    applicability_result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  if not isinstance(
    scope_nodes,
    tuple,
  ):
    raise TypeError(
      "scope_nodes must be a tuple"
    )

  if any(
    not isinstance(
      scope_node,
      RepositoryProofScopeNode,
    )
    for scope_node in scope_nodes
  ):
    raise TypeError(
      "scope_nodes must contain only "
      "RepositoryProofScopeNode objects"
    )

  source_node_ids = {
    id(
      candidate.scope_node
    )
    for candidate
    in applicability_result.candidates
  }

  foreign_scope_nodes = tuple(
    scope_node
    for scope_node in scope_nodes
    if id(
      scope_node
    ) not in source_node_ids
  )

  if foreign_scope_nodes:
    raise ValueError(
      "each scope_node must be an original source "
      "node from applicability_result"
    )

  selected_node_ids = {
    id(
      scope_node
    )
    for scope_node in scope_nodes
  }

  candidates = tuple(
    candidate
    for candidate
    in applicability_result.candidates
    if id(
      candidate.scope_node
    ) in selected_node_ids
  )

  return RepositoryGeneratorApplicabilitySelection(
    applicability_result=(
      applicability_result
    ),
    candidates=candidates,
  )


def select_repository_generator_applicability_by_rule_family(
  applicability_result,
  scope_node,
  rule_name,
):
  if not isinstance(
    applicability_result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  if not isinstance(
    scope_node,
    RepositoryProofScopeNode,
  ):
    raise TypeError(
      "scope_node must be a RepositoryProofScopeNode"
    )

  if not isinstance(
    rule_name,
    str,
  ):
    raise TypeError(
      "rule_name must be a str"
    )

  if not rule_name:
    raise ValueError(
      "rule_name must not be empty"
    )

  source_node_ids = {
    id(
      candidate.scope_node
    )
    for candidate
    in applicability_result.candidates
  }

  if id(
    scope_node
  ) not in source_node_ids:
    raise ValueError(
      "scope_node must be an original source node "
      "from applicability_result"
    )

  candidates = tuple(
    candidate
    for candidate
    in applicability_result.candidates
    if (
      candidate.scope_node
      is scope_node
      and candidate
      .candidate
      .inference_rule
      .name
      == rule_name
    )
  )

  return RepositoryGeneratorApplicabilitySelection(
    applicability_result=(
      applicability_result
    ),
    candidates=candidates,
  )
