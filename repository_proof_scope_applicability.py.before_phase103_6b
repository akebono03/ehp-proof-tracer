from dataclasses import dataclass

from repository_proof_scope import (
  RepositoryProofScopeNode,
  RepositoryProofScopeResult,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
  find_inference_rule_applicability_candidates,
)
from rule_catalog import (
  InferenceRuleCatalog,
)


@dataclass(frozen=True)
class RepositoryProofScopeApplicabilityCandidate:
  scope_node: RepositoryProofScopeNode
  candidate: InferenceRuleApplicabilityCandidate

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.scope_node,
      RepositoryProofScopeNode,
    ):
      raise TypeError(
        "scope_node must be a "
        "RepositoryProofScopeNode"
      )

    if not isinstance(
      self.candidate,
      InferenceRuleApplicabilityCandidate,
    ):
      raise TypeError(
        "candidate must be an "
        "InferenceRuleApplicabilityCandidate"
      )

    if (
      self.candidate.source_step
      is not self.scope_node.proof_step
    ):
      raise ValueError(
        "candidate source_step must be "
        "scope_node.proof_step"
      )

  @property
  def root_entry(
    self,
  ):
    return self.scope_node.root_entry

  @property
  def shortest_depth(
    self,
  ) -> int:
    return self.scope_node.shortest_depth


def find_repository_proof_scope_applicability_candidates(
  scope,
  catalog,
):
  if not isinstance(
    scope,
    RepositoryProofScopeResult,
  ):
    raise TypeError(
      "scope must be a "
      "RepositoryProofScopeResult"
    )

  if not isinstance(
    catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "catalog must be an "
      "InferenceRuleCatalog"
    )

  results = []

  for scope_node in scope.nodes:
    candidates = (
      find_inference_rule_applicability_candidates(
        catalog,
        scope_node.proof_step,
      )
    )

    for candidate in candidates:
      results.append(
        RepositoryProofScopeApplicabilityCandidate(
          scope_node=scope_node,
          candidate=candidate,
        )
      )

  return tuple(
    results
  )
